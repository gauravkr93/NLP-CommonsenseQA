
with open('CommonsenseQA/data/omcs-sentences-free.txt', encoding='utf8') as omcs, open('CommonsenseQA/data/omcs-en-sentences.txt', 'w', encoding='utf8') as out:
    row = None
    try:
        for line in omcs:
            row = line.split('\t')
            # print(row)
            if len(row) == 7 and row[4] == 'en':
                out.write(row[1])
                out.write('\n')
    except:
        print(row)
