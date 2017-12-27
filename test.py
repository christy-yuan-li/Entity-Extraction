from LabtestEvaluation import *
from NegationEntity import *
from QuantityEntity import *
from TimeEntity import *
from MedicalEntity import *
import Parse


TEST_NEGATION = 1
TEST_QUANTITY = 1
TEST_TIME = 1
TEST_LABEVALUATION = 1
TEST_MEDICALENEITY = 1
GENERATE_PARSE = 1

if TEST_MEDICALENEITY:
    ME = MedicalEntity()
    notes = io.open('./admissionNotes/entity_sample.txt', 'r', encoding='utf-8').read()
    sents, res = ME.get_result(notes)
    ME.print_result(sents, res)


if TEST_TIME:
    TM = TimeEntity()
    notes = io.open('./admissionNotes/time_sample.txt', 'r', encoding='utf-8').read()
    sents, res = TM.get_result(notes)
    TM.print_result(sents, res)

if TEST_NEGATION:
    NE = NegationEntity()
    notes = io.open('./admissionNotes/negation_sample.txt', 'r', encoding='utf-8').read()
    sents, res = NE.get_result(notes)
    NE.print_result(sents, res)

if TEST_QUANTITY:
    QN = QuantityEntity()
    notes = io.open('./admissionNotes/quantity_sample.txt', 'r', encoding='utf-8').read().split('\n')
    note = '\n'.join(notes)
    sents, res = QN.get_result(note)
    QN.print_result(sents, res)


if TEST_LABEVALUATION:
    LE = LabtestEvaluation()
    notes = io.open('./admissionNotes/quantity_sample.txt', 'r', encoding='utf-8').read().split('\n')
    note = '\n'.join(notes)
    sents, res = LE.get_result(note)
    LE.print_result(sents, res)

if GENERATE_PARSE:
    # generate output and save to text_temp.txt.out as default
    notes = io.open('./admissionNotes/sample2.txt', 'r', encoding='utf-8').read().split('\n')
    note = '\n'.join(notes[:100])
    sents, res = Parse.get_result(note)