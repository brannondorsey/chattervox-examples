#!/usr/bin/env python3
import os
import sys
import json
import argparse
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

def parse_args():
    categories = ['business', 'entertainment', 'general', 'health', 
                  'science', 'sports', 'technology']

    countries = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co',
                 'cu', 'cz', 'de', 'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie',
                 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my', 'ng',
                 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 
                 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za']

    sources = ["abc-news", "abc-news-au", "aftenposten", "al-jazeera-english", 
               "ansa", "argaam", "ars-technica", "ary-news", "associated-press", 
               "australian-financial-review", "axios", "bbc-news", "bbc-sport", 
               "bild", "blasting-news-br", "bleacher-report", "bloomberg", 
               "breitbart-news", "business-insider", "business-insider-uk", 
               "buzzfeed", "cbc-news", "cbs-news", "cnbc", "cnn", "cnn-es", 
               "crypto-coins-news", "daily-mail", "der-tagesspiegel", 
               "die-zeit", "el-mundo", "engadget", "entertainment-weekly", 
               "espn", "espn-cric-info", "financial-post", "financial-times", 
               "focus", "football-italia", "fortune", "four-four-two", 
               "fox-news", "fox-sports", "globo", "google-news", "google-news-ar", 
               "google-news-au", "google-news-br", "google-news-ca", "google-news-fr", 
               "google-news-in", "google-news-is", "google-news-it", "google-news-ru", 
               "google-news-sa", "google-news-uk", "goteborgs-posten", "gruenderszene", 
               "hacker-news", "handelsblatt", "ign", "il-sole-24-ore", "independent", 
               "infobae", "info-money", "la-gaceta", "la-nacion", "la-repubblica", 
               "le-monde", "lenta", "lequipe", "les-echos", "liberation", "marca", 
               "mashable", "medical-news-today", "metro", "mirror", "msnbc", "mtv-news", 
               "mtv-news-uk", "national-geographic", "national-review", "nbc-news", 
               "news24", "new-scientist", "news-com-au", "newsweek", "new-york-magazine", 
               "next-big-future", "nfl-news", "nhl-news", "nrk", "politico", "polygon", 
               "rbc", "recode", "reddit-r-all", "reuters", "rt", "rte", "rtl-nieuws", 
               "sabq", "spiegel-online", "svenska-dagbladet", "t3n", "talksport", 
               "techcrunch", "techcrunch-cn", "techradar", "the-american-conservative", 
               "the-economist", "the-globe-and-mail", "the-guardian-au", "the-guardian-uk", 
               "the-hill", "the-hindu", "the-huffington-post", "the-irish-times", 
               "the-jerusalem-post", "the-lad-bible", "the-new-york-times", "the-next-web", 
               "the-sport-bible", "the-telegraph", "the-times-of-india", "the-verge", 
               "the-wall-street-journal", "the-washington-post", "the-washington-times", 
               "time", "usa-today", "vice-news", "wired", "wired-de", "wirtschafts-woche", 
               "xinhua-net", "ynet"]

    parser = argparse.ArgumentParser(description='Print weather data from OpenWeatherMap.org')
    parser.add_argument('-k', '--key', required=True, help='API Key')
    parser.add_argument('-u', '--country', choices=countries, help='Country code for zip (default: "us")')
    parser.add_argument('-c', '--category', choices=categories, help='Country code for zip (default: "us")')
    parser.add_argument('-s', '--source', choices=sources, help='Country code for zip (default: "us")')
    parser.add_argument('-x', '--exclude', help='A file containing headlines to exclude from search, one headline per line.')
    args = parser.parse_args()

    if args.exclude and not os.path.exists(args.exclude):
        print('--exclude path does not exist.', file=sys.stderr)
        sys.exit(1)

    if args.source and (args.country or args.category):
        print('The --sources flag can\'t be used with the --category or --country flags.', file=sys.stderr)
        sys.exit(1)

    if (args.country and not args.category ) or (args.category and not args.country):
        print('--category and --country must both be used together.', file=sys.stderr)
        sys.exit(1) 

    return args

def load_excluded_titles(path):
    with open(path, 'r') as f:
        return list(set(filter(lambda line: len(line) > 0, f.read().split('\n'))))

def main():

    NEWS_API_URL='https://newsapi.org/v2/top-headlines'
    args = parse_args()
    params = {
        'apiKey': args.key,
    }

    if args.source: params['sources'] = args.source
    if args.country: params['country'] = args.country
    if args.country: params['category'] = args.category

    try:
        response = urlopen('{}?{}'.format(NEWS_API_URL, urlencode(params)))
    except HTTPError as err:
        if err.code == 401:
            print('Unauthorized. Invalid API key: {}'.format(params['appid']))
        else:
            print('{} {}'.format(err.code, err.reason), file=sys.stderr)
        sys.exit(1)

    if response.code == 200:
        try:
            data = json.loads(response.read().decode('utf8'))
        except:
            print('Error interpretting HTTP response as JSON.', file=sys.stderr)
            sys.exit(1)
        
        headlines = list(set([article['title'] for article in data['articles']]))
        if args.exclude:
            excluded = load_excluded_titles(args.exclude)
            # print('loaded {} excluded titles'.format(len(excluded)), file=sys.stderr)
            # print(excluded, file=sys.stderr)
            headlines = list(set(filter(lambda title: not title in excluded, headlines)))
        if len(headlines) > 0: print('\n'.join(headlines))

if __name__ == '__main__':
    main()
