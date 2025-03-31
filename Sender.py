import bert as b
import blockchain.Access as ac
import blockchain.Initialization as ini

def main(string):
    keywords, key_sentences = extractor.extract_keywords(string)
    Access = ac()
    forward = {}
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
    if len(disease) > 1:
        for i in disease:
            forward[i] = Access.getDisease(i)
    else:
        forward["disease"] = Access.getDisease(disease)
    forward["insurance"] = Access.getIns(policy)
    forward['hospital'] = Access.getHospital(hos)
    forward['User'] = Access.getUser(user)
    if task:
        forward['task'] = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 
        in voluptate velit esse cillum dolore eu fugiat nulla pariatur.Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
    
    return forward
if __name__ == '__main__':
    extractor = b.BERTKeywordExtractor()
    
    string = """my name is John Smith. my age is 45 years old. i am in Memorial Hospital on January 15 2023.
    i am having Hypertension and Diabetes. my policy is HealthCare Plus"""
    print(string)
    keywords, key_sentences = extractor.extract_keywords(string)
    Access = ac()
    forward = {}
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
    if len(disease) > 1:
        for i in disease:
            forward[i] = Access.getDisease(i)
    else:
        forward["disease"] = Access.getDisease(disease)
    forward["insurance"] = Access.getIns(policy)
    forward['hospital'] = Access.getHospital(hos)
    forward['User'] = Access.getUser(user)
    if task:
        forward['task'] = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 
        in voluptate velit esse cillum dolore eu fugiat nulla pariatur.Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""