from collections import Counter
import utils
import re
import string
import io
import operator
import glob
from functools import reduce
import marisa_trie


class Entity():
    def __init__(self, entity, category, startpos, endpos):
        self.entity = entity
        self.category = category
        self.startpos = startpos    # the first word position of the entity in the sentence
        self.endpos = endpos        # the first word position following the entity in the sentence

class MedicalEntity():
    def __init__(self):
        self.dictionary_files = glob.glob('entityDictionaries/*.txt')

        def build_trie_from_files():
            list = []
            entity_category = {}
            for file in self.dictionary_files:
                category = None
                for c in ['abnormality', 'disease', 'labtests', 'medication', 'symptoms']:
                    if c in file:
                        category = c
                assert category is not None, '{} does not have category'.format(file)
                with io.open(file, 'r', encoding='utf-8') as f:
                    for line in f:
                        entity = line.replace('\n', '')
                        list.append(entity)
                        entity_category[entity] = category

            trie = marisa_trie.Trie([str(s) for s in list])
            trie_reverse = marisa_trie.Trie([str(s)[::-1] for s in list])
            return trie, trie_reverse, entity_category

        self.trie, self.trie_reverse, self.entity_category = build_trie_from_files()

    def get_result(self, text):
        # input is text, output is a list of Entity instances.
        res = []
        sentences = [sentence for sentence in text.split('\n') if sentence]
        for sentence in sentences:
            words = sentence.split()
            result = []
            i = 0
            while i < len(words):
                wi = 0
                while i + wi < len(words) and self.trie.has_keys_with_prefix(u' '.join(words[i:i + wi + 1])):
                    wi += 1
                if wi > 0:
                    while wi > 0 and u' '.join(words[i:i + wi]) not in self.trie:
                        wi -= 1
                    if wi > 0:
                        phrase = u' '.join(words[i:i + wi])
                        result.append(Entity(phrase, self.entity_category[phrase], i, i+wi))
                        i = i + wi
                    else:
                        i += 1
                else:
                    i += 1

            res.append(result)
        return sentences, res

    def print_result(self, sents, res):
        print('\nMedical entity results...')
        for sent, re in zip(sents, res):
            print('\n[sentence]: ', sent)
            for r in re:
                print('[entity]: ', r.entity, '[category]: ', r.category, '[startPos]: ', r.startpos, '[endPos]: ', r.endpos)





