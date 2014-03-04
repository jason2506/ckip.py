# CKIP.py

**CKIP.py** is a simple interface for the services provided by [CKIP](http://ckip.iis.sinica.edu.tw/CKIP/index.htm).

## Usage

**CKIP.py** provides two classes, `CKIPSegmenter` and `CKIPParser`, to access the [Chinese segmenter](http://ckipsvr.iis.sinica.edu.tw/) and the [Chinese parser](http://parser.iis.sinica.edu.tw/), respectively.

To create an instance of these classes, you must import the `CKIPSegmenter` class and/or the `CKIPParser` class from the `ckip` module, and then pass your username and password to the constructor:

```python
from ckip import CKIPSegmenter, CKIPParser

segmenter = CKIPSegmenter('YOUR USERNAME', 'YOUR PASSWORD')
parser = CKIPParser('YOUR USERNAME', 'YOUR PASSWORD')
```

Then, you can use the `process()` method to process the given string:

```python
segmented_result = segmenter.process('這是一隻可愛的小花貓')
```

or

```python
parsed_result = parser.process('這是一隻可愛的小花貓')
```

This method returns a dictionary of the processed result:

```python
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
```

The `status` and the `status_code` indicate whether the process is success or not:

```python
if segmented_result['status_code'] != '0':
    print('Process Failed: ' + segmented_result['status'])
```

And the `result` is a list of objects that represent each sentence.

Takes the result of the `CKIPSegmenter.process()` for example, the sentence is represented by a list of dictionary. Each dictionary contains the Chinese term and the corresponding part-of-speech:

```python
for sentence in segmented_result['result']:
    for term in sentence:
        print(term['term'], term['pos'])
```

The sentence in the result of the `CKIPParser.process()`, on the other hand, is represented by a parsing tree:

```python
{
    'punctuation': None,
    'tree':
        {
            'head': {'term': u'是', 'pos': u'Vt'},
            'pos': u'S',
            'child':
                [
                    {
                        'head': {'term': u'這', 'pos': u'DET'},
                        'pos': u'NP',
                        'child':
                            [
                                {'term': u'這', 'pos': u'DET'}
                            ]
                    },
                    {'term': u'是', 'pos': u'Vt'},
                    {
                        'head': {'term': u'花貓', 'pos': u'N'},
                        'pos': u'NP',
                        'child':
                             [
                                 {'term': u'一隻', 'pos': u'DM'},
                                 {
                                     'head': {'term': u'的', 'pos': u'T'},
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
```

The `punctuation` is a dictionary like `{'term': u'。', 'pos': u'PERIODCATEGORY'}`, which represents the symbol that used to separate from next sentence, or `None` if there was no punctuation in this sentence.

`tree` is a dictionary that represent the tree structure. Each node has its own part-of-speech, and its children nodes (if this node is an internal node) or term (if this node is a leaf node).

Here is a simple example for traversing all leaf nodes (each of these is a Chinese term) of the parsing tree:

```python
def traverse(root):
    if 'child' in root:
        for child in root['child']:
            for leaf in traverse(child):
                yield leaf
    else:
        yield root

for sentence in parsed_result['result']:
    for term in traverse(sentence['tree']):
        print(term['term'], term['pos'])
```

## License

Copyright (c) 2012-2014, Chi-En Wu.

Distributed under [The BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause).
