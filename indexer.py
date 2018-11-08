import argparse
import re

from urllib.request import urlopen
from bs4 import BeautifulSoup
'''
This script gathers all of the links to the individual blog posts.
'''

def dedup(l, seen=None):
    '''
    Deduplicates a list, preserving order.
    '''
    if seen is None:
        seen = set()
    return [x for x in l if x not in seen and not seen.add(x)]


def get_post_uris(markup, base_uri):
    '''
    Extracts all the posts' uris in the page.
    '''
    return dedup([uri[:-1] for uri in re.findall(base_uri + '/single-post/[^"]*"', markup)])    


ap = argparse.ArgumentParser()
ap.add_argument('-u', '--url', required=True, help='URL to the blog')
args = vars(ap.parse_args())

try:
    # Parse first page.
    html = urlopen(args['url'])
except HTTPError as e:
    print(e)
else:
    uris = get_post_uris(html.read().decode('utf-8'), args['url'])
    # Parse remaining pages.
    page_number = 1
    while True:
        try:
            html = urlopen(args['url'] + '/blog/page/' + str(page_number))
        except HTTPError as e:
            print(e)
            break
        html_content = html.read().decode('utf-8')
        bs = BeautifulSoup(html_content, 'html.parser')
        empty_page_tag = bs.find('div', {'id':{'ppPrt4-6xh_MediaTopPage_Array__0_0_def_21richTextContainer'}})
        if empty_page_tag is not None:
            print('Done in', page_number)
            break
        print("Trying page", page_number)
        uris += dedup(get_post_uris(html_content, args['url']), set(uris))
        page_number += 1
    print('\n'.join(uris))
        
        
