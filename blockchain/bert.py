import pandas as pd
import numpy as np
import re
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# Load the SciSpaCy biomedical model for better entity recognition
nlp = spacy.load("en_core_sci_sm")

class BERTKeywordExtractor:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Initialize the BERT model
        self.model = SentenceTransformer(model_name)
        
        # Define healthcare-specific entity categories
        self.healthcare_entities = {
            'PERSON': 'name',
            'DATE': 'date',
            'CARDINAL': 'age',  # Age is often recognized as CARDINAL
            'ORG': 'hospital'
        }
        
        # Additional healthcare terms dictionary
        self.healthcare_terms = {
            'policy': ['policy', 'insurance', 'coverage', 'plan', 'premium', 'deductible', 'copay']
        }

    def preprocess_text(self, text):
        """Clean and normalize text."""
        text = re.sub(r'\s+', ' ', text)  # Remove extra white spaces
        return text.strip()
    
    def extract_entities(self, text):
        """Extract named entities related to healthcare."""
        doc = nlp(text)
        entities = {}

        # Extract relevant named entities
        for ent in doc.ents:
            if ent.label_ in self.healthcare_entities:
                entity_type = self.healthcare_entities[ent.label_]
                entities[entity_type] = ent.text
        
        # Extract name using Spacy entities or patterns
        name_match = re.search(r'(?i)(?:this is|my name is|name[:\s]+)([A-Za-z\s]+)', text)
        if name_match:
            entities['name'] = name_match.group(1).strip()
        
        # Extract hospital name
        hospital_match = re.search(r'(?i)in\s+([A-Za-z\s]+hospital)', text)
        if hospital_match:
            entities['hospital'] = hospital_match.group(1).strip()
        
        # Extract age (explicitly using regex)
        age_patterns = [r'age[:|\s]*(\d+)', r'(?:i\'m|i am|my age is)\s+(\d+)[\s-]*years[\s-]*old', r'(\d+)[\s-]*yo']
        for pattern in age_patterns:
            matches = re.search(pattern, text, re.IGNORECASE)
            if matches:
                entities['age'] = matches.group(1)
                break

        return entities

    def extract_domain_specific_terms(self, text):
        """Extract diseases and policy-related terms."""
        result = {}

        # Extract known healthcare-related terms
        text_lower = text.lower()
        for category, terms in self.healthcare_terms.items():
            for term in terms:
                if term in text_lower:
                    pattern = r'(?i)([^.!?]*\b' + term + r'[^.!?]*)'
                    matches = re.findall(pattern, text)
                    if matches:
                        # Clean up the policy text
                        policy_text = matches[0].strip()
                        # Extract just the insurance company name if possible
                        insurance_match = re.search(r'(?i)in\s+([A-Za-z\s]+insurance)', policy_text)
                        if insurance_match:
                            result[category] = insurance_match.group(1).strip()
                        else:
                            result[category] = policy_text
                        break
        
        # Extract diseases using improved regex
        # Look for specific disease patterns with word boundaries
        disease_patterns = [
            r'(?i)(?:i am having|i have|having|have|diagnosed with|suffering from)\s+([A-Za-z\s]+(?:diabetes|disease|syndrome|disorder|infection|illness|condition|cancer|asthma)\b)',
            r'(?i)\b((?:type\s+[12]|gestational)\s+diabetes)\b',
            r'(?i)\b([A-Za-z\s]+(?:disease|syndrome|disorder|infection|illness|condition))\b'
        ]
        
        for pattern in disease_patterns:
            matches = re.search(pattern, text)
            if matches:
                result['disease'] = matches.group(1).strip()
                break
                
        return result

    def extract_keywords(self, text, num_clusters=5):
        """Extract key sentences using BERT embeddings."""
        processed_text = self.preprocess_text(text)
        sentences = re.split(r'[.!?]', processed_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {}, {}
        
        # Get sentence embeddings
        embeddings = self.model.encode(sentences)
        
        # Perform clustering if sentences are greater than num_clusters
        if len(sentences) > num_clusters:
            kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(embeddings)
            closest_indices = []

            for i in range(num_clusters):
                cluster_sentences = np.where(kmeans.labels_ == i)[0]
                if len(cluster_sentences) > 0:
                    centroid = kmeans.cluster_centers_[i].reshape(1, -1)
                    sentence_embeddings = embeddings[cluster_sentences]
                    similarities = cosine_similarity(centroid, sentence_embeddings)[0]
                    closest_idx = cluster_sentences[np.argmax(similarities)]
                    closest_indices.append(closest_idx)
            
            key_sentences = [sentences[i] for i in closest_indices]
        else:
            key_sentences = sentences

        # Extract named entities
        entities = self.extract_entities(processed_text)

        # Extract healthcare-related terms
        domain_terms = self.extract_domain_specific_terms(processed_text)

        # Combine extracted information
        all_keywords = {**entities, **domain_terms}
        
        return all_keywords, key_sentences

    def process_documents(self, documents):
        """Process multiple documents and extract healthcare information."""
        results = []
        for doc in documents:
            keywords, _ = self.extract_keywords(doc)
            results.append(keywords)
        return results

# Example usage
if __name__ == "__main__":
    extractor = BERTKeywordExtractor()
    
    sample_text = """my name is John Smith. my age is 45 years old. i am in Memorial Hospital on January 15 2023.
    i am having Hypertension and Diabetes. my policy is HealthCare Plus"""
    
    keywords, key_sentences = extractor.extract_keywords(sample_text)
    print("Extracted Healthcare Information:")
    for key, value in keywords.items():
        print(f"{key}: {value}")