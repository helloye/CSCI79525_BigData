from pyspark.sql import SparkSession
import math, re, pprint

ignore_pattern = re.compile("^[0-9\-%]*$")

spark = SparkSession.builder.master("local[*]").getOrCreate()

sc = spark.sparkContext

sc.setLogLevel('OFF')

data = sc.textFile("test_small.txt")

num_docs = data.count()

def break_into_words(doc):
    """
    i/p = a line from the file - doc id, doc

    o/p = A list of kv pairs, where k is the docid and the work, value is 1
    """
    (doc_id, sentence) = doc.split(" ", 1)
    filtered_sentence = list(filter(lambda word: not ignore_pattern.match(word), sentence.split(" ")))
    total_words = len(filtered_sentence) # Considered the length without the stop words.
    output = []
    for word in filtered_sentence:
        output.append(((doc_id, total_words, word), 1))

    return output

bydocid = data.flatMap(break_into_words) # the output has (doc_id, total_words_in_doc, word) as our key, and 1 as value
by_doc_counts = bydocid.reduceByKey(lambda x, y: x + y) # the output has (doc_id, total_words_in_doc, word) as key, and word_freq_in_doc as value


def find_tf(pair):
    key = pair[0]
    word_freq = pair[1]
    doc_id = key[0]
    total_words = key[1]
    word = key[2]
    tf = word_freq / total_words
    return (word, [(doc_id, tf)] )

word_doc_tf = by_doc_counts.map(find_tf) # Output is key = (word, [(value as docid, and term frequency)])

word_tf = word_doc_tf.reduceByKey(lambda x, y: x + y) # I,  [ (D1, 1/4), (D2, 1/3) ]

def tf_idf(word_doc_freq):
    word = word_doc_freq[0]
    doc_and_freq = word_doc_freq[1]
    doc_freq = len(doc_and_freq)

    idf = math.log2(num_docs / doc_freq)

    tf_idfs = []

    for (docid, tf) in doc_and_freq:
        tf_idfs.append( (docid, tf * idf) )

    return (word, tf_idfs)

word_and_tfidfs = word_tf.map(tf_idf)  # Collection of (word, [ (docid, tfidf), .... ] )


def find_similarity(word_tf_idf1, word_tf_idf2):
    word1 = word_tf_idf1[0]
    docid_tfidfs1 = dict(word_tf_idf1[1])  # dict allows lookup by docid
    word2 = word_tf_idf2[0]
    docid_tfidfs2 = dict(word_tf_idf2[1])

    all_doc_ids = list( docid_tfidfs1.keys() ) + list( docid_tfidfs2.keys() )

    numerator = 0
    for doc_id in all_doc_ids:
        if doc_id in docid_tfidfs1 and doc_id in docid_tfidfs2:
            numerator = numerator + (docid_tfidfs1[doc_id] * docid_tfidfs2[doc_id])

    denominator = max(math.sqrt( sum([x * x for x in docid_tfidfs1.values()]) ) * math.sqrt( sum([x * x for x in docid_tfidfs2.values()])), 1)

    sim = numerator / denominator

    return (word1, word2, sim)

term_term_sim = word_and_tfidfs.cartesian(word_and_tfidfs).filter(lambda x: x[0][0] < x[1][0]) \
    .map(lambda x: find_similarity(x[0], x[1])).filter(lambda x: x[2] > 0)

# cartesian example
# [1,2] - cartesian with itself and then .filter(lambda x: x[0][0] < x[1][0]) = [(1, 2)]

pprint.pprint(term_term_sim.collect())

# term_term_sim.saveAsTextFile("term_term_sim")
