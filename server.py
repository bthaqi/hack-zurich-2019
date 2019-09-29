from flask import Flask
import json
import requests, json, os
from elasticsearch import Elasticsearch
from ssl import create_default_context
from flask_cors import CORS

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

analyzer = SentimentIntensityAnalyzer()
context = create_default_context(cafile="client.cer")
es = Elasticsearch(['https://data.schnitzel.tech:9200'], http_auth=('hack_zurich', 'punctualunicorns'), ssl_context=context)


@app.route('/recent-query/<query>')
def get_recent_query_data(query):
    results = es.search(index="isp", body={"query": 
        {
            "match_phrase":{
                "d": query
            }
        },
        "sort":
        {  
            "tm":{  
                "order":"asc"
            }
        }
        })
    return json.dumps(results['hits']['hits'])


@app.route('/recent-query-dj/<query>')
def get_recent_query_data_from_dj(query):
    data = []
    query = query.replace("AG", "").replace("Corp", "")
    
    result = es.search(index="dj", body={"query": {
        "query_string": {
                "query" : query,
                "fields" : ['title','snippet', 'body']
            }
        },
        "size" : 10,
        "sort":
        {  
            "publication_datetime":{  
                "order":"asc"
            }
        }
    })
    art = 0
    for item in result['hits']['hits']:
        vs = analyzer.polarity_scores(item['_source']['body'])
        item['_source'].update(vs)
        data.append(item['_source'])
        print("{} {}".format(art, str(vs)))
        art += 1    
    return json.dumps(data)


@app.route('/past-six-months/<query>/<interval>')
def get_past_six_months_trend(query, interval):
    data = []
    data_list = []
    query = query.replace("AG", "").replace("Corp", "")
    
    result = es.search(index="dj", body={
        "query": {
            "bool": {
               "must": [
                   {
                       "match": {
                           "snippet":query
                       },
                   },
                   {
                       "match": {
                           "body":query
                       }
                   },
                   {
                       "match": {
                           "title":query
                       }
                   }
               ], "filter": {
                       "range" : {
                            "publication_datetime" : {
                                "gte" : "now-6M",
                                "lt" :  "now"
                            }
                        }
                   }
            }
        },
        "size" : 0,
        "aggs" : {
            "publication_datetime" : {
                "date_histogram" : {
                    "field" : "publication_datetime",
                    "interval" : interval
                },
                "aggs": {
                    "publication_datetime": {
                        "terms": {
                            "field": "publication_datetime"
                        }
                    }
                },
            }
        }
    })
    
    for item in result["aggregations"]['publication_datetime']['buckets']:
        data_list.append({"time": item['key'], "count": item['doc_count']})
    return json.dumps(data_list)


if __name__ == '__main__':
    app.run()
