from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer, StringIndexer, StopWordsRemover, NGram, HashingTF, IndexToString
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import argparse
import numpy

parser = argparse.ArgumentParser(description = 'Spark ML model builder for fake news detection')
parser.add_argument('--fake-glob', type=str, required=True,
    help='A glob pattern containing text files with extracted articles from fake or click-bait sites')
parser.add_argument('--real-glob', type=str, required=True,
    help='A glob containing text files with extracted articles from real and legitimante sites')
parser.add_argument('--data-partitions', type=int, default=1,
    help='The number of partitions to split the initial set into for better parallelization')
parser.add_argument('--tf-features', type=int, default=10000,
    help='The number of TF features to include in the classifier')
args = parser.parse_args()

# Create the Spark and Spark SQL contexts
conf = SparkConf().setAppName('model-builder')
sc = SparkContext(conf = conf)
scSql = SQLContext(sc)

# Load the fake and real files
fake_files = sc.textFile(args.fake_glob, args.data_partitions)
real_files = sc.textFile(args.real_glob, args.data_partitions)

# Label the fake and real files
labeled_fake_files = fake_files.map(lambda fake_file: ('fake', fake_file))
labeled_real_files = real_files.map(lambda real_file: ('real', real_file))

# Create a union of fake and real files and re-partition
all_labeled_files = sc.union([labeled_fake_files, labeled_real_files])

# Create the dataframe for the ML pipeline
labeled_files_df = scSql.createDataFrame(all_labeled_files, ['label', 'contents'])
(training_data, test_data) = labeled_files_df.randomSplit([0.8, 0.2])

# Stage 1: Tokenize words to create n-grams
tokenizer = Tokenizer(inputCol = 'contents', outputCol='words')

# Stage 2: Represent the string labels as integer indices
indexer = StringIndexer(inputCol = 'label', outputCol='label_index').fit(labeled_files_df)

# Stage 3: Remove stop words before building n-grams
stopwords = StopWordsRemover(inputCol = 'words', outputCol = 'notstopwords')

# Stage 4: Create n-grams as the basis for the feature space
ngram = NGram(n=2, inputCol='notstopwords', outputCol='ngrams')

# Stage 5: Count the n-grams to build the feature space
hashtf = HashingTF(numFeatures=args.tf_features, inputCol='ngrams', outputCol='features')

# Stage 6: Build a random forest model based on the feature data
randforest = RandomForestClassifier(labelCol='label_index', numTrees=100, maxDepth=10)

# Stage 7: Convert the integer indices back to labels
unindexer = IndexToString(inputCol = 'prediction', outputCol='prediction_label', labels=indexer.labels)

# Create the pipeline to run each of the stages
pipeline = Pipeline(stages = [tokenizer, indexer, stopwords, ngram, hashtf, randforest, unindexer])

model = pipeline.fit(training_data)
predictions = model.transform(test_data)

print(predictions.select('prediction_label', 'label').show())

evaluator = MulticlassClassificationEvaluator(labelCol="label_index", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Error = %g" % (1.0 - accuracy))
