import urllib.request as req

from service import Service


class Controller(object):

    def execute(self):

        # 審議会・委員会の新着情報ページから，リンク(aタグ)を取得する。
        url = "https://www.meti.go.jp/shingikai/index.html"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; \
            NP06; rv:11.0) like Gecko Chrome/42.0.2311.135",
        }
        request = req.Request(url, headers=headers)
        parsed_whats_new_html = Service.parse_whats_new(request)

        # 新着情報のある各審議会・委員会の資料のページのURLを取得する。
        base_url = "https://www.meti.go.jp"
        page_url_list, page_name_list = \
            Service.get_page_url(parsed_whats_new_html, base_url)

        # 各審議会・委員会の資料ページから，aタグを取得する。
        # 0番目の要素「新着情報へのurl」と最後の要素「過去の情報一覧へのurl」を省いてfor文を回す。
        # for i in range(1, len(page_url_list)-1):
        for i in range(1, 2):
            url = page_url_list[i]
            base_url = url
            request = req.Request(url, headers=headers)
            parsed_html = Service.parse_page(request)

            # 各審議会・委員会の資料ページのリンク(aタグ)を取得する。
            link_list, text_list = \
                Service.get_pdf_url(parsed_html, base_url)

            # 各審議会・委員会の資料ページのPDFファイルのURLを取得する。
            pdf_url_list, pdf_filename_list = Service.get_pdf(link_list, text_list)

            # PDFファイルのダウンロード
            Service.pdf_download(pdf_url_list, pdf_filename_list, headers)
