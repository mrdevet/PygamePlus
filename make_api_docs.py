
from collections import OrderedDict
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

# Stores the name of each local page
pages = {}

def find_pages (obj, name, parents=[], only_all=True, skip_underscores=True):
    if name == '__base__' or name == '__class__':
        return
    page_name = '.'.join(parents) + '.' + name
    pages[obj] = page_name
    for attr, value in inspect.getmembers(obj):
        if only_all and hasattr(obj, '__all__') and attr not in obj.__all__:
            continue
        if skip_underscores and attr.startswith('_'):
            continue
        if inspect.isclass(value) or inspect.ismodule(value):
            find_pages(value, attr, [name] + parents, only_all, skip_underscores)


def clean_docstring (obj, short=False, blockquote=False):
    docstring = inspect.getdoc(obj)
    if docstring is None or docstring.strip() == '':
        return None
    paragraphs = re.split(2 * os.linesep + '+', docstring)
    paragraphs = [x.replace(os.linesep, ' ') for x in paragraphs]
    if blockquote:
        paragraphs = ['> ' + x for x in paragraphs]
    par_sep = '\n> \n' if blockquote else '\n\n'
    return paragraphs[0] if short else par_sep.join(paragraphs)

def signature (func):
    try:
        return inspect.signature(func)
    except TypeError:
        return ''
    except:
        return '(...)'

def document_module (mod, name, parents=[], file=sys.stdout, only_all=True, skip_underscores=True, recursive=True):
    # If necessary, find local pages
    if mod not in pages:
        find_pages(mod, name, parents)
    
    # Set up dictionary for sorted attributes
    members = OrderedDict()
    members['Submodules'] = []
    members['Classes'] = []
    members['Functions'] = []
    members['Other Members'] = []

    # Sort attributes by kind
    for attr, value in inspect.getmembers(mod):
        if only_all and hasattr(mod, '__all__') and attr not in mod.__all__:
            continue
        if skip_underscores and attr.startswith('_'):
            continue
        if inspect.ismodule(value):
            members['Submodules'].append((attr, value))
        elif inspect.isclass(value):
            members['Classes'].append((attr, value))
        elif inspect.isroutine(value):
            members['Functions'].append((attr, value))
        else:
            members['Other Members'].append((attr, value))

    # Get external docs links
    external_docs = getattr(mod, '_EXTERNAL_DOCS', {})

    # Print Jekyll header
    print('---', file=file)
    print('layout: default', file=file)
    print(f'title: {name}', file=file)
    for index, parent in enumerate(parents):
        if index == 0:
            print(f'parent: {parent}', file=file)
        elif index == 1:
            print(f'grand_parent: {parent}', file=file)
        else:
            print('great_' * (index - 1) + f'grand_parent: {parent}', file=file)
    if members['Classes'] or members['Submodules']:
        print('has_children: true', file=file)
    print('---', file=file)
    
    # Print name and module docstring
    print(f'# {name}', file=file, end='\n\n')
    if mod.__doc__:
        print(clean_docstring(mod), file=file, end='\n\n')
    print('---', file=file, end='\n\n')

    # Print member summaries
    members_with_details = []
    print('## Member Summary', file=file, end='\n\n')
    for kind, kind_members in members.items():
        if not kind_members:
            continue
        print(f'### {kind}', file=file, end='\n\n')
        internal_members = []
        external_members = []
        for attr, value in kind_members:
            if attr in external_docs:
                external_members.append((attr, value))
            else:
                internal_members.append((attr, value))
        if internal_members:
            for attr, value in internal_members:
                sig = signature(value)
                summary = clean_docstring(value, short=True)
                if value in pages:
                    href = '../' + pages[value]
                else:
                    href = f'#{attr}'
                    members_with_details.append((attr, value))
                print(f'| <a href="{href}">`{attr}{sig}`</a> | {summary} |', file=file)
            print(file=file)
        if external_members:
            print(f'**Defined Externally:**', file=file, end='\n\n')
            for attr, value in external_members:
                sig = signature(value)
                href = external_docs[attr]
                print(f'- <a href="{href}">`{attr}{sig}`</a>', file=file)
            print(file=file)
    print('---', file=file, end='\n\n')

    # Document Member Details
    if members_with_details:
        print('## Member Details', file=file, end='\n\n')
        members_with_details.sort()
        for attr, value in members_with_details:
            if attr in external_docs:
                continue
            sig = signature(value)
            print(f'### `{attr}{sig}` {{#{attr}}}', file=file, end='\n\n')
            details = clean_docstring(value, blockquote=True)
            if details:
                print(details, file=file, end='\n\n')

    # Recursively 
    if recursive:
        for attr, value in members['Submodules']:
            if attr in external_docs:
                continue
            with open(f'{DOCS_DIR}{DOCS_SUBDIR}{pages[value]}.md', 'w') as doc_file:
                document_module(value, attr, [name] + parents, doc_file, only_all, 
                                skip_underscores, recursive)
        for attr, value in members['Classes']:
            if attr in external_docs:
                continue
            with open(f'{DOCS_DIR}{DOCS_SUBDIR}{pages[value]}.md', 'w') as doc_file:
                document_class(value, attr, [name] + parents, doc_file, only_all, 
                               skip_underscores, recursive)


