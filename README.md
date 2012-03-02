# CKIP.py

**CKIP.py** is a simple interface for the services provided by [CKIP](http://ckip.iis.sinica.edu.tw/CKIP/index.htm).

## Usage

To access the [Chinese segmentation service](http://ckipsvr.iis.sinica.edu.tw/), you must import the `CKIPSegmenter` class from the `ckip` module, and create a segmenter by passing your username and password:

    from ckip import CKIPSegmenter
    segmenter = CKIPSegmenter('YOUR USERNAME', 'YOUR PASSWORD')

Then, you can use the `process()` method to segment the given text:

    result = segmenter.process(u'這是一隻可愛的小花貓')
    for sentence in result['result']:
        for term in sentence:
            print term['term'], term['pos']

Another supported service is the [CKIP Chinese parser](http://parser.iis.sinica.edu.tw/).

Like the usage example of the `CKIPSegmenter` class, you must import the `CKIPParser` class from the `ckip` module, create a parser, and use the `process()` method to parse the given text:

    from ckip import CKIPParser

    def traverse(node):
        if 'child' in node:
            for child in node['child']:
                for leaf in traverse(child):
                    yield leaf
        else:
            yield node

    parser = CKIPParser('YOUR USERNAME', 'YOUR PASSWORD')
    result = parser.process(u'這是一隻可愛的小花貓')
    for sentence in result['result']:
        for term in traverse(sentence['tree']):
            print term['term'], term['pos']

## License

This project is [BSD-licensed](http://www.opensource.org/licenses/BSD-3-Clause). See LICENSE file for more detail.
