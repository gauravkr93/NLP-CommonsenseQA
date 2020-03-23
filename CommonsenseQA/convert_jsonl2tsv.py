import json

choice_chars = ['A', 'B', 'C', 'D', 'E']
tsvlines = ['id\tquestion_concept\tquestion\tchoiceA\tscoreA\tchoiceB\tscoreB\tchoiceC\tscoreC\tchoiceD\tscoreD\tchoiceE\tscoreE\tanswer\tpredicted']
with open('fb-roberta-output/wrong_preds.jsonl') as f:
    for line in f:
        q = json.loads(line)
        l = []
        l.append(q['id'])
        l.append(q['question']['question_concept'])
        l.append(q['question']['stem'])

        choices = {}
        for c in q['question']['choices']:
            choices[c['label']] = f"{c['text']}\t{round(q['scores'][c['label']], 4)}"
        # To make sure TSV has choices in the order A,B,C,D,E
        for c in choice_chars:
            l.append(choices[c])

        l.append(q['answerKey'])
        l.append(q['predicted'])
        tsvlines.append('\t'.join(l))
        # print('\n'.join(tsvlines))
        # break

with open('fb-roberta-output/wrong_preds.tsv', 'w') as f:
    f.write('\n'.join(tsvlines))