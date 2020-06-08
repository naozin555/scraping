import urllib.request as req

from service import Service


class Controller(object):

    def execute(self):

        url = "https://www.meti.go.jp/shingikai/enecho/shoene_shinene/" \
              + "sho_energy/001.html"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; \
            NP06; rv:11.0) like Gecko Chrome/42.0.2311.135",
        }
        request = req.Request(url, headers=headers)
        parsed_html = Service.parse_html(request)

        base_url = "https://www.meti.go.jp"
        href_list = []
        text_list = []
        href_list, text_list = Service.get_href(parsed_html, base_url)

        pdf_url_list = []
        pdf_filename_list = []
        pdf_url_list, pdf_filename_list = Service.get_pdf(href_list, text_list)

        Service.pdf_download(pdf_url_list, pdf_filename_list, headers)
