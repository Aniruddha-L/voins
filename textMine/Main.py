from rag import textMine
import UniqueValues as uv
from collections import defaultdict

#text from speech
def main(text = ""):
    UV = uv()
    insurance = UV.InsuraceProvider()
    MedicalCon = UV.MedicalCon()
    HosIns = UV.HosIns()
    MediConIns = UV.MediConIns()

    taskList = ['Terms', 'Condition', 'Rules', 'Premium Paid', 'Next Due', 'Remaining term', 'Eligible Hospital']

    extracted = [i.lower() for i in textMine(text)]

    data = defaultdict()

    for i in extracted:
        if i in insurance:
            data['insurance'] = i
            extracted.remove(i)
        elif i in MedicalCon:
            data['MediConIns'] = i
            extracted.remove(i)
        
    for i in HosIns[data['insurance']]:
        if i in extracted:
            data['Hospital'] = i
            extracted.remove(i)
    for i in MediConIns[data['insurance']]:
        if i in extracted and data['MediConIns'] == i:
            data['MedicalCondition'] = i

    for i in taskList:
        if i.lower() in extracted:
            if not data['Task']:
                if i == ' terms' or i == 'condition':
                    data['Task'] = 'Terms and condition'    
                else:
                    data['Task'] = i
            else:
                old = data['Task']
                if i == ' terms' or i == 'condition':
                    data['Task'] = [old,'Terms and condition'    ]
                else:
                    data['Task'] = [old,i]
    
    return data