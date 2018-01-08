# Entity-Extraction

This is a package of extracting entities of various types from textual input. The functions implemented are: 

1. Time entity extraction (TimeEntity.py).
 
2. Quantity entity extraction (QuantityEntity.py).

3. Negaiton entity extraction (NegationEntity.py).

4. Evaluation of lab test results (LabtestEvaluation.py).

5. Medical entity extraction based on pre-defined database (MedicalEntity.py).

### Examples 

![alt text](https://github.com/s1155026040/Entity-Extraction/blob/master/example.png)

## Preparation 

Download stanford-corenlp-parser library from following link and put the folder under current path.
``https://drive.google.com/file/d/0BzgjLMJvxtcpeUpjNTBSMTYwamc/view?usp=sharing``

Run ``bash requirement.sh`` to install required library.

Run test.py to test all available functions.


## Details

Each function provides:

1. get_result(text)

    The input text is a string. This returns (sents, res) where sents is a list of sentence strings and res is a list of instance for each sentence in sents. The instance for each function is defined differently. Please refer to each function script for more details.

2. print_result(sents, res)

    The input sents is a list of sentence strings and res is a list of results for each sentence in sents.


Remark:

This package provides functions for entity extraction based on hand-crafted rules. It is reasonable that some entities are not covered by the functions. I will keep improving and updating the package.
