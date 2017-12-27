import Parse
import utils


class Negation():
    def __init__(self, negation_word, negation_object, negation_subject):
        self.negation_word = negation_word
        self.negation_object = negation_object
        self.negation_subject = negation_subject

class NegationEntity():
    def __init__(self):
        self.MAX_TEXT_LENGTH = 10000
        self.negation_setting_en = {
            'negation_pattern': ['no', 'absent', 'negative'],
            'check_left': [True, True, True],
            'check_right': [True, False, False],
            'connect_words': ['or', 'and', 'of the', 'of'],
            'noun_type': ['NN', 'NNS'],
            'noisy_words': ['plans', 'plan'],
        }

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
        print('\nNegation results...')
        for sent, re in zip(sents, res):
            print('\n[sentence]: ', sent)
            for r in re:
                if r.negation_word == 'no':
                    print('[negation]: ', r.negation_word, '[negation object]: ', r.negation_object)
                elif r.negation_word == 'negative':
                    print('[negation subject]: ', r.negation_subject, '[negation]: ', r.negation_word)

    def traverse_check(self, node):
        assert node is not None
        res = []
        if node.is_leaf:
            if node.get_word() == 'no':
                object = self.check_pattern_no(node)
                res = [Negation('no', object, None)]
            elif node.get_word() == 'negative':
                subject = self.check_pattern_negative(node)
                res = [Negation('negative', None, subject)]
        else:
            for child in node.children:
                temp = self.traverse_check(child)
                res.extend(temp)
        return res

    def check_pattern_no(self, node):
        assert node and node.is_leaf and node.get_word() == 'no'
        object = ''
        # rule 1: any words after 'NO' and appear in the same parent group with 'NO' will be extracted as object of 'NO'
        if node.parent:     # and node.parent.tag == 'NP'
            for child in node.parent.children[node.childid+1:]:
                object += ' ' + child.to_strings()
        # rule 2: if there is a PP group as sibling (next child) of the group that 'NO' is in, then the whole PP gruop will be extracted.
        if node.parent and node.parent.parent and node.parent.childid+1 < len(node.parent.parent.children) and \
            node.parent.parent.children[node.parent.childid+1].tag == 'PP':
            object += ' ' + node.parent.parent.children[node.parent.childid+1].to_strings()
        return object[1:]

    def check_pattern_negative(self, node):
        assert node and node.get_word() == 'negative'
        subject = ''
        # rule 1: only deal with this situation: (S (NP (DT a) (NN glucose) (NN oxidase) (NN test) (NN result)) (VP (VBZ is) (ADJP (JJ negative)))))
        if node.parent and node.parent.parent and node.parent.parent.tag == 'VP':
            vp = node.parent.parent
            if vp.parent and vp.childid > 0 and vp.parent.children[vp.childid-1].tag == 'NP':
                subject = vp.parent.children[vp.childid-1].to_strings()
        return subject

    def is_valid(self):
        pass