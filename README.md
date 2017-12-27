# Entity-Extraction

This is a package of extracting entities of various types from textual input. The functions implemented are: 

1. Time entity extraction (TimeEntity.py).
 
2. Quantity entity extraction (QuantityEntity.py).

3. Negaiton entity extraction (NegationEntity.py).

4. Evaluation of lab test results (LabtestEvaluation.py).

5. Medical entity extraction based on pre-defined database (MedicalEntity.py).

### Examples 

#### Time entity extraction 
`over 1 year, a study is conducted to assess the antileukemic activity of a new tyrosine kinase inhibitor in patients with chronic myeloid leukemia in blast crisis.`

[entity]:  over 1 year \t[charStartPos]:  0 \t[charEndPos]:  11

`a 63-year-old woman comes to the physician because of a 2-week history of fatigue, malaise, nausea and vomiting, and decreased appetite; these symptoms have worsened during the past week.`

[entity]:  2-week history of \t[charStartPos]:  56 \t[charEndPos]:  73

`a 63-year-old woman comes to the physician because of a 2-week history of fatigue, malaise, nausea and vomiting, and decreased appetite; these symptoms have worsened during the past week. she was diagnosed with tuberculosis 3 months ago`

[entity]:  2-week history of \t[charStartPos]:  56 \t[charEndPos]:  73
[entity]:  3 months ago \t[charStartPos]:  224 \t[charEndPos]:  236

#### Medical entity extraction 
`An 83-year-old man comes to the physician because of a 2-day history of constant severe pain of his right knee.`

[entity]:  pain   \t[category]:  symptoms   \t[startPos]:  15  \t[endPos]:  16
  
`Treatment with ibuprofen during the next week significantly improves his condition.`

[entity]:  ibuprofen  \t[category]:  medication  \t[startPos]:  2  \t[endPos]:  3
 
`A 16-year-old boy comes to the physician because of a rash on his left inner thigh that first appeared 2 days after he returned from a hunting trip with friends in Minnesota.`

[entity]:  rash  \t[category]:  disease  \t[startPos]:  10  \t[endPos]:  11

`A 63-year-old woman comes to the physician because of a 2-week history of fatigue, malaise, nausea and vomiting, and decreased appetite`

[entity]:  nausea \t[category]:  symptoms \t[startPos]:  15 \t[endPos]:  16


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
