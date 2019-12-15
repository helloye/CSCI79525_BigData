# Change this to STDIN after development is done
with open('test_small_mapped.txt') as f:
    for line in f:
        line = line.strip().split('\t')
        print(line)
        # TODO: Write reducer function
