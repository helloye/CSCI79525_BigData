with open('test.txt') as f:
    for line in f:
        # This gets the IDs out
        print(line.split()[0])
