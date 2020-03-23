# Tasks for members
## Gaurav
- Analysis of two Models from the leaderboard
- Graph Based Reasoning for using external knowledge sources
- Error Analysis(20 samples)

## Vasudha
- Error Analysis(100 samples)

## Praveen

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
