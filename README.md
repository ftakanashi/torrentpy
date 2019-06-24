TorrentPy is a simple library that helps to load/dump information from BT torrent files.

>All codes are written in Python 2.7.
Basically, it only requires some built-in modules of Python, so that no third-party library installations are needed.

Some of the BT downloading applications in China are widely known that they will examine the content of the torrent file.
So that they could refuse to offer some download boosting service depending on the specific content.

One way to avoid being examined is modifying the content by yourself, pretending that our content is "green".

I've prepared the script blur.py which can easily helps modifying the content of a torrent file. The usage is like:

```
python blur.py -s /path/to/file.torrent -o /output/path/to/file.torrent -comment
```
which means the script will read information from /path/to/file.torrent and modify it with random uuid.
Then the modified content will be saved to /output/path/to/file.torrent. Argument '-comment' exploit the script to modify comment information of the torrent as well.

The little project is still being improved. Any comments or suggestions are welcomed.