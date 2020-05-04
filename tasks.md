# Tasks for members
## Gaurav
- Performed analysis of two models from the leaderboard, along with the analysis of the baseline model.
- Read few papers on BERT, explored other model types like XLNET.
- Read various blogs pertaining to PyTorch library.
- Ran the baseline model on GCP by setting up the platform and attained similar accuracy.
- Explored methods to incorporate external knowledge to deal with the error scenarios.
- Error Analysis(20 samples)
    - Found one question answer, where predicted answer was more correct than the actual answer.
    - Found a couple questions, where questions where not paraphrased properly.
    - For most of the questions, the model was lacking knowledge of that context.
- Explored Graph Based Techniques for employing external knowledge for question answering dataset, read various papers and tried various techniques, most of them being complicated, due to the limited time available dropped the approach.
- Tried out various external knowledge sources like Atomic, Wikipedia APIs by using IR techniques to add relevant knowledge in order to answer questions.
- Adapted the reranking algorithms for IR done on questions from the McQueen repository to suit the commonsenseQA dataset, to deal with redundant facts and ranking based on relevancy.
- Helped Shatrughn in setting up ElasticSearch to perform IR(Information Retrieval) on external knowledge sources.


## Vasudha
- Ran and did analysis of Baseline Models.
- Analysis of two additional Models from the leaderboard.
- Worked on nltk and geotext libraries to extract proper nouns for location specific details.
- Read about BERT.
- Read the overview of graph based knowledge base.
- Read about Pytorch.
- Error Analysis:
    - Worked on 100 samples manually to analyse where the model fails.
    - Most of the questions were Location related. Locations mostly are not specific but are general like 'on microwave' etc. So extracting proper nouns might not work. 
    - Wrote a code to detect the number of location questions (considered it a location question if it had 'Where' or 'where'. There were 356 such questions, out of which 81 were predicted wrong and 51 out of those 81 had second best option as the answer.
    - Around 60 percent of the cases had the second best option as the answer.
    - Some questions made no sense. Ex: What do people with what is most likely to do what?. Cannot do anything for such questions.
    - Questions with not are also to be dealt properly.
    - Questions with negation are also to be taken care of.
    - Used nltk and geotext libraries to perform the analysis based on NNP tags.
- Studied paper on various datasets mentioned by kuntal. I along with shafali worked on knowledgebases like arc, verbphysics, CODAH in order to improve accuracy. Thought verbphysics could help our usecase based on our error analysis but did not implement it as the object pairs were difficult to concert into the format we needed.

## Praveen
- Analysis of the baseline model and two additional models from the leaderboard
- Read few papers for understanding BERT
- Read about PyTorch 
- Error Analysis(25 samples)
    - Some of the questions needed external knowledge to be answered.
    - Some questions were contexually illogical.
- Read papers about employing Information Retreival for Question Answering Systems
    - The documents of interest are fetched by matching query keywords to the index of the document collection.
    - An information retrieval-based QA system mainly follows three steps of analyzing a sentence: question processing, passage
retrieval, and answer processing.
    - Question processing always includes the step of classifying a sentence into answerable categories. This is to make sure that a QA system knows what type of answers are expected. 
    - In question processing, sentences are analyzed and formed into queries. It also includes a step of classification of questions into predefined categories such as location question, person question, and so on.These categories are important because they provide necessary information for constructing answers using the correct information.
    - Then, the relevant passages in all documents are retrieved and answers are constructed based on retrieved information during answer processing.
    - Looked up several examples for IR based QA systems which have been implemented to get an overview of the working process.  
- Looked up information regarding merging Information Retreival in Roberta model.
- Read a paper on incorporating Information Retrieval in a multi-language Question Answering system. 

## Shatrughn
- Worked on getting the baseline code running. We are getting similar accuracy in the dev dataset as the referenced code.
- Read about PyTorch and how the implementation of a model works in it.
- Read provided articles about BERT.
- Error analysis
    - Tried to relate questions with location pronouns to see if the model is having difficulty with location names. Was unsuccessful because location names in choices are lower cased and thus spaCy is having difficulty recognizing proper nouns or doing NER.
    - Analysed 20 samples from the wrong predictions.
      - In some of the questions (4/20), the predicted answers seems better than the correct answer marked by the dataset.
      - Some of the question texts (2/20) have typos or grammatical errors which make them ambiguous. I believe fixing them may give us the correct answer.
      - Some of the questions (4/20) seem to missing some general knowledge about specific topics. Pulling them from some knowledge base and finetuning the model may yield better results.
- **Phase 2**
    - Explored various knowledgebases that could be used as external knowledge to improve results. Since we had identified location based questions in our error analysis, we zeroed on Webchild dataset to get sentences for nouns. Atomic dataset was chosen for handling few of the if-then questions that were failing.
    - As we finally decided on the knowledgebases, Gaurav and I setup the Elasticsearch instance to ingest the datasets. Dockerfile from McQueen repo was used as a reference to setup Elasticsearch in a container.
    - Created multiple Elasticsearch indexes by ingesting different dataset combinations for experiments.
    - Modified some parameters to make the McQueen Roberta Concat solver run in GCP.
    - Created a new Fairseq task (commonsense_qa_with_kb_task.py) from baseline to adapt to the McQueen dataset format. Inputs were created as question + choices + premises truncated to 512 tokens.
    - Since almost all inputs now had 512 tokens because of concatenation of premises, the original finetuning script had to be modified to reduce the max-sentences to 2 at a time to avoid getting out of memory errors.

## Shafali
- Ran the baseline code to understand and evaluate the model we are working on.
- Analysis of Baseline Models.
- Analysis of one additional Model from the leaderboard.
- Did Error Analysis for 75 samples
    - Manual analysis was done and Question Domains were added along with Comments based on what information was gathered just by looking       at the question and options.
    - Wrote a little script to perform POS tagging on the questions and the options to gather more information on the location based             question.
    - Used nltk and geotext libraries to perform the analysis based on NNP tags.
    - Wrote a little script to calculate if we can draw some inference based on word count of the questions.
- Read a few articles to familiarize myself with the working of BERT.
- Studied a few blogs/articles/research papers on what external knowledgebase we can use to improve our model. Discussed upon knowledge bases like COS-E,QA-SRL BANK,CODAH in the meeting with Kuntal to understand if we can use them in our study.
- Worked on understanding datasets suggested by Kuntal that we can refer for the aforementioned purpose. Few of the datasets I looked into were Openbookqa, arc, OMCS, verbphysics, webchild and wikitext. Given the inferences we gathered from error analysis I thought we could make use of verb physics dataset given how it has mapping for different object pairs. 
- Worked on how to introduce verb physics to our model. Refered a few papers on how external knowledgebase can be added and came up with two approaches. Suggested knowledge hunting from using wiki texts for each object in the context.
- Read a few papers on a few other dataset used for common knowledge extraction with included majorly SWAG dataset.
- Noticed that verb physics eventually might not solve the problems because the pairings of objects are not relevant majorly to our model. However, accuracy can be improved if we take objects out of the questions and append additional information for those objects to our concept. For eg. If we some how can take the information for the object from wiki and use it.
- Wrote a script to extract meaningful sentences from the atomic dataset so that it can be used to perform tasks from the mcqueen's repository. The sentence extraction was done based on different combinations of sentence formations for every event listed in the dataset. 
