from Access import Access

Access = Access()
def Reciever(sen):
    # print(sen)
    dis = sen['disease']
    ins = sen['insurance']
    hos = sen['hospital']
    usr = sen['User']
    if len(dis) > 1:
        for i in dis:
            # print('dis',i)
            print("Disease ", Access.getDisease(i[1][0], i[1][1]))
    else:
        print("Disease ",Access.getDisease(dis[0], dis[1]))
    print("User ",Access.getUser(usr[0], usr[1]))
    print("Insurance ",Access.getInsurance(ins[0], ins[1]))
    print("Hospital ",Access.getHospital(hos[0], hos[1]))
    print(sen['task'])

    # tts(sen['task'])