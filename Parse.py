#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import utils

class Tree(object):
    def __init__(self, tag):
        self.tag = tag
        self.is_leaf = False
        self.word = None
        self.children = []
        self.parent = None
        self.span = None     # indicate the word position in a sentence
        self.childid = None
        self.size = None     # for root node for a sentence, size records the number of words in the sentence
        self.next_word = None
        self.prev_word = None

    def set_leaf(self, word):
        self.is_leaf = True
        self.word = word

    def get_word(self):
        if self.is_leaf:
            return self.word
        else:
            raise ValueError('Non-leaf node has not word')

    def set_parent(self, parent):
        self.parent = parent
    def get_parent(self):
        return self.parent

    def set_children(self, child):
        self.children.append(child)

    def to_strings(self):
        # return the string of words under this Tree node (including all children words)
        if self.is_leaf:
            return self.get_word()
        else:
            res = ''
            for child in self.children:
                res += ' ' + child.to_strings()
            return res[1:]

    def to_components(self):
        if self.is_leaf:
            return [[self.tag, self.word, self.span]]
        else:
            res = []
            for child in self.children:
                res.extend(child.to_components())
        return res

    def tag_word_pos(self):
        def _tag_word_pos(node, pos):
            if node.is_leaf:
                node.span = [pos, pos]
                return pos
            else:
                startpos = pos
                for child in node.children:
                    pos = _tag_word_pos(child, pos)
                    pos += 1
                endpos = pos-1
                node.span = [startpos, endpos]
                return endpos

        _tag_word_pos(self, 0)

    def tag_neighbor_word(self):
        def _tag_neighbor_word(node, words):
            if node.is_leaf:
                node.next_word = words[node.span[0] + 1] if node.span[0] < len(words)-1 else ''
                node.prev_word = words[node.span[0] - 1] if node.span[0] > 0 else ''
            else:
                for child in node.children:
                    _tag_neighbor_word(child, words)

        _tag_neighbor_word(self, self.to_strings().split())


def encode_tree(line):
    items = [item.strip() for item in line.replace('))', ') ) ').split()]
    root = Tree(items[0].replace('(', ''))
    i = 1

    def helper(node, i):
        item = items[i]
        while item[0] == '(':
            newnode = Tree(item[1:])
            newnode.set_parent(node)
            newnode.childid = len(node.children)
            node.children.append(newnode)
            i = helper(newnode, i+1)
            i += 1
            item = items[i]

        if item == ')':
            return i
        else:
            node.is_leaf = True
            node.word = item.replace(')', '')
            return i

    while i < len(items):
        i = helper(root, i)
        i += 1

    root.tag_word_pos()
    root.tag_neighbor_word()
    root.size = len(items)
    return root

def get_parsed_text(lines):
    parse_sentences = []
    sentence_lines = []
    for line in lines:
        if not line.strip(): continue
        if 'sentence #' in line.lower():
            if sentence_lines:
                parse_sentences.append(' '.join(sentence_lines))
            sentence_lines = []
        elif line.strip()[0] == '(':
            sentence_lines.append(line.strip())
    if sentence_lines:
        parse_sentences.append(' '.join(sentence_lines))
    return parse_sentences

def get_result(text):
    sents, res = [], []
    parsed_text = utils.call_stanfardnlp_parse(text)
    parsed_sentences = get_parsed_text(parsed_text.split('\n'))
    for parsed_sentence in parsed_sentences:
        root = encode_tree(parsed_sentence)
        sents.append(root.to_strings())
        res.append(root)
    return sents, res

TEST_PARSE_NEW = 0
if TEST_PARSE_NEW:
    pass

