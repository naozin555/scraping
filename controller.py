import urllib.request as req
import csv
import os

from service import WhatsNewService, PdfDlService


class Controller(object):

    def execute(self):

        BASE_DIR = 'C:/Users/naozi/scraping/dlc/'

        # 審議会・委員会の新着情報ページから，リンク(aタグ)を取得する。
        url = "https://www.meti.go.jp/shingikai/index.html"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; \
            NP06; rv:11.0) like Gecko Chrome/42.0.2311.135",
        }
        request = req.Request(url, headers=headers)
        parsed_whats_new_html = WhatsNewService.parse_whats_new(request)

        # 新着情報のある各審議会・委員会の資料のページのURLを取得する。
        base_url = "https://www.meti.go.jp"
        page_url_list, page_name_list = \
            WhatsNewService.get_page_url(parsed_whats_new_html, base_url)
        dict_page = {}
        for i in range(len(page_name_list)):
            dict_page.setdefault(page_url_list[i], page_name_list[i])

        # 前回の新着情報ページとの差分を抽出する
        diff_page_url_list = \
            WhatsNewService.comp_page_url_list(page_url_list, BASE_DIR)
        diff_page_name_list = []
        for diff_page_url in diff_page_url_list:
            diff_page_name_list.append(dict_page[diff_page_url])

        # 前回差分のみの各審議会・委員会の資料ページから，aタグを取得する。
        for i in range(len(diff_page_url_list)):
            url = diff_page_url_list[i]
            base_url = url
            request = req.Request(url, headers=headers)
            parsed_html = PdfDlService.parse_page(request)

            # 各審議会・委員会の資料ページのリンク(aタグ)を取得する。
            link_list, text_list = \
                PdfDlService.get_pdf_url(parsed_html, base_url)

            # 各審議会・委員会の資料ページのPDFファイルのURLを取得する。
            pdf_url_list, pdf_filename_list = \
                PdfDlService.get_pdf(link_list, text_list)

            # PDFファイルのダウンロード
            dl_dir = BASE_DIR + diff_page_name_list[i] + '/'
            os.makedirs(dl_dir)
            PdfDlService.pdf_download(pdf_url_list, pdf_filename_list, headers, dl_dir)
        print('全ての更新分のPDFファイルのダウンロードが完了しました！！')

        # 現在の新着情報ページの資料ページ一覧を保存する
        with open(BASE_DIR + '前回分.csv', 'w') as f:
            writer = csv.writer(f, lineterminator="")
            writer.writerow(page_url_list)
