# CKIP.py

**CKIP.py** is a simple interface for the Chinese segmentation service that provided by [CKIP](http://ckip.iis.sinica.edu.tw/CKIP/index.htm).

To access the Chinese segmentation service, you must [register first](http://ckipsvr.iis.sinica.edu.tw/reg.php).

## Usage

    from ckip import CKIPChineseSegmenter

    client = CKIPChineseSegmenter('YOUR USERNAME', 'YOUR PASSWORD')
    result = client.segment_text(u'這是一隻可愛的小花貓')
    for sentence in result['result']:
        for (term, pos) in sentence:
            print term, pos

## License

This project is [BSD-licensed](http://www.opensource.org/licenses/BSD-3-Clause). See LICENSE file for more detail.
