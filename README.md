# NLP project on commonsenseqa dataset. 

## Dataset summary
A source concept and three target concepts are picked from the ConceptNet, three questions are made such that each target concept is picked as one of the answers. Additionally two other options are chosen as distractors, one option is chosen from the ConceptNet and the other is randomly introduced by the author. The scalability issue of dataset was solved by crowdsourcing.

## Analysis of some approaches used.
| Source  | Model Used | Accuracy  | External Knowledgebase | Extra processsing  | Error Analysis |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| ALBERT (ensemble model), Zhiyan Technology | ALBERT-xxlarge-v2  | 76.5%  | Not used  | For each sample, five parts are concatenated into one string,before sending it to ALBERT   | Not mentioned   |
|XLNet + Graph Reasoning (single model*), Microsoft Research Asia and Bing| XLNet-large | 75.3% | ConceptNet, Wikipedia | Each question is prefixed by a sorted list of evidence sentences from ConceptNet and Wikipedia, and is suffixed by the answer choices. | Three categories of errors were observed lack of evidence,similar evidence and dataset noise.|
| KEDGN (ensemble model) by PLA Academy of Military Science | KEDGN: Dual Graph Network that utilizes RoBERTa as the encoder | 74.4% | Open Mind Common Sense for pretraining | Only pretrain (maximum sequence length: 128; batch size: 96; learning rate: 1e-5; training epochs: 4; warmup steps: 0) and fine tuning (maximum sequence length: 96; batch size: 16; learning rate: 1e-5; training steps: 3000; warmup steps: 150) parameters are available. | N/A |
| DREAM (ensemble model), Microsoft Research Asia and Bing | DREAM,XLNet-Large  | 73.3%  | Wiki Docs  | Used elasticsearch to build index for Wiki docs and find top-10 sentences using BM25. The query is question + answer choice. Then concatenated as  <context tokens> <sep> <question tokens>  <answer tokens> <sep> <cls> to finetune XLNet-large cased model   | Not mentioned|
| RoBERTa + KE (single model) by Alibaba DAMO NLP | RoBERTa + KE (single model) | 73.3% | Open Mind Common Sense (OMCS) corpus and wiki data | Finetuned on OMCS-max updates: 100k, learning rate: 1e-4, batch size: 256, max sequence length: 512 and Finetuned on CSQA-max updates: 1000, learning rate: 1e-5, batch size: 64, max sequence length: 256 | N/A |
| HyKAS 2.0, CMU & Bosch Research and Technology Center (Pittsburgh) | HyKAS  | 73.2%  | BERT,ConceptNet  | Additionally, they extracted relevant ConceptNet triples for QA pairs and added an attention layer to attend question+answer encoding with commonsense information   | The model is able to do better on questions that require commonsense but is losing performance on other types. The models still lack the ability to reason over negation sentences, suggesting another direction for future improvement|  
|FreeLB-RoBERTa (ensemble model), Microsoft Dynamics 365 AI Research & UMD | Roberta-Large (ensemble) model|73.1% | GLUE benchmark | used FreeLB finetuning | The model has not shown great improvements from Roberta model in the following fields : Named Entities, Quantifiers, Interval/Numbers, Universal (Logic). |
| [RoBERTa (ensemble model), Facebook AI](https://github.com/pytorch/fairseq/tree/master/examples/roberta/commonsense_qa) | roberta.large | 72.5% | None | Finetuned RoBERTa on CommonSenseQA. Five inputs constructed for each question, one for each of the five candidate answer choices, by concatenating the question and candidate answer. Eg `<s> Q: Where would I not want a fox? </s> A: hen house </s>` | N/A |
| [RoBERTa + IR (single model), Microsoft STCA-NLP team](https://1drv.ms/b/s!Aq1PIOBthMoKblvGqds3CzR451k?e=Yg6P94) | roberta.large | 72.1% | [RACE Dataset](https://www.cs.cmu.edu/~glai1/data/race/) | Finetune RoBERTa large model on the RACE dataset by concatenating passage, question and answer choice as `<s> <context tokens> </s> <question tokens> </s> <choice tokens> </s>`. Retrieve context information for each question of CommonsenseQA through search engine, and further finetune on train data. | N/A |
|HyKAS (single model), Bosch Research and Technology Center (Pittsburgh) | HyKAS | 62.5% | ConceptNet, ATOMIC | Included domain specific knowledge in order to improve the accuracy of the model. | The model is not very successful in the choice of the knowledge base depending upon the type of questions. Also it cannot handle antonym or negation sentences well. |

## Phase 1 Understanding and Analysis

### XLNET vs BERT for CommonsenseQA dataset
XLNET is an AR(Auto Regressive) Model better for generative tasks, does not leverage the bi directionality of AE(Auto Encoder Models) like BERT. Since BERT assumes independence between masked data in masked LM phase. Hence, BERT is better suited for QA tasks than compared to XLNET. 

### Graph-Based approaches to use external knowledge base.
[Research Paper Referred - Graph-Based Reasoning over Heterogeneous External Knowledge for Commonsense Question Answering](https://arxiv.org/pdf/1909.05311.pdf)

#### Summary
The knowledge base used in this paper was ConceptNet(a structured knowledge base) and Wikipedia(unstructured). A total 107M sentences from Wikipedia was extracted by Spacy and was indexed by the use of Elastic Search tools. The prediction was a two step approach.

##### Graph-Based Contextual Representation Learning Module
A simple way to get the representation of each word is to concatenate all the evidence as a single sequence and feed the raw input into XLNet. However, this would assign a long distance for the words mentioned in different evidence sentences, even though they are semantically related. Therefore, graph structure was used to re-define the relative position between evidence words(topology sort). In
this way, semantically related words will have shorter relative position and the internal relational structures in evidence are used to obtain better contextual word representations.

For Wikipedia sentences,a sentence graph was constructed. The evidence sentences S are nodes in the graph. For two sentences si and sj , if there is anedge (p, q) in Wiki-Graph where p, q are in si and sj respectively, there will be an edge (si, sj ) in the sentence graph. Sorted evidence sequence S' is achieved by the method in Algorithm 1(refer the paper). 

For ConceptNet, the relation template provided by ConceptNet was used to transfer a triple into a natural language text sentence. For example, “mammals HasA hair” will be transferred to “mammals has hair”. In this way, we can get a set of sentences ST based on the triples in the extracted graph. Then we can get the re-ordered evidence for ConceptNet ST' with the method shown in Algorithm 1(refer the paper).

##### Graph-Based Inference Module
The XLNet-based model mentioned in the previous subsection provides effective word-level clues for making the prediction. Beyond that, the graph provides more semantic level information of evidence at a more abstract layer, such as the subject/object of a relation.

A more desirable way is to aggregate evidence at the graph-level to make the final prediction. Specifically, we regard the two evidence graphs ConceptGraph and Wiki-Graph as one graph and adopt Graph Convolutional Networks ([GCNs](https://towardsdatascience.com/how-to-do-deep-learning-on-graphs-with-graph-convolutional-networks-7d2250723780)) (Kipf and Welling 2016) to obtain node representations by encoding graph-structural information.

In order to reason over the graph, we propagate information across evidence via two steps: aggregation and combination. The concatenated input representation hc with the graph representation hg as the input of a Multi-Layer Perceptron(MLP) to compute the confidence score score(q, a). The probability of the answer candidate a to the question a can be computed as follows, where A is the set of candidate answers.

Papers regarding Information Retrieval method for Question Answering System

https://staff.fnwi.uva.nl/m.derijke/Publications/Files/ecir2008-nenormalization.pdf

https://etd.ohiolink.edu/pg_10?0::NO:10:P10_ACCESSION_NUM:osu1388065704

### Baseline model - [RoBERTa, Facebook AI](https://github.com/pytorch/fairseq/tree/master/examples/roberta/commonsense_qa)
We were successful in executing the code provided and getting an accuracy similar to theirs in the dev dataset.

Upload the `CommonsenseQA` folder as a zip and follow the notebook [`CSQA_Roberta.ipynb`](CSQA_Roberta.ipynb) to finetune and evaluate the model.

If you want to simply evaluate the model, download the [checkpoint file](https://drive.google.com/open?id=10PCeHt9yhn-Q6cJxRHQf4CNnwxRvrxNt) and place it in `CommonsenseQA/fairseq/checkpoints` folder. And then execute the relevant cell in the notebook.

#### Error Analysis
The objective of this task was to manually analyse the predictions against the expected outputs to infer any information that would suggest why the predictions do not align with the correct output. There are about 267 samples that were wrongly predicted.
Manual analysis involved marking the questions with relevant information that we inferred from just looking at the questions and options. We also did POS tagging for identifying possible patterns with location based questions. We made use of NER, nltk and geotext to gather the proper nouns for our inferences.
https://docs.google.com/spreadsheets/d/14U5gmqY6iRyP0faPunx0vxphVJW2ycZp7cVCjW-VVAM/edit?usp=sharing

## Phase 2 Experiments

For phase 2, we tried to add external knowledge bases and extract facts for each quetion + answer option combination to train a model with extra knowledge.

We used scripts from [McQueen](https://github.com/ari9dam/McQueen) to ingest KB, IR from them, rerank facts using sentence similarity and finally construct the dataset in the format required by McQueen's MCQ solvers.

Following 3 experiments were tried:

1. **McQueen Roberta Concat Solver**  
  **Accuracy: ~20%**  
  Initially, the script was crashing due to CUDA going out of memory. Reduced `max_seq_length` to make it run (though in hindsight, probably should have modified `train_batch_size`). See the [`CSQA_Roberta.ipynb`](CSQA_Roberta.ipynb) for the script params and [`logs/mcqueen-robertalg_concat_2e6_009.log`](logs/mcqueen-robertalg_concat_2e6_009.log) for the training log.  
  One of the reasons for this poor performance can be that some of the parameters were probably modified wrongly. Also, it was noticed that in the McQueen [`hf_roberta_mcq_concat_reader.py`](https://github.com/ari9dam/McQueen/blob/master/pytorch_transformers/models/hf_roberta_mcq_concat_reader.py) code, question was concatenated with choices to create new choices and question set to None ([1](https://github.com/ari9dam/McQueen/blob/master/pytorch_transformers/models/hf_roberta_mcq_concat_reader.py#L162)), premises were concatenated to act as questions ([2](https://github.com/ari9dam/McQueen/blob/master/pytorch_transformers/models/hf_roberta_mcq_concat_reader.py#L101)) and then finally input is constructed as question (which is now premises) + choices (which is question + choices) ([3](https://github.com/ari9dam/McQueen/blob/master/pytorch_transformers/models/hf_roberta_mcq_concat_reader.py#L65)). This meant that knowledge was added before question and options. Due to concatenation of all 10 premises, it is probable that all the 512 tokens in input were of premises only without the question and choices. Due to lack of time, did not try to experiment with modifying this code.

2. **Fairseq Roberta Concat with KBs ARC, Webchild, OpenbookQA, and Atomic**  
  **Accuracy: 76.49%**  
  See [`CommonsenseQA/finetune-arc-web-open-atomic.sh`](CommonsenseQA/finetune-arc-web-open-atomic.sh) for the finetuning script and  [`logs/finetune-arc-web-open-atomic.log`](logs/finetune-arc-web-open-atomic.log) for training log.  
  Used ARC (14M sentences), Webchild (148k nouns) and Openbook (1300 sentences) as general knowledge bases and Atomic (22k sentences) for If-then type of questions. Modified the fairseq task from baseline ([commonsense_qa_with_kb_task.py](CommonsenseQA/fairseq/examples/roberta/commonsense_qa_with_kb_task/commonsense_qa_with_kb_task.py)) to adapt to the McQueen dataset format. Inputs were created as question + choices + premises truncated to 512 tokens.  
  Accuracy reduced ~2% from the baseline model probably because we used general knowledgebases and didn't use ones which were specific or more relevant to the provided dataset.

3. **Fairseq Roberta Concat with KBs ARC, Webchild, and ConceptNet**  
  **Accuracy: 76.57%**  
  See [`CommonsenseQA/finetune-web-arc-cn.sh`](CommonsenseQA/finetune-web-arc-cn.sh) for the finetuning script and  [`logs/finetune-web-arc-cn.log`](logs/finetune-web-arc-cn.log) for training log.  
  As an experiment, we added ConceptNet as a relevant KB to check if the accuracy improves. There was a very minor improvement though we are not sure if it can be credited to ConceptNet.


 Finally, we can conclude that we need more relevant external knowledge bases and we need to improve our IR and reranking to provide the model with more specific facts.
