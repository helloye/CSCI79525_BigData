## Pre-req
Ensure that the following versions and packages are correct.
-	Java 8
-	PySpark 2.4.4
-	Running using Python 3.7

## Run Instructions
To run the program, simply use the below run command structure:

`spark-submit spark_map_reduce.py <file> <term_to_search> <gene_or_dis_tag>`

Note the paramters in `<...>`:


`<file>`: Location of file, will be fed into spark context, so can be anything from local file to s3 buckets to hdfs

`<term_to_search>`: If supplied, will only search for similarity scores that relates to the term, if omitted prints all term-term pair scores

`<gene_or_dis_tag>`: Can only be supplied if `<term_to_search>` is provided. Enter only `“gene”` or `“dis”` to find gene_xyz_gene or dis_xyz_dis results. Does a string search by splitting word delimited by “_” and checking if encapsulated by “gene” or “dis”
