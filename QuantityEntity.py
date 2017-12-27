import re

import Parse
import utils


class Quantity():
    def __init__(self, quant, quantpos):
        self.entity = None
        self.quantity = quant
        self.unit = None
        self.quantitypos = quantpos
        self.entitypos = None
        self.unitpos = None

    def set_unit(self, unit):
        if unit not in ['and']:
            self.unit = unit

class QuantityEntity():

    def get_result(self, text):
        sents, res = [], []
        parsed_text = utils.call_stanfardnlp_parse(text)
        parsed_sentences = Parse.get_parsed_text(parsed_text.split('\n'))
        for parsed_sentence in parsed_sentences:
            root = Parse.encode_tree(parsed_sentence)
            sents.append(root.to_strings())
            temp = self.traverse_check(root)
            res.append(temp)
        return sents, res

    def print_result(self, sents, res):
        print('\nQuantity result...')
        for sent, re in zip(sents, res):
            print('\n[sentence]: ', sent)
            for r in re:
                print('[entity]: ', r.entity, '[quantity]: ', r.quantity, '[unit]: ', r.unit)

    def traverse_check(self, node):
        # inorder traverse the tree, collect and return a list of quantity instances
        assert node is not None
        res = []
        if node.is_leaf:
            temp = self.check_pattern(node)
            if temp is not None:
                res = [temp]
        else:
            for child in node.children:
                temp = self.traverse_check(child)
                res.extend(temp)
        return res

    def check_pattern(self, node):
        assert node and node.is_leaf
        quant_instance = None
        potquan, potunit = self.check_has_quantity(node.get_word())
        if potquan is not None:
            quant_instance = Quantity(potquan, node.span[0])
            quant_instance.set_unit(potunit if potunit is not None else node.next_word)
            # find entity (the left closest NP phrase)
            stop = False
            temp = node
            while not stop and temp is not None and temp.parent is not None:
                # if temp.parent.tag in ['PP', 'PRN']:
                #     break
                if temp.tag == ',':
                    break
                for child in temp.parent.children[:temp.childid]:
                    # if child.tag in ['PP', 'PRN']:
                    #     stop = True
                    #     break
                    if child.tag == ',':
                        stop = True
                    if child.tag in ['NP', 'WDT']:
                        stop = True
                        quant_instance.entity = child.to_strings()
                        break
                if stop:
                    break
                temp = temp.parent

        return quant_instance


    def check_has_quantity(self, s):
        if not s:
            return (None, None)
        unit = None
        i = len(s) -1
        while i > -1 and s[i].lower() in list('abcdefghijklmnopqrstuvwxyz/-'):
            i -= 1
        if i == -1:
            return (None, None)
        if i < len(s)-1:
            unit = s[i+1:]
        s = s[:i+1]
        if re.match("^\d+?\.\d+?$", s) or re.match("^\d+?\\/\d+?$", s) or re.match("^\d+?\,\d+?$", s) or s.isdigit():
            return (s, unit.replace('-', ' ').strip() if unit else unit)
        return (None, None)


    def is_valid(self):
        pass

