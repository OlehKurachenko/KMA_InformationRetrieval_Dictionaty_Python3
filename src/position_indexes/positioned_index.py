#
#   Created by Oleh Kurachenko
#          aka soll_nevermind aka okurache
#   on 2018-02-04T21:09:29Z as a part of KMA_InformationRetrieval_Dictionaty_Python3
#
#   copying code from GitHub doesn't make you smarter,
#   better ask me oleh.kurachenko@gmail.com , I'm ready to help
#
#   checkout my GitHub https://github.com/OlehKurachenko
#   rate, CV & contacts http://www.linkedin.com/in/oleh-kurachenko-6b025b111
#

from src.indexes.abs_binary_searcher import ABSBinarySearcher
from src.text_file_tokenizers.text_file_simplest_tokenizer import TestFileSimplestTokenizer

from re import split


class PositionInvertedIndex(ABSBinarySearcher):
    # TODO write documentation
    # TODO make pretty

    def __init__(self, target_files):
        self.__inverted_index = {}
        if type(target_files) == list:
            self.__files = list(target_files)
            for i, file in enumerate(target_files):
                words_gen = TestFileSimplestTokenizer(file).token_generator
                for j, word in enumerate(words_gen):
                    self.__inverted_index.setdefault(word, [])
                    ii_list = self.__inverted_index[word]
                    if not (ii_list and ii_list[-1][0] == i):
                        ii_list.append((i, []))
                    ii_list[-1][1].append(j)
        else:
            pass  # TODO load existing incidence matrix

    def export(self, filename):
        assert type(filename) == str, PositionInvertedIndex.__WRONG_ARGUMENT_TYPE

        file = open(filename, "w+")
        file.write(
            "re_im " + str(len(self.__inverted_index)) + " " + str(
                len(self.__files)))
        for filename in self.__files:
            file.write(" " + filename)
        file.write("\n")
        for key in self.__inverted_index.keys():
            file.write(key)
            for val in self.__inverted_index[key]:
                file.write("  " + str(val[0]))
                for val2 in val[1]:
                    file.write(" " + str(val2))
            file.write("\n")
        file.close()

    # TODO refactor
    def perform_request(self, request):
        assert type(request) == str, PositionInvertedIndex.__WRONG_ARGUMENT_TYPE

        strsplit = split("[ .,!?:;\"'\t\r\n\v\f]+", request)
        if len(strsplit) != 3:
            return False
        # noinspection PyBroadException
        distance = 0
        try:
            distance = int(strsplit[2])
        except Exception:
            return False
        # TODO move to another method
        i1 = 0
        i2 = 0
        l1 = self.__inverted_index[strsplit[0]]
        l2 = self.__inverted_index[strsplit[1]]
        res = []
        while (i1 < len(l1)) and (i2 < len(l2)):
            if l1[i1][0] == l2[i2][0]:
                j1 = 0
                j2 = 0
                while (j1 < len(l1[i1][1])) and (j2 < len(l2[i2][1])):
                    # TODO fix b b 1 => similar to non-zero
                    if abs(l1[i1][1][j1] - l2[i2][1][j2]) <= distance:
                        res.append(l1[i1][0])
                        break
                    elif l1[i1][1][j1] < l2[i2][1][j2]:
                        j1 += 1
                    else:
                        j2 += 1
                i1 += 1
                i2 += 1
            elif l1[i1][0] < l2[i2][0]:
                i1 += 1
            else:
                i2 += 1
        return res

        # request += ' '
        # words_list = []
        # operations_list = []
        # i = 0
        # is_value = True
        # while i < len(request):
        #     while i < len(request) and request[i] == ' ' :
        #         i += 1
        #     if i == len(request):
        #         break
        #     if request[i] == '(':
        #         operations_list.append('(')
        #         i += 1
        #     elif request[i] == ')':
        #         temp_opp = operations_list.pop()
        #         while temp_opp != '(':
        #             if temp_opp == 'or':
        #                 words_list.append(
        #                     PositionInvertedIndex.lists_merge(words_list.pop(), words_list.pop()))
        #             elif temp_opp == 'and':
        #                 words_list.append(
        #                     PositionInvertedIndex.lists_intersect(words_list.pop(),
        # words_list.pop()))
        #             else:
        #                 raise Exception
        #             temp_opp = operations_list.pop()
        #         i += 1
        #     else:
        #         j = i
        #         while request[j] != ' ':
        #             j += 1
        #         word = request[i:j]
        #         i = j
        #         if is_value:
        #             if word in self.__inverted_index:
        #                 words_list.append(self.__inverted_index[word])
        #             else:
        #                 words_list.append([])
        #         else:
        #             operations_list.append(word)
        #         is_value = not is_value
        # while operations_list:
        #     temp_opp = operations_list.pop()
        #     if temp_opp == 'or':
        #         words_list.append(
        #             PositionInvertedIndex.lists_merge(words_list.pop(), words_list.pop()))
        #     elif temp_opp == 'and':
        #         words_list.append(
        #             PositionInvertedIndex.lists_intersect(words_list.pop(), words_list.pop()))
        #     else:
        #         print(temp_opp)
        #         raise Exception
        # if len(words_list) != 1 or operations_list:
        #     raise Exception
        # res = []
        # for i in words_list.pop():
        #     res.append(self.__files[i])
        # return res

    # TODO create outher package for utill fucnitons
    @staticmethod
    def lists_merge(l1, l2):
        assert type(l1) == list, PositionInvertedIndex.__WRONG_ARGUMENT_TYPE
        assert type(l2) == list, PositionInvertedIndex.__WRONG_ARGUMENT_TYPE

        lr = []
        i1 = 0
        i2 = 0
        while i1 < len(l1) and i2 < len(l2):
            if l1[i1] == l2[i2]:
                lr.append(l1[i1])
                i1 += 1
                i2 += 1
            elif l1[i1] > l2[i2]:
                lr.append(l2[i2])
                i2 += 1
            else:
                lr.append(l1[i1])
                i1 += 1
        while i1 < len(l1):
            lr.append(l1[i1])
            i1 += 1
        while i2 < len(l2):
            lr.append(l2[i2])
            i2 += 1
        return lr

    # TODO create outher package for utill fucnitons
    @staticmethod
    def lists_intersect(l1, l2):
        assert type(l1) == list, PositionInvertedIndex.__WRONG_ARGUMENT_TYPE
        assert type(l2) == list, PositionInvertedIndex.__WRONG_ARGUMENT_TYPE

        lr = []
        i1 = 0
        i2 = 0
        while i1 < len(l1) and i2 < len(l2):
            if l1[i1] == l2[i2]:
                lr.append(l1[i1])
                i1 += 1
                i2 += 1
            elif l1[i1] > l2[i2]:
                i2 += 1
            else:
                i1 += 1
        return lr

    __WRONG_ARGUMENT_TYPE = "Wrong argument type"
