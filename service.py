import urllib.request as req
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib
import time


class Service(object):

    def parse_whats_new(self):
        resource = req.urlopen(self)
        soup = BeautifulSoup(resource, "html.parser")
        result = soup.find_all("a", tabindex="200")
        return result

    def get_page_url(self, base_url):
        href_list = []
        text_list = []
        for link in self:
            href = link.get('href')
            joined_url = urljoin(base_url, href)
            href_list.append(joined_url)
            text = link.get_text()
            text_list.append(text)
        return href_list, text_list

    def parse_page(self):
        resource = req.urlopen(self)
        soup = BeautifulSoup(resource, "html.parser")
        result = soup.select("a[href]")
        return result

    def get_pdf_url(self, base_url):
        href_list = []
        text_list = []
        for link in self:
            href = link.get('href')
            joined_url = urljoin(base_url, href)
            href_list.append(joined_url)
            text = link.get_text()
            text_list.append(text)
        return href_list, text_list

    def get_pdf(self, text_list):
        i = 0
        pdf_url_list = []
        pdf_filename_list = []
        for link in self:
            if link.endswith('pdf'):
                pdf_url_list.append(link)
                pdf_filename_list.append(text_list[i])
            i += 1
        return pdf_url_list, pdf_filename_list

    def pdf_download(self, pdf_filename_list, headers):
        for i in range(len(self)):
            print(str(i + 1) + '個目のファイルをダウンロード中です。')
            request = req.Request(url=self[i], headers=headers)
            with open('C:/Users/naozi/scraping/dlc/' + pdf_filename_list[i]
                      + '.pdf', "wb") as f:
                f.write(urllib.request.urlopen(request).read())
            time.sleep(2)
        print("指定サイトの全てのpdfファイルのダウンロードが完了しました！")
