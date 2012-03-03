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

from ckip import CKIPSegmenter, CKIPParser

# Helper function to traverse all leaf node of the given tree root
def traverse(root):
    if 'child' in root:
        for child in root['child']:
            for leaf in traverse(child):
                yield leaf
    else:
        yield root

# Usage example of the CKIPSegmenter class
segmenter = CKIPSegmenter('YOUR USERNAME', 'YOUR PASSWORD')
result = segmenter.process(u'這是一隻可愛的小花貓')
if result['status_code'] != '0':
    print 'Process Failure: ' + result['status']

for sentence in result['result']:
    for term in sentence:
        print term['term'], term['pos']

# Usage example of the CKIPParser class
parser = CKIPParser('YOUR USERNAME', 'YOUR PASSWORD')
result = parser.process(u'這是一隻可愛的小花貓')
if result['status_code'] != '0':
    print 'Process Failure: ' + result['status']

for sentence in result['result']:
    for term in traverse(sentence['tree']):
        print term['term'], term['pos']

