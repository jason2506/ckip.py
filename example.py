# -*- coding: utf-8 -*-

#################################################
# example.py
# ckip.py
#
# Copyright (c) 2012-2014, Chi-En Wu
# Distributed under The BSD 3-Clause License
#################################################

from __future__ import unicode_literals, print_function

from ckip import CKIPSegmenter, CKIPParser


def traverse(root):
    """Helper function to traverse all leaf nodes of the given tree root."""
    if 'child' in root:
        for child in root['child']:
            for leaf in traverse(child):
                yield leaf
    else:
        yield root


# Usage example of the CKIPSegmenter class
segmenter = CKIPSegmenter('YOUR USERNAME', 'YOUR PASSWORD')
result = segmenter.process('這是一隻可愛的小花貓')
if result['status_code'] != '0':
    print('Process Failure: ' + result['status'])

for sentence in result['result']:
    for term in sentence:
        print(term['term'], term['pos'])


# Usage example of the CKIPParser class
parser = CKIPParser('YOUR USERNAME', 'YOUR PASSWORD')
result = parser.process('這是一隻可愛的小花貓')
if result['status_code'] != '0':
    print('Process Failure: ' + result['status'])

for sentence in result['result']:
    for term in traverse(sentence['tree']):
        print(term['term'], term['pos'])
