from bs4 import BeautifulSoup
import urllib.request as req
import urllib
import os
import time
import datetime
from urllib.parse import urljoin

url = "https://kanpou.npb.go.jp/index.html"
res = req.urlopen(url)
soup = BeautifulSoup(res, "html.parser")
kanpous = soup.find_all("dd")

for kanpou in kanpous:
    url_temp1 = kanpou.a["href"]
    url2 = "https://kanpou.npb.go.jp"+url_temp1.lstrip('.')
    try:
        res2 = req.urlopen(url2)
        soup2 = BeautifulSoup(res2, "html.parser")
        text_lists = soup2.find_all("span", attrs={"class":"text"})
        for i in text_lists:
            if '破産' in i.get_text():
                court = i.parent.parent

        url_temp2 = court.a["href"] ##裁判所部分のURL
        first_page_number = court.find("span", attrs={"class":"date"}).text ##裁判所部分が始まるページ
        book_number = url_temp1.split("/")[2][-3:]+"号" ##URLで何番目の号かを取得

        for j in text_lists:
            if '会社その他' in j.get_text():
                others = j.parent.parent
        last_page_number = others.find("span", attrs={"class":"date"}).text ##裁判所部分が終わるページ


        ##ファイルのパス設定
        try:
            os.mkdir("C:"+"/"+"kanpou"+"/")
        except:
            pass
        try:
            os.mkdir("C:\kanpou"+"/"+book_number+"/")
        except:
            print("まだ発行された最新号がありません。")


        ##裁判所部分のpdfをダウンロード
        pdf_list = []
        for page_number in range(int(first_page_number), int(last_page_number)):
            if page_number < 10:
                pdf_url = url2[0:49]+"pdf/"+url_temp2[:-7]+str(page_number)+".pdf"
                pdf_list.append(pdf_url)
            else:
                pdf_url = url2[0:49]+"pdf/"+url_temp2[:-8]+str(page_number)+".pdf"
                pdf_list.append(pdf_url)

        filename_list = []
        for target in pdf_list:
            temp_list = target.split("/")
            filename_list.append(temp_list[4][11:14]+"号("+temp_list[4][0:8]+")_p"+temp_list[6][-6:])

        target_dir = "C:\\kanpou\\{}".format(book_number)
        savepath_list = []
        for filename in filename_list:
            savepath_list.append(os.path.join(target_dir, filename))

        for (pdflink, savepath) in zip(pdf_list, savepath_list):
            urllib.request.urlretrieve(pdflink, savepath)
            time.sleep(2)
    except:
        continue

