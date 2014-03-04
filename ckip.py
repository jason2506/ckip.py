# -*- coding: utf-8 -*-

#################################################
# ckip.py
# ckip.py
#
# Copyright (c) 2012-2014, Chi-En Wu
# Distributed under The BSD 3-Clause License
#################################################

from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod
from contextlib import closing
from re import compile
from socket import socket, AF_INET, SOCK_STREAM

from lxml.etree import tostring, fromstring
from lxml.builder import E


def _construct_parsing_tree(tree_text):
    parent_node = None
    current_node = {}

    node_queue = []
    text = ''
    is_head = False
    for char in tree_text:
        if char == '(':
            node_queue.append(parent_node)

            current_node['child'] = []
            current_node['pos'] = text
            text = ''

            parent_node = current_node
            current_node = {}

        elif char == ')':
            if is_head:
                parent_node['head'] = current_node
                is_head = False

            if len(text) > 0:
                current_node['term'] = text
                text = ''

            parent_node['child'].append(current_node)

            if is_head:
                parent_node['head'] = current_node
                is_head = False

            current_node = parent_node
            parent_node = node_queue.pop()

        elif char == ':':
            if text == 'Head':
                is_head = True
            else:
                current_node['pos'] = text

            text = ''

        elif char == '|':
            if is_head:
                parent_node['head'] = current_node
                is_head = False

            if len(text) > 0:
                current_node['term'] = text
                text = ''

            parent_node['child'].append(current_node)
            current_node = {}

        else:
            text += char

    return current_node


class CKIPClient(object):
    __metaclass__ = ABCMeta

    _BUFFER_SIZE = 4096
    _ENCODING = 'big5'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __build_request_xml(self, text):
        return E.wordsegmentation(
            E.option(showcategory='1'),
            E.authentication(username=self.username, password=self.password),
            E.text(text),
            version='0.1')

    def __send_and_recv(self, msg):
        with closing(socket(AF_INET, SOCK_STREAM)) as s:
            s.connect((self._SERVER_IP, self._SERVER_PORT))
            s.sendall(msg)

            result = ''
            done = False
            while not done:
                chunk = s.recv(self._BUFFER_SIZE)
                result += chunk.decode(self._ENCODING)
                done = result.find('</wordsegmentation>') > -1

        return result

    @abstractmethod
    def _extract_sentence(self, sentence):
        raise NotImplementedError()

    def process(self, text):
        tree = self.__build_request_xml(text)
        msg = tostring(tree, encoding=self._ENCODING, xml_declaration=True)

        result_msg = self.__send_and_recv(msg)
        result_tree = fromstring(result_msg)

        status = result_tree.find('./processstatus')
        sentences = result_tree.iterfind('./result/sentence')
        result = {
            'status': status.text,
            'status_code': status.get('code'),
            'result': [self._extract_sentence(sentence.text)
                       for sentence in sentences]
        }

        return result


class CKIPSegmenter(CKIPClient):
    _SERVER_IP = '140.109.19.104'
    _SERVER_PORT = 1501

    def _extract_sentence(self, sentence):
        pattern = compile('^(.*)\(([^(]+)\)$')
        raw_terms = sentence.split()

        terms = []
        for raw_term in raw_terms:
            match = pattern.match(raw_term)
            term = {
                'term': match.group(1),
                'pos': match.group(2)
            }

            terms.append(term)

        return terms


class CKIPParser(CKIPClient):
    _SERVER_IP = '140.109.19.112'
    _SERVER_PORT = 8000

    def _extract_sentence(self, sentence):
        pattern = compile('^#\d+:1\.\[0\] (.+)#(.*)$')
        match = pattern.match(sentence)

        tree_text = match.group(1)
        tree = _construct_parsing_tree(tree_text)

        raw_punctuation = match.group(2)
        punctuation = None
        if len(raw_punctuation) > 0:
            pattern = compile('^(.*)\(([^(]+)\)$')
            match = pattern.match(raw_punctuation)
            punctuation = {
                'term': match.group(1),
                'pos': match.group(2)
            }

        result = {
            'tree': tree,
            'punctuation': punctuation
        }

        return result
