text_data = []

with open('test_small.txt') as f:
    for line in f:
        line = line.strip()
        doc_id, data = line.split(' ', 1)
        words = data.split()
        words.sort()
        wc = len(words)
        for word in words:
            print("%s\t%s\t%s" % (doc_id, word, 1))
