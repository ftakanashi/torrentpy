# -*- coding:utf-8 -*-

import argparse
import logging
import os
import uuid

from torrentpy.models import Torrent

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s][%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def _uuid():    # Currently, the default method of modification is a random uuid.
    return str(uuid.uuid4())

def blur_torrent(t, opt):
    t_data = t.get_data()

    if opt.comment:
        nise_comment = _uuid()
        if 'comment' in t_data:
            t_data['comment'] = nise_comment
        if 'comment.utf-8' in t_data:
            t_data['comment.utf-8'] = nise_comment

    t_info = t_data['info']

    if 'files' not in t_info:
        # single file torrent
        _, ext = os.path.splitext(t_info['name'])
        nise_fn = _uuid() + ext
        t_info['name'] = nise_fn

    else:
        logging.info('{} Files in torrent found.'.format(len(t_info['files'])))
        for fi in t_info['files']:
            _t = []
            if 'path' in fi:
                for p in fi['path']:
                    _, ext = os.path.splitext(p)
                    if ext == '':
                        _t.append(_uuid())
                    else:
                        _t.append(_uuid() + ext)
                fi['path'] = _t
            if 'path.utf-8' in fi:
                fi['path.utf-8'] = _t

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