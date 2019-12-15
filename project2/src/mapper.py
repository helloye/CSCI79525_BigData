# Change this to STDIN after development is done
with open('test_small.txt') as f:
    out_file = open("test_small_mapped.txt", "w")
    for line in f:
        line = line.strip()
        doc_id, data = line.split(' ', 1)
        words = data.split()
        words.sort()
        wc = len(words)
        for word in words:
            mapped_line = '{}\t{}\t{}\n'.format(doc_id, word, 1);
            # print(mapped_line)
            out_file.write(mapped_line)
