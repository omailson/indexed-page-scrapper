#!/usr/bin/env python2

import json
from bs4 import BeautifulSoup
import collections

import os
import errno

index_html = """
<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8">
        <title>Example</title>
    </head>
    <style type="text/css">
        #list li a, #nav span {
            margin: 5px;
        }
    </style>
    <body>
        <div id="content">
            <ul id="list">
            </ul>
        </div>
    </body>
</html>
"""

page_html = """
<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8">
        <title>Example</title>
    </head>
    <body>
        <div id="content">
        </div>
    </body>
</html>
"""

nav_html = """
<div id="nav"></div>
"""

def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# TODO use package level create_path_if_needed
def create_path_if_needed(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            # TODO Python 3 accepts a exist_ok=True in the function below (so we don't need to check whether the path exists)
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

# TODO move to package-level helpers
def save_soup(soup, filename, create_path=False):
    if create_path:
        create_path_if_needed(filename)
    with open(filename, 'w') as f:
        f.write(soup.encode())

def is_iterable(obj):
    return hasattr(obj, '__iter__')

def value_as_iterable(value):
    if not is_iterable(value):
        return [value]
    return value

class Tag:
    # TODO Documentation
    """A helper class to create BeautifulSoup tags

    """
    def __init__(self, tagName, children=None, *args, **kwargs):
        self.tagName = tagName
        self.args = args
        self.kwargs = kwargs
        self.children = children
    
    @staticmethod
    def create(soup, tag, appendTo=None):
        newTag = soup.new_tag(tag.tagName, *tag.args, **tag.kwargs)
        if tag.children is not None:
            if isinstance(tag.children, Tag):
                newTag.append(Tag.create(soup, tag.children))
            elif is_iterable(tag.children):
                for childTag in tag.children:
                    newTag.append(Tag.create(soup, childTag))
            else:
                newTag.string = tag.children

        if appendTo is not None:
            appendTo.append(newTag)
        return newTag

def build_index_tree(template, data):
    soup_index = BeautifulSoup(template, 'html.parser')
    list_tag = soup_index.find(id='list')

    for user in data:
        new_user = 'New!' if int(user['years_active']) == 0 else ''
        tag = Tag.create(
            soup_index,
            Tag('li', children=[
                Tag('a', href=user['userid'], children=user['name']),
                Tag('strong', children=new_user)
            ])
        )
        list_tag.append(tag)

    return soup_index

def build_page_tree(template, user):
    soup_page = BeautifulSoup(template, 'html.parser')
    content_tag = soup_page.find(id='content')

    h2_tag = Tag.create(soup_page, Tag('h2', user['name']))
    dl_tag = Tag.create(
        soup_page,
        Tag('dl', children=[
            Tag('dt', 'Phone'),
            Tag('dd', id='phone', children=user['phone']),
            Tag('dt', 'Company'),
            Tag('dd', id='company', children=user['company']),
            Tag('dt', 'Years active'),
            Tag('dd', id='years-active', children=user['years_active']),
        ])
    )
    content_tag.append(h2_tag)
    content_tag.append(dl_tag)

    return soup_page

def build_navigation_tree(page_index, total_pages, index_filename_func):
    """Build the navigation bar for pagination

    Args:
        page_index (int): The index of the page this navigation will be added to
        total_pages (int): The total number of pages in the result set
        index_filename_func (function): A reference to a function that returns a filename, given a `page_index`
    """
    def create_nav_item_tag(content, id=None, href=None, strong=False):
        """A helper function to create each of the navigation bar items"""
        if strong:
            content = Tag('strong', children=content)
        if href is not None:
            content = Tag('a', href=href, children=content)
        return Tag('span', children=content, id=id)

    soup_nav = BeautifulSoup(nav_html, 'html.parser')

    # Next and Prev buttons
    prev_href = index_filename_func(page_index - 1) if page_index > 0 else None
    prev_tag = create_nav_item_tag('< Prev', id='prev', href=prev_href)
    next_href = index_filename_func(page_index + 1) if page_index + 1 < total_pages else None
    next_tag = create_nav_item_tag('Next >', id='next', href=next_href)

    children = [prev_tag]
    for p in range(total_pages):
        if p == page_index:
            href = None
            strong = True
        else:
            href = index_filename_func(p)
            strong = False
        children.append(create_nav_item_tag(str(p + 1), href=href, strong=strong))
    children.append(next_tag)


    nav_tag = soup_nav.find(id='nav')
    for child in children:
        nav_tag.append(Tag.create(soup_nav, child))

    return soup_nav

def data1():
    """Generate a simple data set with just 5 items"""
    data = read_json('data.json')
    sample_data = data[0:5]
    soup_index = build_index_tree(index_html, sample_data)
    save_soup(soup_index, 'data1/index.html', create_path=True)

    n = 1
    for user in sample_data:
        soup_page = build_page_tree(page_html, user)
        save_soup(soup_page, 'data1/user%d.html' % n)
        n = n + 1

def data2():
    """Generate a much larger data set with all 100 items"""
    data = read_json('data.json')
    soup_index = build_index_tree(index_html, data)
    save_soup(soup_index, 'data2/index.html', create_path=True)

    n = 1
    for user in data:
        soup_page = build_page_tree(page_html, user)
        save_soup(soup_page, 'data2/user%d.html' % n)
        n = n + 1

def data3():
    """Generate paginated data"""
    data = read_json('data.json')
    items_per_page = 10

    def index_filename(page_index):
        return 'index.html' if page_index == 0 else 'index%d.html' % (page_index+1)

    total_data = len(data)
    total_pages = total_data / items_per_page
    for page_index in range(total_pages):
        start = page_index * items_per_page
        stop = start + items_per_page
        soup_index = build_index_tree(index_html, data[start:stop])
        soup_nav = build_navigation_tree(page_index, total_pages, index_filename)

        content_tag = soup_index.find(id='content')
        content_tag.append(soup_nav)

        save_soup(soup_index, 'data3/%s' % index_filename(page_index), create_path=True)

    n = 1
    for user in data:
        soup_page = build_page_tree(page_html, user)
        save_soup(soup_page, 'data3/user%d.html' % n)
        n = n + 1

if __name__ == '__main__':
    data1()
    data2()
    data3()
