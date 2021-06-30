import argparse
import json
from tempfile import NamedTemporaryFile
from os.path import join, splitext, abspath
from sys import stdout
from os import system, chdir, getcwd
import pathlib
from pprint import pprint
from blessings import Terminal

t = Terminal()


def filter_masters(masters, styles, min_year, max_year):
    assert(min_year <= max_year)
    filtered = {k: v for k, v in masters.items(
    ) if 'styles' in v and styles.issubset(set(v['styles']))}
    filtered = {k: v for k, v in filtered.items() if min_year <=
                v['year'] <= max_year}
    return filtered


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='json_fn', required=True,
                        help='masters json file converted from XML before')
    parser.add_argument('--min-year', dest='min_year',
                        type=int, default=0, help='minimum release year')
    parser.add_argument('--max-year', dest='max_year',
                        type=int, default=9999, help='maxmimum release year')
    parser.add_argument('--styles', nargs='+',
                        default=['Deep House', 'Downtempo'])
    parser.add_argument('-a', '--action', dest='results_action', default='json_file',
                        choices=['json_console', 'json_file',
                                 'desc_short', 'links_file', 'links_dl', 'nop'],
                        help='action to perform on the found releases')
    parser.add_argument('-o', '--outdir', dest='out_dir', default='.',
                        help='output directory for actions writing to disk')
    args = parser.parse_args()

    args.json_fn = abspath(args.json_fn)
    args.out_dir = abspath(args.out_dir)
    pathlib.Path(args.out_dir).mkdir(parents=True, exist_ok=True)

    print('loading masters json... ', end='')
    stdout.flush()
    with open(args.json_fn, 'r') as f:
        masters = json.load(f)
    print(t.bold('done'))
    print(f'masters loaded: {t.bold_green(str(len(masters)))}')

    print(
        f'filter:\n  styles: {t.bold_cyan(", ".join(args.styles))}\n  year:   '
        f'{t.bold_cyan(str(args.min_year) + " <= year <= " + str(args.max_year))}')
    results = filter_masters(masters, set(args.styles),
                             args.min_year, args.max_year)
    print(f'result: {t.bold_green(str(len(results)))} masters')

    filter_str = f'{"".join(list(set(args.styles))).replace(" ", "")}_{args.min_year}-{args.max_year}'
    json_name = splitext(args.json_fn)[0]

    def write_results_to_json_file():
        fn = join(args.out_dir, f'{json_name}_{filter_str}.json')
        with open(fn, 'w') as f:
            json.dump(results, f)
        stdout.flush()
        print(f'wrote results to {fn}')

    def print_short_description():
        results_list = [{'id': k, **v} for k, v in results.items()]
        results_list.sort(key=lambda l: l['year'])
        for r in results_list:
            print(f'{", ".join(a["name"] for a in r["artists"])} - '
                  f'{r["title"]} ({r["year"]}) [https://discogs.com/master/{r["id"]}]')

    def get_all_yt_links():
        video_links = []
        results_list = [{'id': k, **v} for k, v in results.items()]
        results_list.sort(key=lambda l: l['year'])
        for r in results_list:
            if 'videos' in r:
                for video in r['videos']:
                    video_links.append(video['src'])
        return video_links

    def write_yt_links_to_file():
        video_links = get_all_yt_links()
        links_fn = join(args.out_dir, f'{json_name}_{filter_str}_yt_links.txt')
        with open(links_fn, 'w') as f:
            f.write('\n'.join(video_links) + '\n')
        stdout.flush()
        print(f'wrote youtube links to {links_fn}')

    if args.results_action == 'json_console':
        pprint(results)

    elif args.results_action == 'json_file':
        write_results_to_json_file()

    elif args.results_action == 'desc_short':
        print_short_description()

    elif args.results_action == 'links_file':
        write_yt_links_to_file()

    elif args.results_action == 'links_dl':
        write_yt_links_to_file()
        video_links = get_all_yt_links()
        print(f'{t.bold("downloading ")}{t.bold(str(len(video_links)))} {t.bold("tracks using youtube-dl")}')
        with NamedTemporaryFile() as f:
            f.write(bytes('\n'.join(video_links) + '\n', 'utf8'))
            stdout.flush()
            tmpdir = getcwd()
            chdir(args.out_dir)
            ytdl_cmd = f'youtube-dl -ia {f.name} -x -f140'
            system(ytdl_cmd)
            chdir(tmpdir)

    elif args.results_action == 'nop':
        pass
