# -*- coding: utf-8 -*-

from ckip import CKIPClient

client = CKIPClient('YOUR USERNAME', 'YOUR PASSWORD')
result = client.segment_text(u'這是一隻可愛的小花貓')
for sentence in result['result']:
    for (term, pos) in sentence:
        print term, pos

