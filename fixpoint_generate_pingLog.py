import random

def generateIPaddress():#それっぽいIPv4のアドレスを作ります
    ipList=["10."+".".join(map(str,(random.randint(0, 255)for i in range(3))))+"/8",
            "192.168."+".".join(map(str,(random.randint(0, 255)for i in range(2))))+"/16"]
    ip =random.choice(ipList)
    return ip

def generatePinLog(LogQuantity=1000,IPaddressQuantity=10,errerRate=1):#ランダムにpingのログを作ります
    responseList=list(range(1,16,1))
    responseList.append("-")
    weight = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,errerRate]
    
    temporalyIpList=[]
    for i in range(IPaddressQuantity):
        temporalyIpList.append(generateIPaddress())
    
    temporalyLogList=[]
    for i in range(LogQuantity):
        log=""
        log += str(random.randint(2020,2020)).zfill(4)
        log += str(random.randint(10,10)).zfill(2)
        log += str(random.randint(19,19)).zfill(2)
        log += str(random.randint(13,14)).zfill(2)
        log += str(random.randint(0,59)).zfill(2)
        log += str(random.randint(0,59)).zfill(2) + ","
        log += random.choice(temporalyIpList)+","
        log += str(random.choices(responseList,k=1,weights = weight)[0])+"\n"
        temporalyLogList.append(log)
        temporalyLogList = sorted(temporalyLogList)
    return temporalyLogList

#csv形式で出力
f = open('fixpoint_generated_logdata.csv', 'w',encoding="utf-8")
f.writelines(generatePinLog(errerRate=10))
f.close()
    