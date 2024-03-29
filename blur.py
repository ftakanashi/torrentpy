# -*- coding:utf-8 -*-

import argparse
import logging
import os

from torrentpy.models import Torrent
from torrentpy.utils import blur_torrent

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s][%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    args = argparse.ArgumentParser()

    args.add_argument('-s', '--source', help='Path of the source torrent file.')
    args.add_argument('-o', '--output', help='Output path of the modified torrent file.')

    args.add_argument('-comment', action='store_true', default=False,
                      help='Blur the comment information in torrent file.')

    opt = args.parse_args()

    if opt.source is None:
        logging.error('Please Input a Source Path.')
        return
    else:
        opt.source = os.path.abspath(opt.source)

    if not os.path.isfile(opt.source):
        logging.error('File {} does not exist.'.format(opt.source))
        return

    if opt.output is None or os.path.isdir(opt.output):
        if opt.output is None:
            logging.warning('Output path not specified. Will adapt to the source directory.')
            dir_fn = os.path.dirname(opt.source)
        else:
            dir_fn = opt.output

        base_fn = os.path.splitext(os.path.basename(opt.source))[0]
        opt.output = os.path.join(dir_fn, '{}-modified.torrent'.format(base_fn))

    if os.path.isfile(opt.output):
        flag = raw_input('File {} already exists. Overwrite?(y/n)'.format(opt.output))
        if flag != 'y':
            logging.error('File {} already exists. Please try another path.'.format(opt.output))
            return

    t = Torrent(opt.source)
    blur_torrent(t, opt)
    t.dump(opt.output)

if __name__ == '__main__':
    main()