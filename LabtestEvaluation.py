import io
import json
from collections import OrderedDict
import ModelAccess
from QuantityEntity import *
import utils

class AbnormalQuantity():
    def __init__(self, entity, quantity, unit, lowerBound, upperBound, refUnit):
        self.entity = entity
        self.quantity = quantity
        self.unit = unit
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.refUnit = refUnit

class LabtestEvaluation():

    def __init__(self):
        self.labtestref_path = 'labtest_ref.json'

        def build_labtest_dict(labtestref_path):
            entries = json.load(io.open(labtestref_path, 'r', encoding='utf-8'))
            labtest_dict = OrderedDict()
            for entry in entries:
                labtest_dict[entry['name'].lower()] = entry
            return labtest_dict

        self.labtestdict = build_labtest_dict(self.labtestref_path)

    def get_result(self, text):
        sents, quantity_res = QuantityEntity().get_result(text)
        res = []
        for quant_list in quantity_res:
            res.append(self.evaluate_labtest(quant_list))
        return sents, res

    def print_result(self, sents, res):
        print('\nLabtest abnormal evaluation results...')
        for sent, re in zip(sents, res):
            print('\n[sentence]: ', sent)
            for r in re:
                print('[entity]: ', r.entity, '[quantity]: ', r.quantity, '[unit]: ', r.unit, '[lowerBound]: ', r.lowerBound, '[upperBound]: ', r.upperBound, '[refUnit]: ', r.refUnit)

    def evaluate_labtest(self, quantity_list):
        # input quantity_list is a list of Quantity instance with keys (quantity, entity, unit)
        abnormal_quantities = []
        for quant in quantity_list:
            quantity, entity, unit = quant.quantity, quant.entity, quant.unit
            if not self.is_number(quantity):
                continue
            quantity = float(quantity)
            if entity:
                entity_tmp = self.remove_common_words(entity)
                if entity_tmp in self.labtestdict:
                    for refUnit, lowerBound, upperBound in self.labtestdict[entity_tmp]['ref_values']['Universal']:
                        if unit == refUnit:
                            if quantity < lowerBound or quantity > upperBound:
                                abnormal_quantities.append(AbnormalQuantity(entity, quantity, unit, lowerBound, upperBound, refUnit))

        return abnormal_quantities

    def is_number(self, value):
        for char in value:
            if not char.isdigit():
                return False
        return True

    def remove_common_words(self, entity):
        entity = entity.lower()
        entity = entity.replace('serum', '').replace('blood', '')
        return entity.strip()


    def is_valid(self):
        pass