import re
import argparse
import pathlib
from itertools import takewhile
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_main(bs):
    '''
    Retrieves the main text section.
    '''
    paragraph_tags = bs.find_all('p', {'class':{'font_8'}})
    for i, tag in enumerate(paragraph_tags):
        if 'Tags:' in tag.get_text():
            paragraph_tags = paragraph_tags[:i-1]
    # Filter out the blog tags.
    return '\n'.join([tag.get_text() for tag in paragraph_tags])
    

def get_title(bs):
    '''
    Retrieves the title from the post.
    '''
    return bs.find('em').get_text()


def get_author(bs):
    '''
    Retrieves the post's author.
    '''
    parent = bs.find('div', {'id':{'ppPrtb-1br4_SinglePostMediaTop_MediaPost__0_0_authorrichTextContainer'}})
    if parent:
        return parent.contents[0].get_text()
    else:
        return 'not found'


def get_image_uris(markup):
    '''
    Finds all the post's image uris, extracted from the JS code.
    '''
    uri_list = re.findall('static.wixstatic.com[^"&]*.jp[e]?g', markup)
    # Place into a set to make unique.
    uri_set = set(uri_list)
    # Remove escape slashes.
    return [re.sub(r'\\', '', uri) for uri in uri_set]

ap = argparse.ArgumentParser()
ap.add_argument('-u', '--url', required=True, help='URL to the post')
ap.add_argument('-o', '--output', required=True, help='Path of output folder to be created')
args = vars(ap.parse_args())

try:
    html = urlopen(args['url'])
    html_content = html.read()
except HTTPError as e:
    print(e)
else:    
    bs = BeautifulSoup(html_content, 'html.parser')
    pathlib.Path(args['output'] + '/images').mkdir(parents=True, exist_ok=True)
    with open(args['output'] + '/post.txt', 'w+') as f:
        f.write(get_title(bs))
        f.write('\n')
        f.write("Written by {}".format(get_author(bs)))
        f.write('\n\n')
        f.write(get_main(bs))

    # Download and save images.
    image_uris = get_image_uris(html_content.decode('utf-8'))
    for i, uri in enumerate(image_uris):
        if 'mv2' in uri:
            with open(args['output'] + '/images/' + str(i) + '.jpg', 'wb+') as f:
                f.write(urlopen('http://' + uri).read())

