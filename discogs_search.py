import argparse
import json
from os.path import splitext
from sys import stdout
from pprint import pprint


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
    parser.add_argument('-o', '--output', dest='outf', default='json_file',
                        choices=['json', 'json_file', 'short', 'links', 'none'])
    args = parser.parse_args()

    print('loading masters json...', end='')
    stdout.flush()
    with open(args.json_fn, 'r') as f:
        masters = json.load(f)
    print(f'done. {len(masters)} masters.')

    print(
        f'filtering: styles {args.styles}, {args.min_year} <= year <= {args.max_year}')
    results = filter_masters(masters, set(args.styles),
                             args.min_year, args.max_year)
    print(f'results: {len(results)}')

    if args.outf == 'json':
        pprint(results)
    elif args.outf == 'json_file':
        fn = f'{splitext(args.json_fn)[0]}_{"".join(list(set(args.styles))).replace(" ", "")}_{args.min_year}-{args.max_year}.json'
        with open(fn, 'w') as f:
            json.dump(results, f)
    elif args.outf == 'short':
        for k, v in results.items():
            print(
                f'{", ".join(a["name"] for a in v["artists"])} - {v["title"]} ({v["year"]})')
    elif args.outf == 'links':
        pass
    elif args.outf == 'none':
        pass
