# NLP project on commonsenseqa dataset. 

## Dataset summary
A source concept and three target concepts are picked from the ConceptNet, three questions are made such that each target concept is picked as one of the answers. Additionally two other options are chosen as distractors, one option is chosen from the ConceptNet and the other is randomly introduced by the author. The scalability issue of dataset was solved by crowdsourcing.

## Analysis of some approaches used.
| Source  | Model Used | Accuracy  | External Knowledgebase | Extra processsing  | Error Analysis |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| ALBERT (ensemble model), Zhiyan Technology | ALBERT-xxlarge-v2  | 76.5%  | Not used  | For each sample, five parts are concatenated into one string,before sending it to ALBERT   | Not mentioned   |
|XLNet + Graph Reasoning (single model*), Microsoft Research Asia and Bing| XLNet-large | 75.3% | ConceptNet, Wikipedia | Each question is prefixed by a sorted list of evidence sentences from ConceptNet and Wikipedia, and is suffixed by the answer choices. | Three categories of errors were observed lack of evidence,similar evidence and dataset noise.|
| KEDGN (ensemble model) by PLA Academy of Military Science | KEDGN: Dual Graph Network that utilizes RoBERTa as the encoder | 74.4% | Open Mind Common Sense for pretraining | Only pretrain (maximum sequence length: 128; batch size: 96; learning rate: 1e-5; training epochs: 4; warmup steps: 0) and fine tuning (maximum sequence length: 96; batch size: 16; learning rate: 1e-5; training steps: 3000; warmup steps: 150) parameters are available. | N/A |
| RoBERTa + KE (single model) by Alibaba DAMO NLP | RoBERTa + KE (single model) | 73.3% | Open Mind Common Sense (OMCS) corpus and wiki data | Finetuned on OMCS-max updates: 100k, learning rate: 1e-4, batch size: 256, max sequence length: 512 and Finetuned on CSQA-max updates: 1000, learning rate: 1e-5, batch size: 64, max sequence length: 256 | N/A |
|FreeLB-RoBERTa (ensemble model), Microsoft Dynamics 365 AI Research & UMD | Roberta-Large (ensemble) model| 73.1% | used FreeLB finetuning | The model has not shown great improvements from Roberta model in the following fields : Named Entities, Quantifiers, Interval/Numbers, Universal (Logic). |
| [RoBERTa (ensemble model), Facebook AI](https://github.com/pytorch/fairseq/tree/master/examples/roberta/commonsense_qa) | roberta.large | 72.5% | None | Finetuned RoBERTa on CommonSenseQA. Five inputs constructed for each question, one for each of the five candidate answer choices, by concatenating the question and candidate answer. Eg `<s> Q: Where would I not want a fox? </s> A: hen house </s>` | N/A |
| [RoBERTa + IR (single model), Microsoft STCA-NLP team](https://1drv.ms/b/s!Aq1PIOBthMoKblvGqds3CzR451k?e=Yg6P94) | roberta.large | 72.1% | [RACE Dataset](https://www.cs.cmu.edu/~glai1/data/race/) | Finetune RoBERTa large model on the RACE dataset by concatenating passage, question and answer choice as `<s> <context tokens> </s> <question tokens> </s> <choice tokens> </s>`. Retrieve context information for each question of CommonsenseQA through search engine, and further finetune on train data. | N/A |
|HyKAS (single model), Bosch Research and Technology Center (Pittsburgh) | HyKAS | 62.5% | ConceptNet, ATOMIC | Included domain specific knowledge in order to improve the accuracy of the model. | The model is not very successful in the choice of the knowledge base depending upon the type of questions. Also it cannot handle antonym or negation sentences well. |
