from bs4 import BeautifulSoup
import urllib.request as req
from urllib.parse import urljoin
import urllib
import time


url = "https://www.meti.go.jp/shingikai/enecho/shoene_shinene/sho_energy/001.html"
headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NP06; rv:11.0) like Gecko Chrome/42.0.2311.135",
         }
request = req.Request(url, headers=headers)
soup = BeautifulSoup(request, "html.parser")
result = soup.select("a[href]")

base = "https://www.meti.go.jp"
link_list = []
text_list = []
for link in result:
    href = link.get('href')
    joined_url = urljoin(base, href)
    link_list.append(joined_url)
    doc = link.get_text()
    text_list.append(doc)

pdf_url_list = []
pdf_filename_list = []
i = 0
for link in link_list:
    if link.endswith('pdf'):
        pdf_url_list.append(link)
        pdf_filename_list.append(text_list[i])
    i += 1

for i in range(len(pdf_url_list)):
    print(str(i+1) + '個目のファイルをダウンロード中です。')
    request = req.Request(url=pdf_url_list[i], headers=headers)
    with open('C:/Users/naozi/scraping/dlc/' + pdf_filename_list[i] + '.pdf', "wb") as f:
        f.write(urllib.request.urlopen(request).read())
    time.sleep(2)

print("指定サイトの全てのpdfファイルのダウンロードが完了しました！")
