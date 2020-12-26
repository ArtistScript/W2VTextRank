#-*- encoding:utf-8 -*-
import jieba
import math
from string import punctuation
from heapq import nlargest
from itertools import product, count
from gensim.models import Word2Vec
from FastTextRank import util
import numpy as np
import os
from itertools import count
import codecs

class FastTextRank4Word(object):
    def __init__(self,use_stopword=False,stop_words_file=None,max_iter=100,tol=0.0001,window=2):
        """
        :param max_iter: 最大的迭代轮次
        :param tol: 最大的容忍误差
        :param window: 词语窗口
        :return:
        """
        self.__use_stopword = use_stopword
        self.__max_iter = max_iter
        self.__tol = tol
        self.__window = window
        self.__stop_words = set()
        self.__stop_words_file = self.get_default_stop_words_file()
        self.__sentences = [] # original segged sentences
        if type(stop_words_file) is str:
            self.__stop_words_file = stop_words_file
        if use_stopword:
            for word in codecs.open(self.__stop_words_file, 'r', 'utf-8', 'ignore'):
                self.__stop_words.add(word.strip())
        # Print a RuntimeWarning for all types of floating-point errors
        np.seterr(all='warn')

    def get_default_stop_words_file(self):
        d = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(d, 'stopwords.txt')

    def build_worddict(self,sents):
        """
        构建字典，是词语和下标之间生成一对一的联系，为之后的词图构建做准备
        :param sents:
        :return:
        """
        word_index = {}
        index_word = {}
        words_number = 0
        for word_list in sents:
            for word in word_list:
                if not word in word_index:
                    word_index[word] = words_number
                    index_word[words_number] = word
                    words_number += 1
        return word_index,index_word,words_number

    def build_word_grah(self,sents,words_number,word_index,window=2):
        graph = [[0.0 for _ in range(words_number)] for _ in range(words_number)]
        for word_list in sents:
            for w1, w2 in util.combine(word_list, window):
                if w1 in word_index and w2 in word_index:
                    index1 = word_index[w1]
                    index2 = word_index[w2]
                    graph[index1][index2] += 1.0
                    graph[index2][index1] += 1.0
        return graph

    def get_keywords(self, text, keywords_num = None):
        self.text = text #original raw text
        # text = text.replace('\n', '')
        # text = text.replace('\r', '')
        text = util.as_text(text)#处理编码问题
        sentences=util.cut_sentences(text)# this text here means a full text content ; all in one line
        #sentences用于记录已分词文章最原本的句子，wordlist_sents用于提取关键词
        sentences,wordlist_sents=util.psegcut_filter_words(sentences, self.__stop_words, self.__use_stopword)

        self.__sentences = sentences

        word_index, index_word, words_number=self.build_worddict(wordlist_sents)
        graph=self.build_word_grah(wordlist_sents,words_number,word_index,window=self.__window)
        scores = util.weight_map_rank(graph,max_iter=self.__max_iter,tol=self.__tol)
        if keywords_num is None:
            keywords_num = int(words_number/3)
            keywords_selected = nlargest(keywords_num, zip(scores, count()))
        else:
            keywords_selected = nlargest(keywords_num, zip(scores, count()))

        return [(index_word[item[1]],item[0]) for item in keywords_selected]# item: [(score,word_index) list]

    def get_keyphrases(self, text, keywords_num, min_occur_num = 2):
        """获取关键短语。
        获取 keywords_num 个关键词构造的可能出现的短语。

        Return:
        关键短语的列表。
        """
        keywords_set = set([item[0] for item in self.get_keywords(text, keywords_num)])
        keyphrases = set()
        for sentence in self.__sentences:
            one = []
            for word in sentence:
                if word in keywords_set:
                    one.append(word)
                else:
                    if len(one) >  1:
                        keyphrases.add(''.join(one))
                    if len(one) == 0:
                        continue
                    else:
                        one = []
            # 兜底
            if len(one) >  1:
                keyphrases.add(''.join(one))

        return [phrase for phrase in keyphrases
                if self.text.count(phrase) >= min_occur_num]

    def get_keyphrases_according_to_keywords(self, keywords, min_occur_num = 2):
        """根据关键词获取关键短语。
        获取 keywords关键词构造的可能出现的短语。

        Return:
        关键短语的列表。
        """
        keywords_set = set(keywords)
        keyphrases = set()
        for sentence in self.__sentences:
            one = []
            for word in sentence:
                if word in keywords_set:
                    one.append(word)
                else:
                    if len(one) >  1:
                        keyphrases.add(''.join(one))
                    if len(one) == 0:
                        continue
                    else:
                        one = []
            # 兜底
            if len(one) >  1:
                keyphrases.add(''.join(one))

        return [phrase for phrase in keyphrases
                if self.text.count(phrase) >= min_occur_num]