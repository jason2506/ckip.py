# -*- coding: utf-8 -*-

from contextlib import closing
from re import compile
from socket import socket, AF_INET, SOCK_STREAM

from lxml.etree import tostring, fromstring
from lxml.builder import E

class CKIPClient(object):
    __SERVER_IP = '140.109.19.104'
    __SERVER_PORT = 1501
    __BUFFER_SIZE = 4096
    __ENCODING = 'big5'

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
            s.connect((self.__SERVER_IP, self.__SERVER_PORT))
            s.sendall(msg)

            result = ''
            done = False
            while not done:
                chunk = s.recv(self.__BUFFER_SIZE)
                result += chunk
                done = result.find('</wordsegmentation>') > -1

        return result

    def __extract_terms(self, sentence):
        pattern = compile('^(.*)\(([^(]+)\)$')
        raw_terms = sentence.split()

        terms = []
        for raw_term in raw_terms:
            match = pattern.match(raw_term)
            term = (match.group(1), match.group(2))
            terms.append(term)

        return terms

    def segment_text(self, text):
        tree = self.__build_request_xml(text)
        msg = tostring(tree, encoding=self.__ENCODING, xml_declaration=True)

        result_msg = self.__send_and_recv(msg)
        result_tree = fromstring(result_msg.decode(self.__ENCODING))

        status = result_tree.find('./processstatus')
        sentences = result_tree.iterfind('./result/sentence')
        result = {
            'status': status.text,
            'status_code': status.get('code'),
            'result': [self.__extract_terms(sentence.text)
                for sentence in sentences]
        }

        return result

