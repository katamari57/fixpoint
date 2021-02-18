###################################################################
#
#設問1
#監視ログファイルを読み込み、故障状態のサーバアドレスとそのサーバの故障期間を出力するプログラムを作成せよ。
#出力フォーマットは任意でよい。
#なお、pingがタイムアウトした場合を故障とみなし、最初にタイムアウトしたときから、次にpingの応答が返るまでを故障期間とする。
#
###################################################################
import pandas as pd
import datetime 
import csv

logData = pd.read_csv(filepath_or_buffer="fixpoint_generated_logdata.csv", encoding="utf-8", sep=",")#csvファイルの読み込み
logData = logData.values#DataFrameだけ抜き出す

serverList=pd.DataFrame()#初期化
breakDownList=[]#この中に故障状態のサーバーアドレスと、故障期間を格納する


for log in logData:#ログデータを全て見る　logは[[日時][ipv4][応答結果]]が入ってる
    dt=datetime.datetime(year=int(str(log[0])[0:4]), month=int(str(log[0])[4:6]),
                     day=int(str(log[0])[6:8]),hour=int(str(log[0])[8:10]),
                     minute=int(str(log[0])[10:12]),second=int(str(log[0])[12:14]))#故障時間を見るためにdatatime型に変換
    log[0] =  dt#datatime型に直して格納し直す
    if not log[1] in serverList.values:#新しく発見したIPアドレスなら
        serverList = serverList.append(pd.DataFrame([log],index = [str(log[1])]))#サーバーリストに追加
        continue # 最初にIPアドレスをserverListに登録したら、これ以降は飛ばして、次のlogに移る
        
    if serverList.loc[log[1]][2]=="-":#serverListの、同じipがタイムアウトしてたら
        if log[2] == "-":#更に、今見ているlogがタイムアウトしているなら
            continue # serverListは更新しないでおく。
        else:#前回タイムアウト、今回タイムアウトではないなら
            breakDownList.append([log[1],serverList.loc[log[1]][0],
                                 log[0],(log[0]-serverList.loc[log[1]][0]).seconds])
    serverList.loc[log[1]] = log#serverListを、IPアドレスごとに最新の日付に更新

#csvファイルで書き出し
f = open('fixpoint_question1_breakDownServer.csv', 'w',encoding="utf-8")
writer = csv.writer(f, lineterminator='\n')
writer.writerows(breakDownList)
f.close()

