# -*- coding:utf-8 -*-

import logging
import os
import uuid

class TorrentPyException(Exception):
    pass

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

    # single-file torrent
    nise_fn = None
    if 'name' in t_info:
        _, ext = os.path.splitext(t_info['name'])
        nise_fn = _uuid() + ext
        t_info['name'] = nise_fn
    if 'name.utf-8' in t_info:
        if nise_fn is None:
            nise_fn = _uuid() + os.path.splitext(t_info['name.utf-8'])[1]
        t_info['name.utf-8'] = nise_fn

    # multiple-file torrent
    if 'files' in t_info:
        logging.info('{} Files in torrent found.'.format(len(t_info['files'])))

        # collect all the possible filenames in all file paths.
        # In first edition, I found that file records in modified torrent are far more than the original one.
        # Then i realized that the parent directory uuids are different(randomly generated respectively)
        # for two files under the same directory. To keep files under same directory are still together after modification
        # it is necessary to have a matching map between the original directory names and the modified one.
        fn_map = {}
        for fi in t_info['files']:
            for k in ('path', 'path.utf-8'):
                if k in fi:
                    for p in fi[k]:
                        if p not in fn_map: fn_map[p] = _uuid() + os.path.splitext(p)[1]


        for fi in t_info['files']:
            _t = []
            if 'path' in fi:
                for p in fi['path']:
                    _t.append(fn_map[p])
                fi['path'] = _t
            if 'path.utf-8' in fi:
                fi['path.utf-8'] = _t