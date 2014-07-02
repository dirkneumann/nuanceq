import simplejson as json
import numpy as np
import spark
import text_nltk
import sys


def annotate_skip(x):
    try:
        headline = x["headline"]["main"]
        lead_paragraph = x["lead_paragraph"]
        h1 = text_nltk.semantic_vector_skip(headline, model='vectors_25d')
        if not h1:
            return []
        l1 = text_nltk.semantic_vector_skip(
            lead_paragraph, model='vectors_25d')
        if not l1:
            return []
        h2 = text_nltk.semantic_vector_skip(
            headline, model='twitter_vectors_25d')
        if not h2:
            return []
        l2 = text_nltk.semantic_vector_skip(
            lead_paragraph, model='twitter_vectors_25d')
        if not l2:
            return []
        h3 = text_nltk.semantic_vector_skip(
            headline, model='GoogleNews-vectors-negative300')
        if not h3:
            return []
        l3 = text_nltk.semantic_vector_skip(
            lead_paragraph, model='GoogleNews-vectors-negative300')
        if not l3:
            return []
        y = {
            "headline_main_vectors_25d":  h1,
            "lead_paragraph_vectors_25d": l1,
            "headline_main_twitter_vectors_25d":  h2,
            "lead_paragraph_twitter_vectors_25d": l2,
            "headline_main_GoogleNews-vectors-negative300":  h3,
            "lead_paragraph_GoogleNews-vectors-negative300": l3,
            "headline": x["headline"]["main"],
        }
        for k in ["_id", "pub_date", "query", "web_url"]:
            y[k] = x[k] if k in x else ""
        return [y]
    except KeyError:
        return []


def nyt(source, target):
    spark.data(source, cores=16)   \
        .flatMap(lambda x: annotate_skip(x))  \
        .map(json.dumps)   \
        .saveAsTextFile(target)

if __name__ == '__main__':
    nyt()
