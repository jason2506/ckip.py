# -*- coding: utf-8 -*-
#
# Copyright (c) 2012, Chi-En Wu
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the organization nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from abc import ABCMeta, abstractmethod
from contextlib import closing
from re import compile
from socket import socket, AF_INET, SOCK_STREAM

from lxml.etree import tostring, fromstring
from lxml.builder import E

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
                result += chunk
                done = result.find('</wordsegmentation>') > -1

        return result

    @abstractmethod
    def _extract_terms(self, sentence):
        raise NotImplementedError()

    def process(self, text):
        tree = self.__build_request_xml(text)
        msg = tostring(tree, encoding=self._ENCODING, xml_declaration=True)

        result_msg = self.__send_and_recv(msg)
        result_tree = fromstring(result_msg.decode(self._ENCODING))

        status = result_tree.find('./processstatus')
        sentences = result_tree.iterfind('./result/sentence')
        result = {
            'status': status.text,
            'status_code': status.get('code'),
            'result': [self._extract_terms(sentence.text)
                for sentence in sentences]
        }

        return result

class CKIPSegmenter(CKIPClient):
    _SERVER_IP = '140.109.19.104'
    _SERVER_PORT = 1501

    def _extract_terms(self, sentence):
        pattern = compile('^(.*)\(([^(]+)\)$')
        raw_terms = sentence.split()

        terms = []
        for raw_term in raw_terms:
            match = pattern.match(raw_term)
            term = (match.group(1), match.group(2))
            terms.append(term)

        return terms

