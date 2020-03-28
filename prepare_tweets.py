import argparse

def get_tweets(keyword):
    try:
        os.mkdir(f"./data/raw/tweets")
    except:
        pass
    c = twint.Config()
    c.Search = keyword
    c.Lang = "en"
    c.Store_json = True
    c.Output = f"./data/raw/tweets/tweets_{keyword}.json"
    twint.run.Search(c)

def scrape():
    import twint
    get_tweets("coronavirus")
    get_tweets("CDC")

def main():
    parser = argparse.ArgumentParser(description='Generate finetuning corpus for tweets.')
    parser.add_argument('--scrape',
                        action='store_true',
                        help='scrape tweets about COVID-19')
    parser.add_argument('--large',
                        action='store_true',
                        help='export large corpus (10 mio), default is 1 mio')
    args = parser.parse_args()