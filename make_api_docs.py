
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

namespace = {}    

def clean_docstring (obj, short=False, replace_newlines=False, blockquote=False):
    docstring = inspect.getdoc(obj)
    if docstring is None or docstring.strip() == '':
        return None
    paragraphs = re.split(2 * os.linesep + '+', docstring)
    if replace_newlines:
        paragraphs = [x.replace(os.linesep, '<br />') for x in paragraphs]
    if blockquote:
        paragraphs = ['> ' + x for x in paragraphs]
    par_sep = '\n> \n' if blockquote else '\n\n'
    return paragraphs[0] if short else par_sep.join(paragraphs)

def filter_members (obj, predicate=None, only_all=True, skip_underscores=True):
    members = inspect.getmembers(obj, predicate)
    if only_all and hasattr(obj, '__all__'):
        members = [x for x in members if x[0] in obj.__all__]
    elif skip_underscores:
        members = [x for x in members if not x[0].startswith('_')]
    return members

def signature (func):
    try:
        return inspect.signature(func)
    except TypeError:
        return ''
    except:
        return '(...)'

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
            summary = clean_docstring(value, short=True)
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
            summary = clean_docstring(value, short=True)
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
            summary = clean_docstring(value, short=True)
            print(f'| {attr}{signature} | {summary} |', file=file)
            attributes_seen.append(value)
        print(file=file)

    # Document Others
    others_predicate = lambda obj: bool(obj not in attributes_seen)
    others = filter_members(mod, others_predicate, only_all, skip_underscores)
    if others:
        print(f'## Other Attributes', file=file, end='\n\n')
        print('| Name | Value |', file=file)
        print('| --- | --- |', file=file)
        for attr, value in others:
            print(f'| {attr} | {value!r} |', file=file)
        print(file=file)

    # Document Function Details
    if funcs:
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


classes = {}

def document_class (cls, name, parent=None, file=sys.stdout, only_all=True, skip_underscores=True):
    # Print Jekyll header
    print('---', file=file)
    print('layout: default', file=file)
    print(f'title: {name}', file=file)
    if parent:
        print(f'parent: {parent}', file=file)
    print('---', file=file)

    classes[name] = cls
    
    # Print name and module docstring
    print(f'# {name}', file=file, end='\n\n')
    if cls.__doc__:
        print(clean_docstring(cls), file=file, end='\n\n')
    print('---', file=file, end='\n\n')

    attributes = OrderedDict()
    attributes["Nested Classes"] = []
    attributes["Methods"] = []
    attributes["Static Methods"] = []
    attributes["Class Methods"] = []
    attributes["Properties"] = []
    attributes["Other Attributes"] = []

    # Sort attributes by kind
    attributes_defined_here = []
    for attr, kind, def_cls, value in inspect.classify_class_attrs(cls):
        if skip_underscores and attr.startswith('_'):
            continue
        if inspect.isclass(value):
            attributes["Nested Classes"].append((attr, def_cls, value))
        elif kind == "static method":
            attributes["Static Methods"].append((attr, def_cls, value))
        elif kind == "class method":
            attributes["Class Methods"].append((attr, def_cls, value))
        elif kind == "method":
            attributes["Methods"].append((attr, def_cls, value))
        elif kind == "property":
            attributes["Properties"].append((attr, def_cls, value))
        else:
            attributes["Other Attributes"].append((attr, def_cls, value))
        if def_cls is cls:
            attributes_defined_here.append((attr, value))

    # Print attribute summaries
    print('## Attribute Summary', file=file, end='\n\n')
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
                    print('| Attribute | Description |', file=file)
                    print('| --- | --- |', file=file)
                    for attr, value in attributes_by_origin[current_cls]:
                        sig = signature(value)
                        summary = clean_docstring(value, True, True)
                        print(f'| `{attr}{sig}` | {summary} |', file=file)
                else:
                    print(f'**Inherited from `{current_cls.__module__}.{current_cls.__name__}`:**', file=file, end='\n\n')
                    for attr, value in attributes_by_origin[current_cls]:
                        sig = signature(value)
                        print(f'- `{attr}{sig}`', file=file)
                print(file=file)
    print('---', file=file, end='\n\n')

    # Print attribute details
    print('## Attribute Details', file=file, end='\n\n')
    for attr, value in attributes_defined_here:
        sig = signature(value)
        print(f'### `{attr}{sig}`', file=file, end='\n\n')
        details = clean_docstring(value, blockquote=True)
        if details:
            print(details, file=file, end='\n\n')
                


if __name__ == '__main__':
    # pprint.pprint(filter_members(pygameplus))
    # with open(f'{DOCS_DIR}{DOCS_SUBDIR}{MODULE.__name__}.md', 'w') as doc_file:
    #     document_module(MODULE, MODULE.__name__, file=doc_file)
    # pprint.pprint(filter_members(pygameplus.Painter))
    with open(f'{DOCS_DIR}{DOCS_SUBDIR}pygameplus.Painter.md', 'w') as doc_file:
        document_class(pygameplus.Painter, 'Painter', 'pygameplus', file=doc_file)
