from Access import Access

Access = Access()
def Reciever(sen):
    # print(sen)
    data ={}
    arr= []
    dis = sen['disease']
    ins = sen['insurance']
    hos = sen['hospital']
    usr = sen['User']
    if len(dis) > 1:
        for i in dis:
            # print('dis',i)
            print("Disease ", Access.getDisease(i[1][0], i[1][1]))
            arr.append(Access.getDisease(i[1][0], i[1][1]))
        data['disease'] = ', '.join(arr)
    else:
        data['disease'] = Access.getDisease(dis[0], dis[1])
        print("Disease ", data['disease'])
    
    data['user'] = Access.getUser(usr[0], usr[1])
    print("User ",data['user'])
    data['insurance'] =Access.getInsurance(ins[0], ins[1]) 
    print("Insurance ",data['insurance'])
    data ['hospital'] = Access.getHospital(hos[0], hos[1])
    print("Hospital ",data['hospital'])
    print(sen['task'])

    
    string = f"Hi {data['user']}, you are having {data['disease']} disease. Here are the terms and condtion for the {data['hospital']}.{sen['task']}"
    
    # tts(sen['task'])
    return string