#!/usr/bin/env python
# -*- coding:utf-8 -*-
INDEX_DIR = "IndexFiles.index"

# import sys
# import os
# import json
import jieba
import utils

import nltk
import nltk.stem.porter as pt

import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause


def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def get_stem(doc):
    res = ""
    stemmer = pt.PorterStemmer()
    token = nltk.word_tokenize(doc)
    for t in token:
        if t.isalpha():
            stem = stemmer.stem(t)
            res = res + stem + " "
    return res


class ModernPoemSearcher(object):
    def __init__(self, folder='modern_index'):
        self.chSearcher = IndexSearcher(DirectoryReader.open(SimpleFSDirectory(File(folder+'/chinese'))))
        self.enSearcher = IndexSearcher(DirectoryReader.open(SimpleFSDirectory(File(folder+'/english'))))
        self.Analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)

    def ch_seach(self, command_dict, target_range=None,
                 targets=('title', 'author', 'text', 'likes', 'imgurl', 'label')):
        res = []

        querys = BooleanQuery()
        for key, value in command_dict.items():
            if key not in ['author', 'title', 'label', 'content']:
                continue
            query = QueryParser(Version.LUCENE_CURRENT, key, self.Analyzer).parse(utils.jieba_seg(value[0]))
            if value[1]:
                querys.add(query, BooleanClause.Occur.MUST)
            else:
                querys.add(query, BooleanClause.Occur.SHOULD)
        totalDocs = self.chSearcher.search(querys, utils.MAX_RESULTS).scoreDocs

        total_match = len(totalDocs)
        if target_range is None:
            scoreDocs = totalDocs[:]
        else:
            scoreDocs = totalDocs[max(0, int(target_range[0])):min(total_match, int(target_range[1]))]
        del totalDocs

        for i, scoreDoc in enumerate(scoreDocs):
            doc = self.chSearcher.doc(scoreDoc.doc)
            res.append({key: doc.get(key) for key in targets})

        return total_match, res

    # def search(self, command, type):
    #     # type all title author content
    #     if command == '':
    #         return
    #     data = []
    #     if not command.isalpha():
    #         # segmentation
    #         content = command
    #         try:
    #             seg_list = jieba.cut(content)
    #             content = ' '.join(seg_list)
    #         except:
    #             # print 'segmentation failed'
    #             pass
    #         # booleanQuery
    #         querys = BooleanQuery()
    #         if type == 'title':
    #             query = QueryParser(Version.LUCENE_CURRENT, 'title', self.Analyzer).parse(content)
    #             querys.add(query, BooleanClause.Occur.MUST)
    #         elif type == 'author':
    #             query = QueryParser(Version.LUCENE_CURRENT, 'author', self.Analyzer).parse(content)
    #             querys.add(query, BooleanClause.Occur.MUST)
    #         elif type == 'content':
    #             query = QueryParser(Version.LUCENE_CURRENT, 'content', self.Analyzer).parse(content)
    #             querys.add(query, BooleanClause.Occur.MUST)
    #         else:
    #             query = QueryParser(Version.LUCENE_CURRENT, 'title', self.Analyzer).parse(content)
    #             querys.add(query, BooleanClause.Occur.SHOULD)
    #             query = QueryParser(Version.LUCENE_CURRENT, 'content', self.Analyzer).parse(content)
    #             querys.add(query, BooleanClause.Occur.SHOULD)
    #             query = QueryParser(Version.LUCENE_CURRENT, 'author', self.Analyzer).parse(content)
    #             querys.add(query, BooleanClause.Occur.SHOULD)
    #         scoreDocs = self.chSearcher.search(querys, 200).scoreDocs
    #         # print "%s total matching documents." % len(scoreDocs)
    #
    #         for i, scoreDoc in enumerate(scoreDocs):
    #             doc = self.chSearcher.doc(scoreDoc.doc)
    #             item = {}
    #             item['title'] = doc.get('title')
    #             item['author'] = doc.get('author')
    #             item['text'] = doc.get('text')
    #             item['img'] = doc.get('img')
    #             item['likes'] = doc.get('likes')
    #             data.append(item)
    #         return len(scoreDocs), data
    #     else:
    #         content = get_stem(command)
    #         # booleanQuery
    #         querys = BooleanQuery()
    #         query = QueryParser(Version.LUCENE_CURRENT, 'content', self.Analyzer).parse(content)
    #         querys.add(query, BooleanClause.Occur.MUST)
    #         scoreDocs = self.enSearcher.search(querys, 200).scoreDocs
    #         print "%s total matching documents." % len(scoreDocs)
    #
    #         for i, scoreDoc in enumerate(scoreDocs):
    #             doc = self.enSearcher.doc(scoreDoc.doc)
    #             item = {}
    #             item['title'] = doc.get('title')
    #             item['author'] = doc.get('author')
    #             item['text'] = doc.get('text')
    #             item['img'] = doc.get('img')
    #             item['likes'] = doc.get('likes')
    #             data.append(item)
    #         return len(scoreDocs), data


# if __name__ == '__main__':
#     lucene.initVM(vmargs=['-Djava.awt.headless=true'])
#     print 'lucene', lucene.VERSION
#     # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
#     mps = ModernPoemSearcher()
#     print mps.search("flower光线", 'title')
