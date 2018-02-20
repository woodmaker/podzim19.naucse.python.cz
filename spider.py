import collections
from urllib.parse import urlparse, urljoin, urldefrag
from tidylib import tidy_document
import sys
import os
import re

import flask
import lxml.html
import requests
from flask_frozen import Freezer

import naucse as the_site


TIDY_IGNORED_ERRORS = {
    r'^line \d+ column \d+ - Warning: <img> lacks "alt" attribute$',
    r'^line 9 column 9 - Warning: trimming empty <style>$',
    r'^line \d+ column \d+ - Warning: <script> proprietary attribute "(integrity|crossorigin)"$',

    # Notebooks:
    r'^line \d+ column 1 - Warning: <img> discarding newline in URI reference$',
    r'^line \d+ column 1 - Warning: <svg> proprietary attribute ".*:.*"$',
    r'^line \d+ column 1 - Warning: discarding unexpected XML declaration$',
    r'^line \d+ column 1 - Warning: <svg> attribute "(width|height)" has invalid value "\d+.\d+"$',
    r'^line \d+ column 1 - Warning: <svg> anchor "[a-z0-9]+" already defined$',
    r'^line \d+ column \d+ - Warning: <th> proprietary attribute "halign"$',
}


def test_spider(client, app, check_external_links):
    """Check that all links work

    Spiders the site, making sure all internal links point to existing pages.
    Includes fragments: any #hash in a link must correspond to existing element
    with id.

    If check_external_links is true, checks external links as well.
    """
    to_visit = {'http://localhost/'}
    visited = set()
    external = set()

    wanted_fragments = collections.defaultdict(set)
    page_ids = {}

    def recording_url_for(*args, **kwargs):
        url = flask.url_for(*args, **kwargs)
        if 'apiref' in url:
            print('?'*80, url, args, kwargs)
        if url not in visited:
            to_visit.add(urljoin('http://localhost/', url))
        return url

    app.jinja_env.globals['url_for'] = recording_url_for

    links_to = {}
    links_to['http://localhost/'] = set()

    while to_visit:
        url = sorted(to_visit)[0]
        to_visit.remove(url)
        if url in visited:
            continue
        visited.add(url)
        links = []
        parsed = urlparse(url)
        if parsed.netloc == 'localhost':
            print('visit', url)
            page_ids[url] = []
            try:
                check_url(client, url, links, page_ids[url])
            except:
                print('! from:', links_to.get(url))
                raise
            for link in links:
                fullurl = urljoin('http://localhost/', url)
                fullurl = urljoin(fullurl, link)
                if 'apiref' in url:
                    print('!'*80, url, link, fullurl)
                result = urldefrag(fullurl)
                defrag = result.url
                fragment = result.fragment
                if fragment and urlparse(fullurl).netloc == 'localhost':
                    wanted_fragments[defrag].add(fragment)
                if defrag not in visited:
                    to_visit.add(defrag)

                links_to.setdefault(fullurl, set()).add(url)
        else:
            if parsed.scheme in ('http', 'https'):
                external.add(url)
            else:
                print('ignore', url)

    for url, fragments in wanted_fragments.items():
        missing = fragments - set(page_ids[url])
        if missing:
            raise AssertionError('Missing fragments for URL {}: {}'.format(
                url, missing))

    if check_external_links:
        for url in sorted(external):
            print('check', url)
            check_external_link(url)

    return visited


def check_url(client, url, links_out=None, ids_out=None):
    if url == 'http://localhost/static/':
        return
    result = client.get(url)
    if result.status_code != 200:
        raise AssertionError("Got HTTP status {} when accessing {}".format(
            result.status_code, url))
    tree = lxml.html.document_fromstring(result.data)
    if links_out is not None:
        for element, attribute, link, pos in tree.iterlinks():
            links_out.append(link)
    if ids_out is not None:
        for element in tree.cssselect('*[id]'):
            ids_out.append(element.attrib['id'])

    if result.content_type.startswith('text/html'):
        check_tidy(url, result.data)


def check_external_link(url):
    status_code = requests.head(url).status_code
    if status_code not in (200, 301, 302):
        raise AssertionError("Got HTTP status {} when accessing {}".format(
            status_code, url))


def check_tidy(url, content):
    document, errors = tidy_document(
        content,
        options={
            'anchor-as-name': 1,
            'numeric-entities': 0,
            'drop-empty-paras': 0,
            'enclose-block-text': 1,
            'enclose-text': 0,
            'fix-uri': 1,
            'merge-divs': 1,
            'break-before-br': 1,
            'punctuation-wrap': 1,
            'sort-attributes': 'alpha',
            'vertical-space': 1,
            'char-encoding': 'utf8',
            'drop-empty-elements': 'no',
        }
    )
    errors = [err for err in errors.splitlines()
              if not any(re.match(e, err) for e in TIDY_IGNORED_ERRORS)]

    if errors:
        for error in errors:
            print('{}: {}'.format(url, error))
        raise AssertionError('HTML check failed')


def main():
    app = the_site.app
    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    freezer = getattr(the_site, 'freezer', Freezer(app))
    client = app.test_client()

    visited = set(test_spider(client, app, False))

    for path in freezer.all_urls():
        url = urljoin('http://localhost/', path)
        if url not in visited:
            print('Unlinked frozen URL:', path)


if __name__ == '__main__':
    main()
