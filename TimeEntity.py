import re
import sys
import ModelAccess

class Time():
    def __init__(self, entity, startpos, endpos):
        self.entity = entity
        self.charstartpos = startpos    # the position of the first char of the entity
        self.charendpos = endpos        # the position of the first char following the entity in the sentence

class TimeEntity():
    def __init__(self):
        self.age_pattern_en = '(\d+-(year|month|day|)s?-old)|(at\sthe\sage\sof\s|at\sthe\sages\sof\s)\d+\s*(year|month|day)?s*(and\s*\d+\s*(year|month|day)?s?)*'
        self.time_patterns_en = '(within )*(over the past )*(for the past )*(for )*(over )*(in )*(the past )*(after )*' \
                           '(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three)' \
                           '[ -]+(weeks|years|months|days|hours|minutes|seconds|week|year|month|day|hour|minute|second)+[ ]*(ago)?(after)?(history of)?(period)?'

    def get_result(self, text):
        sentences = text.lower().split('\n')
        sentences = [sentence for sentence in sentences if sentence]
        res = []
        for sentence in sentences:
            result = []
            text_pointer = 0
            age_pointer = 0
            age_search = re.search(self.age_pattern_en, sentence)
            time_search = re.search(self.time_patterns_en, sentence)
            while time_search:
                while age_search and time_search and set(
                        range(age_pointer + age_search.start(), age_pointer + age_search.end())).intersection(
                        set(range(text_pointer + time_search.start(), text_pointer + time_search.end()))):
                    text_pointer += time_search.end()
                    age_pointer += age_search.end()
                    time_search = re.search(self.time_patterns_en, sentence[text_pointer:])
                    if time_search and not set(range(age_pointer + age_search.start(), age_pointer + age_search.end())).intersection(
                            set(range(text_pointer + time_search.start(), text_pointer + time_search.end()))):
                        age_search = re.search(self.age_pattern_en, sentence[age_pointer:])

                if not time_search:
                    break
                result.append(Time(sentence[text_pointer + time_search.start():text_pointer + time_search.end()],
                                   text_pointer + time_search.start(), text_pointer + time_search.end()))

                text_pointer += time_search.end()
                time_search = re.search(self.time_patterns_en, sentence[text_pointer:])
            res.append(result)
        return sentences, res

    def print_result(self, sents, res):
        print('\nTime entity results...')
        for sent, re in zip(sents, res):
            print('\n[sentence]: ', sent)
            for ti in re:
                print('[entity]: ', ti.entity, '[charStartPos]: ', ti.charstartpos, '[charEndPos]: ', ti.charendpos)

    def is_valid(self):
        pass
