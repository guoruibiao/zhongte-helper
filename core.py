# coding: utf8
from jieba import analyse

def get_keywords(fulltext):
    tags = analyse.textrank(fulltext, topK=10, withWeight=False)
    keywords = []
    for tag in tags:
        if tag == "":
            continue
        keywords.append(tag)
    return keywords

