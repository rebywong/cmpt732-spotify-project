
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types, Row

song_schema = types.StructType([
        types.StructField('track_id', types.StringType()),
        types.StructField('lyrics', types.StringType()),
        types.StructField('language', types.StringType()),
    ])
    

def main(input,output,output1):
    df = spark.read.json(input,schema=song_schema).cache()
    

    df.createOrReplaceTempView('goup')
    combined_df = spark.sql("""
    SELECT distinct language
    FROM goup
    where language != 'no'                        
""")
    #combined_df.write.csv(output,mode='append',header=True)
    combined_df.write.csv(output,mode='append',header=True)
    par_lan = spark.sql("""
    SELECT *
    FROM goup
    where language is not NULL and lyrics is not NULL                        
""").cache()
    
    par_lan.coalesce(1).write.json(output, mode="append")
    par_lan.write.partitionBy("language").parquet(output1, mode="append")

    

if __name__ == '__main__':
    inputs = sys.argv[1]
    output = sys.argv[2]
    output1 = sys.argv[3]
    spark = SparkSession.builder.appName('reddit average df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    
    sc = spark.sparkContext
    main(inputs, output, output1)
    #main(output)