import csv
import pandas as pd

##pandasライブラリを利用し、CSVを読み込む
f1 = pd.read_csv('bank_data(2020.10.05).csv', names=['金融機関名','フリガナ','金融機関コード','支店名','フリガナ2','支店コード','住所','電話番号','取得時刻','ループの処理時間(秒)','更新日'], encoding="utf-8-sig")
f2 = pd.read_csv('bank_data(2020.10.13).csv', names=['金融機関名','フリガナ','金融機関コード','支店名','フリガナ2','支店コード','住所','電話番号','取得時刻','ループの処理時間(秒)','更新日'], encoding="utf-8-sig")

##比較に不要なカラムを取り除く
f1 = f1.drop(0,0)
f1 = f1.drop(['取得時刻','ループの処理時間(秒)','更新日'], axis=1)
f2 = f2.drop(0,0)
f2 = f2.drop(['取得時刻','ループの処理時間(秒)','更新日'], axis=1)

##data_Updates.csvを取得
with open('data_Updates.csv', 'w', newline="", encoding="utf-8-sig") as outFile:
    writer=csv.writer(outFile)
    header_list = ['金融機関名','フリガナ','金融機関コード','支店名','フリガナ2','支店コード','住所','電話番号','1:変更 2:追加']
    writer.writerow(header_list)
    for i in range(len(f2)):
        bank_code = f2.iloc[i,2]
        branch_code = f2.iloc[i,5]
        if bank_code in f1.iloc[:,2].values:
            if branch_code in f1.iloc[:,5].values:
                if (f2.iloc[i,0] not in f1.iloc[:,0].values) or (f2.iloc[i,1] not in f1.iloc[:,1].values) or (f2.iloc[i,3] not in f1.iloc[:,3].values) or (f2.iloc[i,4] not in f1.iloc[:,4].values) or (f2.iloc[i,6] not in f1.iloc[:,6].values) or (f2.iloc[i,7] not in f1.iloc[:,7].values):
                    output=','.join(f2.iloc[i,:].values)+',1\n'
                    outFile.write(output)
                else:
                    continue
            else:
                output=','.join(f2.iloc[i,:].values)+',2\n'
                outFile.write(output)

          

    
