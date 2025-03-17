import pandas as pd
class UniqueValues:
    def __init__(self):
        self.data = pd.read_csv('healthcare_dataset.csv')
        self.data.drop(['Name', 'Age', 'Gender', 'Blood Type',
       'Date of Admission', 'Doctor',  
       'Billing Amount', 'Room Number', 'Admission Type', 'Discharge Date',
       'Medication', 'Test Results'], axis=1, inplace=True)
        
    def InsuraceProvider(self):
        arr = []
        for i in self.data['Insurance Provider']:
            if i not in arr:
                arr.append(i)
        return arr
    
    def MedicalCon(self):
        medCon = []
        for i in self.data['Medical Condition']:
            if i not in medCon:
                medCon.append(i)
        return medCon

    def HosIns(self):
        hospital_insurance = self.data.groupby('Insurance Provider')['Hospital'].unique()
        return hospital_insurance.to_dict()

    
    def MediConIns(self):
        disease_insurance = self.data.groupby('Medical Condition')['Insurance Provider'].unique()
        return disease_insurance.to_dict()