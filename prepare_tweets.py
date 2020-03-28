import argparse
import os

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
            with open(f"RAW_DIR/{filename}") as file:
                for line in file:
                    print(json.loads(line)['tweet'])