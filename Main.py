import bert as b
import blockchain.Access as ac
import blockchain.Initialization as ini


if __name__ == '__main__':
    extractor = b.BERTKeywordExtractor()
    
    string = """my name is John Smith. my age is 45 years old. i am in Memorial Hospital on January 15 2023.
    i am having Hypertension and Diabetes. my policy is HealthCare Plus"""
    
    keywords, key_sentences = extractor.extract_keywords(string)

    ini()
    hos = keywords['hospital']
    policy = keywords['policy']
    disease = keywords['disease']
    user = keywords['name']
    age = keywords['age']
    task = keywords['terms_conditions']

    if 'and' in disease:
        disease = disease.split('and')
    if age > 65:
        print('Policy not claimable')
        exit()
    
    