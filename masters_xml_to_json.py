import argparse
from os.path import splitext
import xml.etree.ElementTree as ET
import json


def masters_xml_to_obj(root):
    masters = {}
    for master in root:
        mid = int(master.attrib['id'])
        masters[mid] = {}
        masters[mid]['main_release'] = int(master.find('main_release').text)
        masters[mid]['year'] = int(master.find('year').text)
        masters[mid]['title'] = master.find('title').text
        masters[mid]['data_quality'] = master.find('data_quality').text
        if artists := master.find('artists'):
            masters[mid]['artists'] = []
            for artist in artists:
                masters[mid]['artists'].append(
                    {'id': artist.find('id').text, 'name': artist.find('name').text})
        if genres := master.find('genres'):
            masters[mid]['genres'] = []
            for genre in genres.findall('genre'):
                masters[mid]['genres'].append(genre.text)
        if styles := master.find('styles'):
            masters[mid]['styles'] = []
            for style in styles.findall('style'):
                masters[mid]['styles'].append(style.text)
        if videos := master.find('videos'):
            masters[mid]['videos'] = []
            for video in videos.findall('video'):
                masters[mid]['videos'].append({'src': video.attrib['src'], 'title': video.find(
                    'title').text, 'desc': video.find('description').text})
    return masters


def load_xml_file(fn):
    print('loading', fn)
    tree = ET.parse(fn)
    root = tree.getroot()
    print('loading complete')
    return root


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', dest='xml_masters_fn', required=True,
                        help='a file like discogs_20210601_masters.xml')
    args = parser.parse_args()

    masters = masters_xml_to_obj(load_xml_file(args.xml_masters_fn))
    json_masters_fn = f'{splitext(args.xml_masters_fn)[0]}.json'
    with open(json_masters_fn, 'w') as f:
        json.dump(masters, f)
