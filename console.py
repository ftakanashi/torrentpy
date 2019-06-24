# -*- coding:utf-8 -*-

import collections
import logging
import os
import sys
reload(sys)
sys.setdefaultencoding('gb18030')

from torrentpy.models import Torrent
from torrentpy.utils import blur_torrent

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s][%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def _exit():
    raw_input(u'按回车退出...')
    sys.exit(1)

def main():
    pwd = os.getcwd()

    source = raw_input(u'请输入要修改的种子名(回车确认): ')
    source = os.path.abspath(source)
    if not os.path.isfile(source):
        logging.error(u'文件 {} 不存在'.format(source))
        _exit()

    base_fn = os.path.splitext(os.path.basename(source))[0]

    t = Torrent(source)
    Opt = collections.namedtuple('Option', ['comment'])
    opt = Opt(comment=True)
    blur_torrent(t, opt)
    new_fn = os.path.join(pwd, '{}-modified.torrent'.format(base_fn))
    t.dump(new_fn)

    logging.info(u'已经完成修改')
    _exit()

if __name__ == '__main__':
    main()