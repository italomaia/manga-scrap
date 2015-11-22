import argparse
import pprint
from manga_scrap.spiders import *

SPIDER_MAP = {
    'mangahere': MangaHere
}


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('site', type=str, nargs=1, help='name of the site you wish to scrap')
    parser.add_argument('comic', type=str, nargs='?', help='comic identifier')
    parser.add_argument('chapter', type=str, nargs='?', help='chapter identifier')
    parser.add_argument('-d', '--download', action='store_true', default=False, help='do you want to download?')
    parser.add_argument('-s', '--search', type=str, nargs=1, help='searching term')
    parser.add_argument('-i', '--info', action='store_true', default=False, help='apply to all')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    site = args.site[0]
    manga = SPIDER_MAP[site]()

    if args.download:
        if args.chapter:
            manga.download_chapter(args.comic, args.chapter)
        else:
            manga.download_comic(args.comic)

    if args.info:
        if args.chapter:
            manga.get_chapter_info(args.comic, args.chapter)
        else:
            manga.get_comic_info(args.comic)

    if args.search:
        pprint(manga.search(args.search))


if __name__ == '__main__':
    main()
