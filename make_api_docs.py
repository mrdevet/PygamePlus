
import inspect
import os
import pprint
import re
import sys

import pygame
import pygameplus

MODULE = pygameplus
DOCS_DIR = 'docs/'
DOCS_SUBDIR = '_api/'
LINK_FORMATTER = lambda page: f'{{{{ site.baseurl }}}}{{% link {DOCS_SUBDIR}{page} %\}}'

def clean_docstring (obj, short=False):
    docstring = inspect.getdoc(obj)
    if docstring is None or docstring.strip() == '':
        return None
    paragraphs = re.split(2 * os.linesep + '+', docstring)
    return paragraphs[0] if short else '\n\n'.join(paragraphs)

def filter_members (obj, predicate=None, only_all=True, skip_underscores=True):
    members = inspect.getmembers(obj, predicate)
    if only_all and hasattr(obj, '__all__'):
        members = [x for x in members if x[0] in obj.__all__]
    elif skip_underscores:
        members = [x for x in members if not x[0].startswith('_')]
    return members

def document_module (mod, name, parent=None, file=sys.stdout, only_all=True, skip_underscores=True):
    # Print Jekyll header
    print('---', file=file)
    print('layout: default', file=file)
    print(f'title: {name}', file=file)
    if parent:
        print(f'parent: {parent}', file=file)
    print('---', file=file)
    
    # Print name and module docstring
    print(f'# {name}', file=file, end='\n\n')
    if mod.__doc__:
        print(clean_docstring(mod), file=file, end='\n\n')

    # Store the attributes that have been seen to help get "others"
    attributes_seen = []

    # Document submodules
    submods = filter_members(mod, inspect.ismodule, only_all, skip_underscores)
    if submods:
        print(f'## Submodules', file=file, end='\n\n')
        print('| Module | Description |', file=file)
        print('| --- | --- |', file=file)
        for attr, value in submods:
            summary = clean_docstring(value, short=True).replace(os.linesep, '<br />')
            print(f'| {attr} | {summary} |', file=file)
            new_parent = f'{parent}.{name}' if parent else name
            subfile_name = f'{DOCS_DIR}{DOCS_SUBDIR}{new_parent}.{attr}.md'
            with open(subfile_name, 'w') as fn:
                document_module(value, attr, new_parent, fn, only_all, skip_underscores)
            attributes_seen.append(value)
        print(file=file)

    # Document subclasses
    subclasses = filter_members(mod, inspect.isclass, only_all, skip_underscores)
    if subclasses:
        print(f'## Classes', file=file, end='\n\n')
        print('| Class | Description |', file=file)
        print('| --- | --- |', file=file)
        for attr, value in subclasses:
            summary = clean_docstring(value, short=True).replace(os.linesep, '<br />')
            print(f'| {attr} | {summary} |', file=file)
            attributes_seen.append(value)
        print(file=file)

    # Document functions
    funcs = filter_members(mod, inspect.isroutine, only_all, skip_underscores)
    if funcs:
        print(f'## Functions', file=file, end='\n\n')
        print('| Function | Description |', file=file)
        print('| --- | --- |', file=file)
        for attr, value in funcs:
            try:
                signature = inspect.signature(value)
            except:
                signature = "(...)"
            summary = clean_docstring(value, short=True).replace(os.linesep, '<br />')
            print(f'| {attr}{signature} | {summary} |', file=file)
            attributes_seen.append(value)
        print(file=file)

        print(f'## Function Details', file=file, end='\n\n')
        for attr, value in funcs:
            try:
                signature = inspect.signature(value)
            except:
                signature = "(...)"
            print(f'### `{attr}{signature}`', file=file, end='\n\n')
            details = clean_docstring(value)
            if details:
                print(details, file=file, end='\n\n')

    # Document Others
    others_predicate = lambda obj: bool(obj not in attributes_seen)
    others = filter_members(mod, others_predicate, only_all, skip_underscores)
    if others:
        print(f'## Other Attributes', file=file, end='\n\n')
        print('| Name | Description |', file=file)
        print('| --- | --- |', file=file)
        for attr, value in others:
            summary = clean_docstring(value, short=True)
            print(f'| {attr} | {summary} |', file=file)
        print(file=file)


if __name__ == '__main__':
    # pprint.pprint(filter_members(pygameplus))
    # pprint.pprint(filter_members(pygameplus.music_stream))
    with open(f'{DOCS_DIR}{DOCS_SUBDIR}{MODULE.__name__}.md', 'w') as doc_file:
        document_module(MODULE, MODULE.__name__, file=doc_file)
