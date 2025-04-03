import bert as b
from Access import Access
from Initialization import Initialization
from Recorder import record
import os
from Reciever import Reciever

extractor = b.BERTKeywordExtractor()
def main(string):
    keywords, key_sentences, se = extractor.extract_keywords(string)
    Acces = Access()
    forward = {}
    os.system('cd blockchain')
    Initialization()
    os.system('cd ..')
    # print(keywords)
    hos = keywords['hospital']
    policy = keywords['policy']
    disease = keywords['disease']
    user = keywords['name']
    age = int(keywords['age'])
    forward['disease'] = list()
    # task = keywords['terms_conditions']
    if 'and' in disease:
        disease = disease.split('and')
    if age > 65:
        print('Policy not claimable')
        exit()
    # print(disease)
    if len(disease) > 1:
        for i in disease:
            # print(i)
            forward['disease'].append((i, Acces.getADisease(disName = i)))
    else:
        forward["disease"] = Acces.getADisease(disName = disease)
    print(forward['disease'])
    forward["insurance"] = Acces.getAIns(policy)
    forward['hospital'] = Acces.getAHospital(hos)
    forward['User'] = Acces.setUser(user, forward['hospital'][1], forward['insurance'][1])
    # print(forward)
    # if task:

    forward['task'] = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 
    in voluptate velit esse cillum dolore eu fugiat nulla pariatur.Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
    
    # Reciever(forward)
    return forward
if __name__ == '__main__':
    
    string = """my name is John Smith. my age is 45 years old. i am in Memorial Hospital on January 15 2023.
    i am having Hypertension and Diabetes. my policy is HealthCare Plus"""
    main(string)