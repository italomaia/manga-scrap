import os
from manga_scrap.manga import Manga
from collections import defaultdict

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


class MangaHere(Manga):
    _comic_url = u"http://www.mangahere.co/manga/%s/"
    _chapter_url = u"http://www.mangahere.co/manga/%s/%s/"

    @staticmethod
    def _get_chapter_name(sel):
        return sel.css('h1.title::text').extract_first()

    @staticmethod
    def _get_alternative_names(sel):
        element = sel.css('ul.detail_topText li')[2]
        element_str = element.css(':not(label)::text').extract_first()
        return [name.strip() for name in element_str.split(';')]

    def _fetch_page_image(self, page_url):
        data = self.read_response(page_url)

        sel = self.parse(data.decode('utf-8'))
        return sel.css('img#image::attr(src)').extract_first()

    @staticmethod
    def _get_chapter_number_of_pages(sel):
        return len(sel.css('select')[1].css('option'))

    def fetch_chapter_id_list(self, comic_url):
        data = self.read_response(comic_url)
        sel = self.parse(data.decode('utf-8'))
        chapter_id_list = list()

        for url in sel.css('.detail_list li a::attr(href)').extract():
            chapter_id_list.append(url[:-1].split('/')[-1])

        return chapter_id_list

    def fetch_chapter_image_list(self, chapter_url):
        data = self.read_response(chapter_url)

        sel = self.parse(data.decode('utf-8'))

        page_url = sel.css('section#viewer a::attr(href)').extract_first()
        page_path = os.path.dirname(page_url)

        image_url = sel.css('img#image::attr(src)').extract_first()

        c = 1
        while True:
            name = os.path.basename(image_url).split('?')[0]

            yield c, name, image_url

            c += 1
            page_url = '/'.join((page_path, "%03d.html" % c))
            image_url = self._fetch_page_image(page_url)

            if not image_url:
                break

    def fetch_comic_info(self, comic_url):
        data = self.read_response(comic_url)

        cls = MangaHere
        sel = self.parse(data)
        rs = defaultdict(lambda: None)
        rs['name'] = cls._get_chapter_name(sel)
        rs['alternative_names'] = cls._get_alternative_names(sel)
        return rs

    def fetch_chapter_info(self, chapter_url):
        data = self.read_response(chapter_url)

        cls = MangaHere
        sel = self.parse(data.decode('utf-8'))
        rs = defaultdict(lambda: None)
        rs['number_of_pages'] = cls._get_chapter_number_of_pages(sel)
        return rs

    def search(self, term):
        pass

    def make_comic_url(self, comic_id):
        return self._comic_url % comic_id

    def make_chapter_url(self, comic_id, chapter_id):
        return self._chapter_url % (comic_id, chapter_id)