def document_class (cls, name, parents=None, file=sys.stdout, only_all=True, skip_underscores=True, recursive=True):
    # If necessary, find local pages
    if cls not in pages:
        find_pages(mod, name, parents)
    
    # Set up dictionary for sorted attributes
    attributes = OrderedDict()
    attributes['Nested Classes'] = []
    attributes['Methods'] = []
    attributes['Static Methods'] = []
    attributes['Class Methods'] = []
    attributes['Properties'] = []
    attributes['Other Attributes'] = []

    # Sort attributes by kind
    for attr, kind, def_cls, value in inspect.classify_class_attrs(cls):
        if skip_underscores and attr.startswith('_'):
            continue
        if inspect.isclass(value):
            attributes['Nested Classes'].append((attr, def_cls, value))
        elif kind == 'static method':
            attributes['Static Methods'].append((attr, def_cls, value))
        elif kind == 'class method':
            attributes['Class Methods'].append((attr, def_cls, value))
        elif kind == 'method':
            attributes['Methods'].append((attr, def_cls, value))
        elif kind == 'property':
            attributes['Properties'].append((attr, def_cls, value))
        else:
            attributes['Other Attributes'].append((attr, def_cls, value))
            print(attr, def_cls, value)

    # Get external docs links
    external_docs = getattr(cls, '_EXTERNAL_DOCS', {})
            
    # Print Jekyll header
    print('---', file=file)
    print('layout: default', file=file)
    print(f'title: {name}', file=file)
    for index, parent in enumerate(parents):
        if index == 0:
            print(f'parent: {parent}', file=file)
        elif index == 1:
            print(f'grand_parent: {parent}', file=file)
        else:
            print('great_' * (index - 1) + f'grand_parent: {parent}', file=file)
    print('---', file=file)
    
    # Print name and module docstring
    print(f'# {name}', file=file, end='\n\n')
    if cls.__doc__:
        print(clean_docstring(cls), file=file, end='\n\n')
    print('---', file=file, end='\n\n')

    # Print attribute summaries
    print('## Attribute Summary', file=file, end='\n\n')
    attributes_with_details = []
    for kind, kind_attributes in attributes.items():
        if not kind_attributes:
            continue
        print(f'### {kind}', file=file, end='\n\n')
        attributes_by_origin = {}
        for attr, def_cls, value in kind_attributes:
            if def_cls in attributes_by_origin:
                attributes_by_origin[def_cls].append((attr, value))
            else:
                attributes_by_origin[def_cls] = [(attr, value)]
        for current_cls in inspect.getmro(cls):
            if current_cls in attributes_by_origin:
                if current_cls is cls:
                    for attr, value in attributes_by_origin[current_cls]:
                        sig = signature(value)
                        sig = re.sub(r'^\(self,? ?', '(', str(sig))
                        summary = clean_docstring(value, short=True)
                        if value in pages:
                            href = '../' + pages[value]
                        else:
                            href = f'#{attr}'
                            attributes_with_details.append((attr, value))
                        print(f'| <a href="{href}">`.{attr}{sig}`</a> | {summary} |', file=file)
                else:
                    if current_cls in pages:
                        page_name = pages[current_cls]
                        print(f'**Inherited from <a href="../{page_name}">`{pages[current_cls]}`</a>:**', file=file, end='\n\n')
                    else:
                        print(f'**Inherited from `{current_cls.__module__}.{current_cls.__name__}`:**', file=file, end='\n\n')
                    for attr, value in attributes_by_origin[current_cls]:
                        sig = signature(value)
                        sig = re.sub(r'^\(self,? ?', '(', str(sig))
                        if attr in external_docs:
                            href = external_docs[attr]
                            print(f'- <a href="{href}">`.{attr}{sig}`</a>', file=file)
                        elif current_cls in pages:
                            href = f'../{page_name}#{attr}'
                            print(f'- <a href="{href}">`.{attr}{sig}`</a>', file=file)
                        else:
                            print(f'- `.{attr}{sig}`', file=file)
                print(file=file)
    print('---', file=file, end='\n\n')

    # Print attribute details
    if attributes_with_details:
        print('## Attribute Details', file=file, end='\n\n')
        for attr, value in attributes_with_details:
            sig = signature(value)
            sig = re.sub(r'^\(self,? ?', '(', str(sig))
            print(f'### `.{attr}{sig}` {{#{attr}}}', file=file, end='\n\n')
            details = clean_docstring(value, blockquote=True)
            if details:
                print(details, file=file, end='\n\n')

    # Recursively 
    if recursive:
        for attr, value in attributes['Nested Classes']:
            with open(f'{DOCS_DIR}{DOCS_SUBDIR}{pages[value]}.md', 'w') as doc_file:
                document_class(value, attr, [name] + parents, doc_file, only_all, 
                               skip_underscores, recursive)
                

if __name__ == '__main__':
    with open(f'{DOCS_DIR}{DOCS_SUBDIR}{MODULE.__name__}.md', 'w') as doc_file:
        document_module(MODULE, MODULE.__name__, file=doc_file)
