Get Discogs XML files here: http://data.discogs.com/

- Download for example http://discogs-data.s3-us-west-2.amazonaws.com/data/2021/discogs_20210601_masters.xml.gz and `gunzip`

Then:

```
❯ discogs-search % python discogs_search.py --styles "Deep House" "Downtempo" --min-year 1995 --max-year 2000 -i discogs_20210601_masters.json -a json_file
loading masters json... done
masters loaded: 1893892
filter:
  styles: Deep House, Downtempo
  year:   1995-2000
result: 333 masters
wrote results to /home/lfs/discogs-search/discogs_20210601_masters_DeepHouseDowntempo_1995-2000.json
```

Options:
```
usage: discogs_search.py [-h] -i JSON_FN [--min-year MIN_YEAR] [--max-year MAX_YEAR] [--styles STYLES [STYLES ...]] [-a {json_console,json_file,desc_short,links_file,links_dl,nop}] [-o OUT_DIR]
discogs_search.py: error: the following arguments are required: -i
```
