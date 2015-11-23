import gevent
from gevent import monkey
monkey.patch_socket()

import os
import abc
import socket
import parsel
import logging
import urllib2


def make_sure_folder_exists(path):
    try:  # make sure folder exists
        os.makedirs(path, exist_ok=True)
    except TypeError:
        os.makedirs(path)
    except OSError:
        print("%s already exists. " % path)


class Manga(object):
    __metaclass__ = abc.ABCMeta  # for py2, py3 compatibility

    # CHROME 41
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    request_timeout = 12

    def __init__(self):
        self.logger = logging.getLogger()

    def setup_logger(self, logger):
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    @abc.abstractmethod
    def make_comic_url(self, comic_id):
        return

    @abc.abstractmethod
    def make_chapter_url(self, comic_id, chapter_id):
        return

    @abc.abstractmethod
    def fetch_chapter_info(self, chapter_url):
        return

    @abc.abstractmethod
    def fetch_comic_info(self, comic_url):
        return

    @abc.abstractmethod
    def fetch_chapter_image_list(self, chapter_url):
        return

    @abc.abstractmethod
    def fetch_chapter_id_list(self, comic_url):
        return

    @abc.abstractmethod
    def search(self, term):
        """
        Returns a list of all comics matched in search

        Arguments:
            term: <str> term used with search

        Returns:
            <list<dict>> where dict has the keys url,
            name, alternative_name_list, comic_id, last_chapter
        """
        return

    def make_request(self, url):
        request = urllib2.Request(url, headers={
            'User-Agent': self.USER_AGENT,
            'X-Requested-With': 'XMLHttpRequest',
        })
        return urllib2.urlopen(
            request, timeout=self.request_timeout)

    def read_response(self, url):
        try:
            handle = self.make_request(url)
            data = handle.read()
            handle.close()
            return data
        except socket.timeout:
            handle = self.make_request(url)
            data = handle.read()
            handle.close()
            return data

    @staticmethod
    def parse(data):
        return parsel.Selector(text=data)

    def get_chapter_folder(self, chapter_id):
        return chapter_id

    def download_image(self, url, name, folder):
        """
        Arguments:
            name: <str> name to the image file
            url: <str> full image url
            folder: <str> where the image will be downloaded to
        """
        data = self.read_response(url)
        filepath = os.path.join(folder, name)

        if not os.path.exists(filepath):
            with open(filepath, 'wb') as f:
                f.write(data)

            logging.debug(u'%s downloaded' % name)
        else:
            logging.info(u"%s already exists. Skipped." % filepath)

    def download_chapter(self, comic_id, chapter_id, folder=None):
        chapter_url = self.make_chapter_url(comic_id, chapter_id)
        chapter_folder = self.get_chapter_folder(chapter_id)

        if folder is None:
            folder = chapter_folder
        else:
            folder = os.path.join(folder, chapter_folder)

        make_sure_folder_exists(folder)

        jobs = [
            gevent.spawn(self.download_image, url, name, folder)
            for index, name, url in self.fetch_chapter_image_list(chapter_url)]

        gevent.joinall(jobs)
        self.logger.info("finished downloading chapter")

    def download_comic(self, comic_id, folder=None):
        comic_url = self.make_comic_url(comic_id)

        jobs = [
            gevent.spawn(self.download_chapter, comic_id, chapter_id, folder)
            for chapter_id in self.fetch_chapter_id_list(comic_url)]

        gevent.joinall(jobs)
        self.logger.info("finished downloading comic")

    def get_chapter_info(self, comic_id, chapter_id):
        chapter_url = self.make_chapter_url(comic_id, chapter_id)
        return self.fetch_chapter_info(chapter_url)

    def get_comic_info(self, comic_id):
        comic_url = self.make_comic_url(comic_id)
        return self.fetch_comic_info(comic_url)
