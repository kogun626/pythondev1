import csv
import requests
import re
import datetime
from bs4 import BeautifulSoup

##get date
main_url = "https://zengin.ajtw.net/taiou.php"
html = requests.get(main_url)
soup = BeautifulSoup(html.content, "html.parser")
menu_line = soup.find("div", attrs={"class":"a6"})
menu1 = menu_line.div                              ##上段ニューバーの <div>[全国の金融機関コード・銀行コード・支店コードや店番、支店番号を簡単に検索］</div>
menu2 = menu1.find_next_sibling("div").text        ##ミラーサイト　トップページ　更新日（2020/09/23)


def date_ceansing(text):
    pattern = '\d+/(\d+)/(\d+)'
    r = re.compile(pattern)
    match = r.search(text).group(0)
    return match

renewal_date = "更新日: "+date_ceansing(menu2)

##save as csv
filename = "bank_data-コゴン.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
title = "金融機関名,フリガナ,金融機関コード,支店名,フリガナ,支店コード,住所,電話番号,取得時刻,ループの処理時間(秒),{}".format(renewal_date).split(",")
writer.writerow(title)

##data
now_time = datetime.datetime.now()
for i in range(1, 10000):
    try:
        url1 = "https://zengin.ajtw.net/linkmeisai.php?abg={}".format(i)
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
        res = requests.get(url1, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        if soup.find("div", attrs={"class":"f1"}).text == "支店一覧":
            continue
        if url1:
            for j in range(1, 1000):
                try:
                    url2 = "https://zengin.ajtw.net/dbs5.php?abg={}&abs={}".format(i, j)
                    if url2:
                        res = requests.get(url2, headers=headers)
                        soup = BeautifulSoup(res.text, "lxml")
                        data_rows = soup.find("tbody")
                        bank_name = data_rows("tr")[0]
                        bank_name_is = bank_name("td")[1].text
                        if bank_name_is == "該当なし":
                            continue
                        bank_hurigana = data_rows("tr")[1]
                        bank_hurigana_is = bank_hurigana("td")[1].text
                        bank_code = data_rows("tr")[2]
                        bank_code_is = bank_code("td")[1].text
                        branch_name = data_rows("tr")[3]
                        branch_name_is = branch_name("td")[1].text
                        branch_hurigana = data_rows("tr")[4]
                        branch_hurigana_is = branch_hurigana("td")[1].text
                        branch_code = data_rows("tr")[5]
                        branch_code_is = branch_code("td")[1].text
                        address = data_rows("tr")[6]
                        address_is = address("td")[1]
                        address_is_text = address_is.find("div", attrs={"class":"k1"}).text
                        tel = data_rows("tr")[7]
                        tel_is = tel("td")[1].text
                        loof_time = datetime.datetime.now()-now_time
                        now_time = datetime.datetime.now()
                        writer.writerow([bank_name_is, bank_hurigana_is, bank_code_is, branch_name_is, branch_hurigana_is, branch_code_is, address_is_text, tel_is, now_time.time(), round(loof_time.total_seconds(),2)])
                        print(now_time)
                        
                    else:
                         continue
                except:
                        print('error')         
        else:
            continue
    except:
            print('error')        
f.close()
