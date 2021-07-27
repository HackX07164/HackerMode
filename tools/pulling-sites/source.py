from requests_html import HTMLSession, HTML


class PullSites:
    def __init__(self, url):
        self.url = url

        session = HTMLSession()
        response = session.get(url)
        response.html.render()
        self.html_text = response.text

    def
