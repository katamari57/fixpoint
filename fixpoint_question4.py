###################################################################
#
#設問4
#ネットワーク経路にあるスイッチに障害が発生した場合、そのスイッチの配下にあるサーバの応答がすべてタイムアウトすると想定される。
#そこで、あるサブネット内のサーバが全て故障（ping応答がすべてN回以上連続でタイムアウト）している場合は、
#そのサブネット（のスイッチ）の故障とみなそう。
#設問2または3のプログラムを拡張して、各サブネット毎にネットワークの故障期間を出力できるようにせよ。
#
###################################################################
import pandas as pd
import datetime 
import csv
import numpy as np
from ipaddress import ip_interface

N=3
m=3
t=100

logData = pd.read_csv(filepath_or_buffer="fixpoint_generated_logdata.csv", encoding="utf-8", sep=",")#csvファイルの読み込み
logData = logData.values#DataFrameだけ抜き出す

serverList=pd.DataFrame()#ipv4毎の情報を格納する
breakDownList=[]#この中に故障状態のサーバーアドレスと、故障期間を格納する
OverloadServerList=[]

ipSearchList=[]#responseTimeListでリスト番号を検索するためだけのリスト　ipv4アドレスが入ってる
responseTimeList=[]#ipv4アドレスごとに時刻をｍ個格納するリスト
subnetList=[]#ネットワークアドレスを入れる　
breakDownList2=[]#各IPで一番古いタイムアウトの時刻を入れる

subnetList2=[]#ネットワークアドレスを重複なしで入れる
subnetSerchList=[]#ipとネットワークアドレスの対応関係のリスト

for log in logData:#ログデータを全て見る　logは[[日時][ipv4][応答結果]]が入ってる
    dt=datetime.datetime(year=int(str(log[0])[0:4]), month=int(str(log[0])[4:6]),
                     day=int(str(log[0])[6:8]),hour=int(str(log[0])[8:10]),
                     minute=int(str(log[0])[10:12]),second=int(str(log[0])[12:14]))#故障時間を見るためにdatatime型に変換
    log[0] =  dt#datatime型に直して格納し直す
    log = np.append(log,0)#故障回数の項目を追加
    if not log[1] in serverList.values:#新しく発見したIPアドレスなら
        serverList = serverList.append(pd.DataFrame([log],index = [str(log[1])]))#サーバーリストに追加
        ipSearchList.append(log[1])
        responseTimeList.append([log[0]])
        ip = ip_interface(log[1])
        subnetList.append(str(ip.network))
        breakDownList2.append("")
        """
        if not subnetList2 in [str(ip_interface(log[1]).network)]:#subnetList2にネットワークアドレスが未登録ならば
            subnetList2.append(str(ip_interface(log[1]).network))
            subnetSerchList.append([])
        subnetSerchList[subnetList2.index(str(ip_interface(log[1]).network))].append(ipSearchList.index(log[1]))
        """
        continue # 最初にIPアドレスをserverListに登録したら、これ以降は飛ばして、次のlogに移る
        
    if serverList.loc[log[1]][2]=="-":#serverListの、同じipがタイムアウトしてたら
        breakDownList2[ipSearchList.index(log[1])]=log[0]
        if log[2] == "-":#更に、今見ているlogがタイムアウトしているなら
            log[3] = serverList.loc[log[1]][3] + 1# serverListは,タイムアウトが連続した回数を記録していく。
        else:#前回タイムアウト、今回タイムアウトではないなら
            if(serverList.loc[log[1]][3] >= N):
                breakDownList.append([log[1],serverList.loc[log[1]][0],
                                 log[0],(log[0]-serverList.loc[log[1]][0]).seconds])
    else:#serverListの、同じipがタイムアウトではない、
        breakDownList2[ipSearchList.index(log[1])]=""
        if log[2] != "-":#更に、今見ているlogがタイムアウトしていないなら
            responseTimeList[ipSearchList.index(log[1])].append(log[0])#
            
            if len(responseTimeList[ipSearchList.index(log[1])]) > m+1:#m+1個の時刻データがあれば、平均応答時間が分かるので、古いものを消す
                del responseTimeList[ipSearchList.index(log[1])][0]
                
            if len(responseTimeList[ipSearchList.index(log[1])]) ==4:
                temporaly=0 #平均応答時間を入れる変数
                for i in range(1,m+1):
                    temporaly += (responseTimeList[ipSearchList.index(log[1])][i] - 
                     responseTimeList[ipSearchList.index(log[1])][i-1]).seconds
                    temporaly /= m#直近m回の平均応答時間を計算
                if temporaly > t:#平均応答時間が閾値ｔを超えていれば
                    OverloadServerList.append([log[1],responseTimeList[ipSearchList.index(log[1])][0],
                                               responseTimeList[ipSearchList.index(log[1])][m]]) #ip,過負荷の頭、終わりの時刻をリストで格納
    serverList.loc[log[1]] = log#serverListを、IPアドレスごとに最新の日付に更新
    #サブネット毎に故障回数が全てN以上か確認する
    
    
    for i in ipSearchList:
        number = subnetList.index(str(ip_interface(i).network))#
    
#csvファイルで書き出し
f = open('fixpoint_question4_breakDownServer.csv', 'w',encoding="utf-8")
writer = csv.writer(f, lineterminator='\n')
writer.writerows(breakDownList)
f.close()
#csvファイルで書き出し
f = open('fixpoint_question4_overloadServer.csv', 'w',encoding="utf-8")
writer = csv.writer(f, lineterminator='\n')
writer.writerows(OverloadServerList)
f.close()


