import argparse
import os
import json
import re
from tqdm import tqdm
import spacy

RAW_DIR = "./data/raw/tweets"
TRANS_DIR = "./data/transformed/tweets"

def get_tweets(keyword):
    c = twint.Config()
    c.Search = keyword
    c.Lang = "en"
    c.Store_json = True
    c.Output = f"{RAW_DIR}/tweets_{keyword}.json"
    twint.run.Search(c)

def scrape():
    import twint
    try:
        os.mkdir(RAW_DIR)
    except:
        pass
    get_tweets("coronavirus")
    get_tweets("CDC")

def sentence_segment_filter_docs(doc_array):
    # get sentence segemented review with #sentences > 2
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    sentences = []
    for doc in nlp.pipe(doc_array, disable=['parser', 'tagger', 'ner'], batch_size=1000, n_threads=8):
        sentences.append([sent.text.strip() for sent in doc.sents])
    return sentences

def main():
    parser = argparse.ArgumentParser(description='Generate finetuning corpus for tweets.')
    parser.add_argument('--scrape',
                        action='store_true',
                        help='scrape tweets about COVID-19')
    args = parser.parse_args()
    
    if args.scrape:
        scrape()
    
    tweets = []
    for filename in os.listdir(RAW_DIR):
        if filename.endswith(".json"):
            with open(f"{RAW_DIR}/{filename}") as file:
                for line in file:
                    tweet = json.loads(line)['tweet']
                    no_url = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet, flags=re.MULTILINE)
                    tweets.append(no_url)
    
    print(f'Found {len(tweets)} tweets')
    print(f'Tokenizing tweets...')

    sentences = sentence_segment_filter_docs(tweets)
    nr_sents = sum([len(s) for s in sentences])
    print(f'Segmented {nr_sents} tweet sentences')

    with open(f"{TRANS_DIR}/tweet_corpus.txt", "w") as f:
        for sents in tqdm(sentences):
            real_sents = []
            for s in sents:
                x = s.replace(' ', '').replace('\n', '').replace('\u200d', '').replace('\u200b', '')
                if x != '':
                   real_sents.append(s.replace('\n', '').replace('\u200d', '').replace('\u200b', ''))
            if len(real_sents) >= 2:
                str_to_write = "\n" + "\n".join(real_sents) + "\n"
                f.write(str_to_write)

if __name__ == "__main__":
    main()