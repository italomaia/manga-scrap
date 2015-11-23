import os
import shutil
import pytest
from unittest import TestCase


class MangaHereTest(TestCase):
    comic_id = 'traeh'
    chapter_id = 'c001'
    chapter_count = 1
    first_chapter_page_count = 36
    download_to = "/tmp/manga/"

    def setUp(self):
        from manga_scrap.spiders import MangaHere
        self.manga = MangaHere()

    def tearDown(self):
        if os.path.exists(self.download_to):
            shutil.rmtree(self.download_to)

        print("%s erased" % self.download_to)

    def test_comic_download(self):
        self.manga.download_comic('hungry_prince', self.download_to)

        download_dir = os.path.join(self.download_to, 'c001')

        # the chapter folder exists
        assert os.path.exists(download_dir)

        # one-shot, so, 1 folder
        assert len(os.listdir(self.download_to)) == 1

        # 32 pages
        assert len(os.listdir(download_dir)) == 32

    def test_chapter_download(self):
        self.manga.download_chapter('nickelodeon', 'c001', self.download_to)

        download_dir = os.path.join(self.download_to, self.chapter_id)
        assert os.path.exists(download_dir)
        assert len(os.listdir(download_dir)) == 9  # 9 pages
