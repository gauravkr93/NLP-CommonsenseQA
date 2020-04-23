# Tasks for members
## Gaurav
- Analysis of two models from the leaderboard, along with the analysis of the baseline model.
- Read few papers on understanding BERT, explored other model types like XLNET.
- Graph Based Reasoning.
- Explored methods to incorporate external knowledge to deal with the error scenarios.
- Error Analysis(20 samples)
    - Found one question answer, where predicted answer was more correct than the actual answer.
    - Found a couple questions, where questions where not paraphrased properly.
    - For most of the questions, the model was lacking knowledge of that context.

## Vasudha
- Analysis of Baseline Models.
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
- Studied a paper on ARC dataset. However, this might not help more as it does not have much information about objects and their locations. ARC dataset has mainly information about Scientific data which might not help our usecase.

## Praveen
- Analysis of the baseline model and two additional models from the leaderboard
- Read few papers for understanding BERT
- Read about PyTorch 
- Read papers about deploying Information Retreival for Question Answering systems(QA)
- Error Analysis(25 samples)
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

## Shafali
- Ran the baseline code to understand and evaluate the model we are working on.
- Analysis of Baseline Models.
- Analysis of one additional Model from the leaderboard.
- Did Error Analysis for 75 samples
 - Manual analysis was done and Question Domains were added along with Comments based on what information was gathered just by looking at    the question and options.
 - Wrote a little script to perform POS tagging on the questions and the options to gather more information on the location based            question.
 - Used nltk and geotext libraries to perform the analysis based on NNP tags.
 - Wrote a little script to calculate if we can draw some inference based on word count of the questions.
- Read a few articles to familiarize myself with the working of BERT.
- Studied a few blogs/articles/research papers on what external knowledgebase we can use to improve our model. Discussed upon knowledge bases like COS-E,QA-SRL BANK,CODAH in the meeting with Kuntal.
- Worked on understanding datasets suggested by Kuntal that we can refer for the aforementioned purpose. Few of the datasets I looked into were Openbookqa, arc, OMCS, verbphysics, webchild and wikitext. Given the inferences we gathered from error analysis I thought we could make use of verb physics dataset given how it has mapping for different object pairs. 
- Worked on how to introduce verb physics to our model. Refered a few papers on how external knowledgebase can be added and came up with two approaches (need to clarify on the update call).
- Read a few papers on a few other dataset used for common knowledge extraction with included majorly on SWAG dataset.
- Noticed that verb physics eventually ight not solve the problems because the pairings of objects are not relevant majorly to our model. However, accuracy can be improved if we take objects out of the questions and append additional information for those objects to our concept. For eg. If we some how can take the information for the object from wiki and use it.(need to discuss on the call).
