import pandas as pd
import numpy as np
import re
import spacy
import scispacy
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
            'policy': [
                'policy', 'insurance', 'coverage', 'plan', 'premium', 
                'deductible', 'copay', 'benefits', 'claim', 'reimbursement',
                'co-insurance', 'exclusions', 'network', 'provider', 'pre-authorization',
                'waiting period', 'policyholder', 'insured', 'sum assured', 'out-of-pocket',
                'renewal', 'endorsement', 'claim process', 'lapse', 'grace period'
            ]
        }

        self.policy_patterns = [
            r'(?i)(?:my|have|get|the)\s+([A-Za-z\s]+?)\s+policy',
            r'(?i)policy\s+(?:is|from|by|with)\s+([A-Za-z\s]+)',
            r'(?i)insured\s+(?:with|by)\s+([A-Za-z\s]+)',
            r'(?i)covered\s+(?:by|under|with)\s+([A-Za-z\s]+)',
            r'(?i)premium\s+(?:amount|cost|details|of)\s+(\d+\s?\w*)',
            r'(?i)claim\s+(?:process|procedure|details)',
            r'(?i)what\s+(?:does|do)\s+(?:the\s+)?policy\s+cover',
            r'(?i)coverage\s+details',
            r'(?i)policy\s+exclusions',
            r'(?i)what\s+is\s+the\s+waiting\s+period',
            r'(?i)out-of-pocket\s+expenses',
            r'(?i)how\s+to\s+renew\s+the\s+policy',
            r'(?i)grace\s+period\s+for\s+renewal'
        ]

        
        # Question and intent patterns
        self.question_patterns = {
            'terms_conditions': [
                r'(?i)(?:what are|get|know|tell me about|want to know|find out about)\s+(?:the\s+)?terms\s+(?:and\s+)?conditions',
                r'(?i)terms\s+(?:and\s+)?conditions',
                r'(?i)policy\s+details',
                r'(?i)what\s+(?:does|do)\s+(?:the\s+)?policy\s+cover',
                r'(?i)coverage\s+details'
            ]
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
        name_match = re.search(r'(?i)(?:this is|my name is|name[:\s]+|i am)[\s]+([A-Za-z\s]+?)(?:\s+and|\s+i\'m|\s+i am|\s+i|\.|$)', text)
        if name_match:
            entities['name'] = name_match.group(1).strip()
        
        # Extract hospital name
        hospital_patterns = [
            r'(?i)in\s+([A-Za-z\s]+hospital)',
            r'(?i)at\s+([A-Za-z\s]+hospital)',
            r'(?i)([A-Za-z\s]+hospital)'
        ]
        
        for pattern in hospital_patterns:
            hospital_match = re.search(pattern, text)
            if hospital_match:
                entities['hospital'] = hospital_match.group(1).strip()
                break
        
        # Extract age (explicitly using regex)
        age_patterns = [r'age[:|\s]*(\d+)', r'(?:i\'m|i am|my age is)\s+(\d+)[\s-]*years[\s-]*old', r'(\d+)[\s-]*yo', r'(?:i\'m|i am)\s+(\d+)']
        for pattern in age_patterns:
            matches = re.search(pattern, text, re.IGNORECASE)
            if matches:
                entities['age'] = matches.group(1)
                break

        return entities

    def extract_domain_specific_terms(self, text):
        """Extract diseases and policy-related terms."""
        result = {}

        # Extract policy information with improved patterns
        policy_patterns = [
            r'(?i)(?:my|have|get|the)\s+([A-Za-z\s]+?)\s+policy',
            r'(?i)policy\s+(?:is|from|by|with)\s+([A-Za-z\s]+)',
            r'(?i)insured\s+(?:with|by)\s+([A-Za-z\s]+)',
            r'(?i)covered\s+(?:by|under|with)\s+([A-Za-z\s]+)'
        ]
        
        for pattern in policy_patterns:
            policy_match = re.search(pattern, text)
            if policy_match:
                result['policy'] = policy_match.group(1).strip()
                break
        
        # Extract diseases using improved regex
        # Look for specific disease patterns with word boundaries

        
        disease_patterns = [
            #r'(?i)(?:i am having|i have|having|have|diagnosed with|suffering from|been diagnosed with)\s+([A-Za-z\s-]+(?:diabetes|disease|syndrome|disorder|infection|illness|condition|cancer|asthma|hypertension|malaria|flu|fever|covid|tuberculosis|migraine|stroke|pneumonia|arthritis|depression|anxiety|obesity|cholera|dengue|eczema|hepatitis|leukemia|lymphoma|psoriasis|sepsis|ulcer|autism|paralysis|thyroid))\b',
            r'(?i)\b((?:type\s+[12]|gestational)\s+diabetes)\b',
            r'(?i)\b([A-Za-z\s-]+(?:disease|syndrome|disorder|infection|illness|condition|cancer))\b',
            r'(?i)\b(hypertension|diabetes|asthma|malaria|flu|fever|covid|tuberculosis|migraine|stroke|pneumonia|arthritis|depression|anxiety|obesity|cholera|dengue|eczema|hepatitis|leukemia|lymphoma|psoriasis|sepsis|ulcer|autism|paralysis|thyroid)\b'
        ]

        for pattern in disease_patterns:
            matches = re.search(pattern, text)
            if matches:
                result['disease'] = matches.group(1).strip()
                break

        return result


    def extract_query_intent(self, text):
        """Extract the question or intent from the text."""
        intents = {}
        
        # Check for terms and conditions questions
        for intent_type, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    intents[intent_type] = True
                    break
        
        return intents

    def extract_keywords(self, text, num_clusters=5):
        """Extract key sentences using BERT embeddings."""
        processed_text = self.preprocess_text(text)
        sentences = re.split(r'[.!?]', processed_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {}, {}, []
        
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
        
        # Extract query intent
        query_intent = self.extract_query_intent(processed_text)

        # Combine extracted information
        all_keywords = {**entities, **domain_terms}
        
        return all_keywords, query_intent, key_sentences

    def process_query(self, query):
        """Process a user query and extract all relevant information."""
        keywords, query_intent, key_sentences = self.extract_keywords(query)
        
        result = {
            "extracted_info": keywords,
            "query_intent": query_intent,
            "key_sentences": key_sentences
        }
        
        return result

# Example usage
if __name__ == "__main__":
    extractor = BERTKeywordExtractor()
    
    # Single string input
    sample_query = """My name is William. I am 57 years old . I am in Kmch Hospital. 
I have been diagnosed with flu. My policy is Starlife.
Can you tell me the terms and conditions"""
    
    
    print("\nProcessing query:", sample_query)
    result = extractor.process_query(sample_query)
    
    print("\nExtracted Information:")
    for key, value in result["extracted_info"].items():
        print(f"  {key}: {value}")


    true_values = {
    "hospital": "kg hospital",
    "age": "45",
    "policy": "starlife",
    "name": "John",
    #"disease": ["diabetes", "hypertension"]
}

# Use the model to predict
predicted_values = extractor.extract_entities(sample_query)  # Use the method from the class instance

# Compare predictions with ground truth (use the earlier code)
def evaluate_extraction(true_values, keywords):
    """
    Evaluate the accuracy of the extracted information by comparing
    the predicted values with the true values.
    """
    correct = 0
    total = len(true_values)
    
    for key, true_value in true_values.items():
        if key in predicted_values:
            if isinstance(true_value, list):
                # Compare lists (e.g., diseases)
                if set(true_value) == set(predicted_values[key]):
                    correct += 1
            else:
                # Compare single values
                if true_value == predicted_values[key]:
                    correct += 1
    
    return (correct / total) * 100 if total > 0 else 0

accuracy = evaluate_extraction(true_values, result["extracted_info"])
print(f"Extraction accuracy: {accuracy:.2f}%")

print("\nQuery Intent:")
print(result['query_intent'])
if "terms_conditions" in result["query_intent"]:
    print("  User is asking about policy terms and conditions")
else:
    print("  No specific question about terms and conditions detected")
        
print("\nKey Sentences:")
for i, sentence in enumerate(result["key_sentences"]):
    print(f"  {i+1}. {sentence}")
print("-" * 80)
