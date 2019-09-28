import requests, json, os
from elasticsearch import Elasticsearch
from ssl import create_default_context


"""
Frontend will make a POST request,  
we have to convert it to a query to call this func get_recent_query_data_from_dj
"""
def get_recent_query_data_from_dj(query):
    query = query.replace("AG", "").replace("Corp", "")
    
    ress = es.search(index="dj", body={"query": {
                                       "query_string": {
                                               "query" : query,
                                               "fields" : ['title','snippet', 'body']
                                           }
                                       },
                                       "size" : 5,
                                        "sort":
                                        {  
                                           "publication_datetime":{  
                                              "order":"asc"
                                           }
                                        }
                                    })
    return ress['hits']['hits']