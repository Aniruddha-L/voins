from Sender import main
import blockchain.Access as ac
# STT from whisper
voice = True
sen = main(voice)

def Reciever(sen):
    Access = ac()
    dis = sen['disease']
    ins = sen['insurance']
    hos = sen['hospital']
    usr = sen['User']
    print(Access.getDisease(dis[0], dis[1]))
    print(Access.getUser(usr[0], usr[1]))
    print(Access.getHospital(hos[0], hos[1]))
    print(Access.getInsurance(ins[0], ins[1]))
    print(sen['task'])