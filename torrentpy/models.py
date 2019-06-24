# -*- coding:utf-8 -*-

import os
import re

from utils import TorrentPyException

class Torrent(object):
    def __init__(self, fn):
        if not os.path.isfile(fn):
            raise TorrentPyException('File {} not found'.format(fn))

        with open(fn, 'rb') as f:
            self.raw = f.read()    # a stack like string. processed bytes will be discarded from left end.

        if self.raw[0] != 'd' or self.raw[-1] != 'e':
            raise TorrentPyException('Invalid format of file {}. Should be a bencode dictionary.'.format(fn))

        self.load()
        self.dump_raw = ''

    def get_data(self):
        return self._data

    def load(self):
        self._data = self.load_proxy()

    def load_proxy(self):
        '''
        load an object out of the string read from the torrent file.
         It is a recursive method and will return a dictionary representing the whole torrent file at the top level.
        '''
        flag = self.raw[0]
        if flag == 'd':
            self.raw = self.raw[1:]
            _tmp = {}
            while self.raw[0] != 'e':
                k = self._find_string()
                v = self.load_proxy()
                _tmp[k] = v
            self.raw = self.raw[1:]
            return _tmp

        elif flag == 'l':
            self.raw = self.raw[1:]
            _tmp = []
            while self.raw[0] != 'e':
                v = self.load_proxy()
                _tmp.append(v)
            self.raw = self.raw[1:]
            return _tmp

        elif flag == 'i':
            m = re.search('i(\d+?)e', self.raw)
            try:
                v_str = m.group(1)
                v = int(v_str)
                v_len = len(v_str)
            except Exception as e:
                raise TorrentPyException('invalid integer format at header {}'.format(self.raw))
            else:
                self.raw = self.raw[v_len+2:]
                return v

        else:
            return self._find_string()

    def _find_string(self):
        '''

        '''
        first_column = self.raw.find(':')
        if first_column < 0:
            raise TorrentPyException('Cannot specify any column from {}'.format(self.raw))
        try:
            int_cols = int(self.raw[:first_column])
        except ValueError as e:
            raise TorrentPyException('Invalid integer format at head {}'.format(self.raw[first_column]))
        info_s = first_column + 1
        info_e = info_s + int_cols

        _string = self.raw[info_s:info_e]
        self.raw = self.raw[info_e:]
        return _string

    def dump(self, fn):
        '''
        :param fn: dump path of the file
        '''
        with open(fn, 'wb') as f:
            content = self.dump_proxy(self._data)
            f.write(content)

    def dump_proxy(self, obj):
        '''
        It is a recursive method to dump all information in a object.
        At the top level, the objects must be a dictionary representing the whole torrent file.
        :param obj:  object to dump
        '''

        if type(obj) is dict:
            _tmp = 'd'
            for key in sorted(obj):
                if type(key) is not str:
                    raise TorrentPyException('Key {} must be string.'.format(key))
                value = obj[key]
                _tmp += '{}:{}'.format(len(key), key)
                _tmp += self.dump_proxy(value)
            _tmp += 'e'
            return _tmp

        elif type(obj) is int:
            return 'i{}e'.format(obj)

        elif type(obj) is list:
            _tmp = 'l'
            for item in obj:
                _tmp += self.dump_proxy(item)
            _tmp += 'e'
            return _tmp

        elif type(obj) is str:
            return '{}:{}'.format(len(obj), obj)