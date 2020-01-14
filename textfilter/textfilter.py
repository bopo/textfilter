# -*- coding:utf-8 -*-
import os
import re
from collections import defaultdict

__all__ = ['TextFilter']


class NaiveFilter:
    """
    Filter Messages from keywords

    very simple filter implementation

    >>> f = NaiveFilter()
    >>> f.add("sexy")
    >>> f.filter("hello sexy baby")
    hello **** baby
    """

    def __init__(self):
        self.keywords = set([])

    def parse(self, path):
        for keyword in open(path):
            self.keywords.add(keyword.strip())

    def filter(self, message, repl="*"):
        message = str(message)

        for kw in self.keywords:
            if kw:
                message = message.replace(kw, repl)

        return message

    def add(self, keyword):
        self.keywords.add(keyword.strip())


class BSFilter:
    """
    Filter Messages from keywords

    Use Back Sorted Mapping to reduce replacement times

    >>> f = BSFilter()
    >>> f.add("sexy")
    >>> f.filter("hello sexy baby")
    hello **** baby
    """

    def __init__(self):
        self.keywords = []
        self.kwsets = set([])
        self.bsdict = defaultdict(set)
        self.pat_en = re.compile(r'^[0-9a-zA-Z]+$')  # english phrase or not

    def add(self, keyword):
        """
        添加关键词
        :param keyword:
        :return:
        """
        if keyword is None:
            return None

        if not isinstance(keyword, str):
            keyword = keyword.decode('utf-8')

        keyword = keyword.lower()

        if keyword not in self.kwsets:
            self.keywords.append(keyword)
            self.kwsets.add(keyword)
            index = len(self.keywords) - 1

            for word in keyword.split():
                if self.pat_en.search(word):
                    self.bsdict[word].add(index)
                else:
                    for char in word:
                        self.bsdict[char].add(index)

    def parse(self, path):
        """
        解析字典
        :param path:
        :return:
        """
        with open(path, "r") as f:
            for keyword in f:
                self.add(keyword.strip())

    def filter(self, message, repl="*"):
        """
        过滤器
        :param message:
        :param repl:
        :return:
        """
        if not isinstance(message, str):
            message = message.decode('utf-8')

        message = message.lower()

        for word in message.split():
            if self.pat_en.search(word):
                for index in self.bsdict[word]:
                    message = message.replace(self.keywords[index], repl)
            else:
                for char in word:
                    for index in self.bsdict[char]:
                        message = message.replace(self.keywords[index], repl)
        return message


class DFAFilter:
    """
    Filter Messages from keywords

    Use DFA to keep algorithm perform constantly

    >>> f = DFAFilter()
    >>> f.add("sexy")
    >>> f.filter("hello sexy baby")
    hello **** baby
    """

    def __init__(self, path=None):
        self.keyword_chains = {}
        self.delimit = '\x00'

        if path:
            self.parse(path)

    def add(self, keyword):
        """
        添加关键字
        :param keyword:
        :return:
        """
        global last_level, last_char

        if keyword is None:
            return None

        if not isinstance(keyword, str):
            keyword = keyword.decode('utf-8')

        keyword = keyword.lower()
        chars = keyword.strip()

        if not chars:
            return

        level = self.keyword_chains

        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break

                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]

                last_level[last_char] = {self.delimit: 0}
                break

            if i == len(chars) - 1:
                level[self.delimit] = 0

    def parse(self, path):
        """
        解析字典
        :param path:
        :return:
        """
        with open(path) as f:
            for keyword in f:
                self.add(keyword.strip())

    def filter(self, message, repl="*"):
        """
        过滤器
        :param message:
        :param repl:
        :return:
        """
        if not isinstance(message, str):
            message = message.decode('utf-8')

        message = message.lower()
        ret = []
        start = 0

        while start < len(message):
            level = self.keyword_chains
            step_ins = 0

            for char in message[start:]:
                if char in level:
                    step_ins += 1

                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])

            start += 1

        return ''.join(ret)


class TextFilter:
    method = None
    dicts = 'keywords'

    def __init__(self, file=None, method=None):
        method = method if method in ('Naive', 'DFA', 'BS') else 'Naive'
        method = '{}Filter()'.format(method)
        dictdir = os.path.dirname(__file__)

        self.dicts = file if file is not None else os.path.join(dictdir, self.dicts)
        self.method = eval(method)
        self.method.parse(self.dicts)

    def filter(self, *args, **kwargs):
        return self.method.filter(*args)

    def add(self, *args, **kwargs):
        return self.method.add(*args)

# if __name__ == "__main__":
#     gfw = TextFilter(method='BS')
#     gfw.add('币')
#     gfw.add('世')
#
#     # gfw = NaiveFilter()
#     # gfw = BSFilter()
#     # gfw = DFAFilter("keywords")
#     # gfw.parse("keywords")
#
#     t = time.time()
#     print(gfw.filter("法轮功 我操操操", "*"))
#     print(gfw.filter("针孔摄像机 我操操操", "*"))
#     print(gfw.filter("售假人民币 我操操操", "*"))
#     print(gfw.filter("传世私服 我操操操", "*"))
#     print(time.time() - t)
