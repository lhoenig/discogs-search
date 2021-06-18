from random import shuffle
from datetime import datetime
from os.path import isfile
import argparse
import pickle
import xml.etree.ElementTree as ET
from requests import get
import lxml


def find_matching_masters(root, styles, year_min, year_max):
    matching_masters = []
    for master in root:
        master_styles = set()
        _styles = master.find('styles')
        if _styles == None:
            continue
        _year = master.find('year')
        if _year != None:
            year = int(_year.text)
            if not (year_min <= year <= year_max):
                continue
        for _style in _styles.findall('style'):
            master_styles.add(_style.text)
        if styles.issubset(master_styles):
            matching_masters.append(master)
    return matching_masters


def shuffled_playlist_from_masters(masters):
    playlist = []
    for master in masters:
        videos = master.find('videos')
        if videos == None:
            continue
        for video in videos.findall('video'):
            playlist.append(video.attrib['src'])
    shuffle(playlist)
    return playlist


def dl_latest_discogs_releases_data():
    year = datetime.now().year
    url = f'http://data.discogs.com/?prefix=data/{year}/'
    print(url)
    rsp = get(url)
    print(rsp.body)


def write_playlist_to_file(pl, fn):
    with open(fn, 'w') as f:
        for ytl in dh_dt_playlist:
            f.write(ytl + '\n')


def load_xml_file(fn):
    print('loading', fn)
    pckl_fn = fn + '.pckl'
    if isfile(pckl_fn):
        print('using pickled')
        with open(pckl_fn, 'rb') as f:
            root = pickle.load(f)
    else:
        tree = ET.parse(fn)
        root = tree.getroot()
        print('loading complete, saving pickle..')
        with open(pckl_fn, 'wb') as f:
            pickle.dump(root, f)
        print('pickle done.')
    return root


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', dest='xml_masters_file', required=True,
                        help='a file like discogs_20210601_masters.xml')
    parser.add_argument('--min-year', dest='min_year',
                        type=int, default=0, help='minimum release year')
    parser.add_argument('--max-year', dest='max_year',
                        type=int, default=9999, help='maxmimum release year')
    parser.add_argument('--styles', nargs='+',
                        default=['Deep House', 'Downtempo'])
    args = parser.parse_args()

    xml_root = load_xml_file(args.xml_masters_file)

    deephouse_downtempo_masters = find_matching_masters(
        xml_root, args.styles, args.year_min, args.year_max)
    print(f'Found {len(deephouse_downtempo_masters)} masters')
    dh_dt_playlist = shuffled_playlist_from_masters(
        deephouse_downtempo_masters)
    write_playlist_to_file(f'{"_".join(args.styles)}-{args.min_year}-{args.max_year}.txt')
