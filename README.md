# NLP project on commonsenseqa dataset. 

## Analysis of some approaches used.
| Source  | Model Used | Accuracy  | External Knowledgebase | Extra processsing  | Error Analysis |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| ALBERT (ensemble model), Zhiyan Technology | ALBERT-xxlarge-v2  | 76.5%  | Not used  | For each sample, five parts are concatenated into one string,before sennding it to ALBERT   | Not mentioned   |
|XLNet + Graph Reasoning (single model*), Microsoft Research Asia and Bing| XLNet-large | 75.3% | ConceptNet, Wikipedia | ||
| [RoBERTa (ensemble model), Facebook AI](https://github.com/pytorch/fairseq/tree/master/examples/roberta/commonsense_qa) | roberta.large | 72.5% | None | Finetuned RoBERTa on CommonSenseQA. Five inputs constructed for each question, one for each of the five candidate answer choices, by concatenating the question and candidate answer. Eg `<s> Q: Where would I not want a fox? </s> A: hen house </s>` | N/A |
| [RoBERTa + IR (single model), Microsoft STCA-NLP team](https://1drv.ms/b/s!Aq1PIOBthMoKblvGqds3CzR451k?e=Yg6P94) | roberta.large | 72.1% | [RACE Dataset](https://www.cs.cmu.edu/~glai1/data/race/) | Finetune RoBERTa large model on the RACE dataset by concatenating passage, question and answer choice as `<s> <context tokens> </s> <question tokens> </s> <choice tokens> </s>`. Retrieve context information for each question of CommonsenseQA through search engine, and further finetune on train data. | N/A |
