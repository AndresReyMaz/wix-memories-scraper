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


try:
    html = urlopen('http://clarisseandandres.wixsite.com/wanderlust/single-post/2017/10/14/Ehrwald')
except HTTPError as e:
    print(e)
else:    
    bs = BeautifulSoup(html.read(), 'html.parser')
    print(get_title(bs))
    print("Written by: {}".format(get_author(bs)))
    print(get_main(bs))
