# CKIP.py

**CKIP.py** is a simple interface for the services provided by [CKIP](http://ckip.iis.sinica.edu.tw/CKIP/index.htm).

## Usage

**CKIP.py** provides two classes, `CKIPSegmenter` and `CKIPParser`, to access the [Chinese segmenter](http://ckipsvr.iis.sinica.edu.tw/) and the [Chinese parser](http://parser.iis.sinica.edu.tw/), respectively.

To create an instance of these classes, you must import the `CKIPSegmenter` class and/or the `CKIPParser` class from the `ckip` module, and then pass your username and password to the constructor:

    from ckip import CKIPSegmenter, CKIPParser

    segmenter = CKIPSegmenter('YOUR USERNAME', 'YOUR PASSWORD')
    parser = CKIPParser('YOUR USERNAME', 'YOUR PASSWORD')

Then, you can use the `process()` method to process the given string:

    segmented_result = segmenter.process(u'這是一隻可愛的小花貓')

or

    parsed_result = parser.process(u'這是一隻可愛的小花貓')

This method returns a dictionary of the processed result:

    {
        'status': 'Success',
        'status_code': '0',
        'result':
            [
                [
                    {'term': u'這', 'pos': u'DET'},
                    {'term': u'是', 'pos': u'Vt'},
                    {'term': u'一', 'pos': u'DET'},
                    {'term': u'隻', 'pos': u'M'},
                    {'term': u'可愛', 'pos': u'Vi'},
                    {'term': u'的', 'pos': u'T'},
                    {'term': u'小', 'pos': u'Vi'},
                    {'term': u'花貓', 'pos': u'N'}
                ]
            ]
    }

The `status` and the `status_code` indicate whether the process is success or not:

    if segmented_result['status_code'] != '0':
        print 'Process Failed: ' + segmented_result['status']

And the `result` is the a list of objects that represent each sentence.

Takes the result of the `CKIPSegmenter.process()` for example, the sentence is represented by a list of dictionary. Each dictionary contains the Chinese term and the corresponding part-of-speech:

    for sentence in segmented_result['result']:
        for term in sentence:
            print term['term'], term['pos']

The sentence in the result of the `CKIPParser.process()`, on the other hand, is represented by a parsing tree:

    {
        'punctuation': None,
        'tree':
            {
                'pos': u'S',
                'child':
                    [
                        {
                            'pos': u'NP',
                            'child':
                                [
                                    {'term': u'這', 'pos': u'DET'}
                                ]
                        },
                        {'term': u'是', 'pos': u'Vt'},
                        {
                            'pos': u'NP',
                            'child':
                                 [
                                     {'term': u'一隻', 'pos': u'DM'},
                                     {
                                         'pos': u'V‧的',
                                         'child':
                                             [
                                                 {'term': u'可愛', 'pos': u'Vi'},
                                                 {'term': u'的', 'pos': u'T'}
                                             ]
                                     },
                                     {'term': u'小', 'pos': u'Vi'},
                                     {'term': u'花貓', 'pos': u'N'}
                                 ]
                        }
                    ]
            }
    }

The `punctuation` is the punctuation that used to separate from other sentences.

`tree` is a dictionary that represent the tree structure. Each node has its own part-of-speech, and its children nodes (if this node is an internal node) or term (if this node is a leaf node).

Here is a simple example for traversing all leaf nodes (each of these is a Chinese term) of the parsing tree:

    def traverse(node):
        if 'child' in node:
            for child in node['child']:
                for leaf in traverse(child):
                    yield leaf
        else:
            yield node

    for sentence in result['result']:
        for term in traverse(sentence['tree']):
            print term['term'], term['pos']

## License

This project is [BSD-licensed](http://www.opensource.org/licenses/BSD-3-Clause). See LICENSE file for more detail.
