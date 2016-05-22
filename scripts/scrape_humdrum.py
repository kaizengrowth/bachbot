#!/usr/bin/env python

import click

from lxml import html
import urllib
import urlparse
import requests
import re
import copy
import shutil
import os

@click.command()
@click.argument('keyword', default='Bach+Johann')
def scrape_humdrum(keyword):
    '''Queries kern.humdrum.org with and constructs a corpus of the hits in ./corpus/{keyword}/'''

    directory = './corpus/{0}/'.format(keyword)
    if not os.path.exists(directory):
        os.makedirs(directory)
    click.echo('Saving scrape results to {0}'.format(directory))

    search_url='http://kern.humdrum.org/search?s=t&keyword={0}'.format(keyword)
    click.echo('Requesting {0}'.format(search_url))
    tree = html.fromstring(requests.get(search_url).content)
    all_urls = tree.xpath('//a/@href')
    info_page_urls = filter(
            lambda url: re.search("file=.*format=info", url),
            all_urls)

    for url in info_page_urls:
        parsed_url = urlparse.urlparse(url)
        parsed_query = urlparse.parse_qs(parsed_url.query)

        filename = parsed_query['file'][0]
        new_query = parsed_url.query[:-12] + "&f=kern"

        kern_url = urlparse.urlunparse(parsed_url[:4] + (new_query,) + parsed_url[5:])
        click.echo('Saving {0}'.format(kern_url))
        response = requests.get(kern_url, stream=True)
        with open(directory + filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
