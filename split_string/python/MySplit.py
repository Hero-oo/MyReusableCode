import os, sys

class MySplit(object):
    def __init__(self, dt):
        self.dt = dt
        self.max_len = max(len(w) for w in self.dt)  # 词最大长度，默认等于词典最长词
        self.total = sum(self.dt.values())  # 总频数

    '''
    词典匹配分词
    '''
    def dict_split(self, sentence):
        tail = len(sentence)
        words = []
        while tail > 0:
            head = max(tail - self.max_len, 0)
            for middle in range(head, tail - 1):  # 忽略长度为1的词
                word = sentence[middle: tail]
                if word in self.dt.keys():
                    # print(middle, tail - 1, word)
                    words.append(word)
                    tail = middle
                    break
            else:
                tail -= 1
                # print(tail, tail, sentence[tail])
                words.append(sentence[tail])
        # print(words[::-1])
        return words[::-1]
    
    '''
    正向最大匹配
    '''
    def _maximum_matching(self, sentence):
        length = len(sentence)
        head = 0
        while head < length:
            tail = min(head + self.max_len, length)
            for middle in range(tail, head + 1, -1):
                word = sentence[head: middle]
                if word in self.dt:
                    head = middle
                    break
            else:
                word = sentence[head]
                head += 1
            yield word

    def maximum_matching(self, sentence):
        return list(self._maximum_matching(sentence))

    '''
    逆向最大匹配
    '''
    def reverse_maximum_matching(self, sentence):
        length = len(sentence)
        words = []
        tail = length
        while tail > 0:
            head = min(tail - self.max_len, 0)
            for middle in range(head, tail - 1):
                word = sentence[middle: tail]
                if word in self.dt:
                    tail = middle
                    break
            else:
                tail -= 1
                word = sentence[tail]
            words.append(word)  # 比words.insert(0, word)快6%
        return words[::-1]

    '''
    贝叶斯网络
    '''
    def _probability(self, sentence):
        length = len(sentence)

        # get DAG
        DAG = dict()
        for head in range(length):
            DAG.update({head: [head]})
            tail = min(head + self.max_len, length)
            for middle in range(head + 2, tail + 1):
                word = sentence[head: middle]
                if word in self.dt:
                    DAG[head].append(middle - 1)
        # calculate route
        route = {}
        route[length] = (1, 1)
        for idx in range(length - 1, -1, -1):
            route[idx] = max(
                (self.dt.get(sentence[idx:x + 1], 0) / self.total * route[x + 1][0], x)
                for x in DAG[idx])
        # yield
        x = 0
        while x < length:
            y = route[x][1] + 1
            l_word = sentence[x:y]
            yield l_word
            x = y

    def probability(self, sentence):
        return list(self._probability(sentence))

'''
USE:

import MySplit as mySplit

splitdict = {'china': 1, 'vip': 1}
mysplit = mySplit.MySplit(splitdict)
sentence = 'chinavip1'
res = mysplit.dict_split(sentence)
print(res)  # res = ['china', 'vip', '1']
'''
