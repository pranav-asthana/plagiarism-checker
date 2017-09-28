import argparse
from nltk import wordpunct_tokenize
from tf_idf import *

def get_keywords(text):
    text = text.split()
    text = [word for word in text if word not in nltk.corpus.stopwords.words('english')] # remove stopwords
    biwords = [[text[i], text[i+1]] for i in range(len(text) - 1)]
    biwords = [' '.join(pair) for pair in biwords]
    searches = 0
    keywords = []
    for pair in biwords:
        tf = biwords.count(pair)
        if searches < 5:
            print(tf, pair)
            keywords.append(pair)
            searches += 1
        if tf > 1:
            print(tf, pair)
            keywords.append(pair)
        if len(pair) > 25:
            print(tf, pair)
            keywords.append(pair)
    return list(set(keywords))

def scrape_data(url):
    import requests
    from bs4 import BeautifulSoup

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.find_all('p')
    text = ''.join([t.text for t in text])
    return text

def retrive_from_google(query, num_pages = 5):
    print('Searching google for "', query, '" ...')
    import google_search as google
    import os
    response = google.search(query, stop = num_pages)
    results = {}
    cache = [''.join(fname.split('.')[:-1]) for fname in os.listdir('google_retrieved')]
    pbar = ProgressBar()
    for link in pbar(response):
        fname = ''.join(link.split('/'))
        if fname not in cache:
            text = scrape_data(link)
            cache.append(link)
            open(os.path.join('google_retrieved', fname), 'w').write(text)
    return results

def main():
    parser = argparse.ArgumentParser(
                description='Fetch similar documents from Google')
    parser.add_argument('text_file', type=str,
                        help='Path to text file for checking')
    args = parser.parse_args()
    target_file = args.text_file

    text = open(target_file).read()
    keywords = get_keywords(text)

    for keyword in keywords:
        retrive_from_google(keyword)


if __name__ == "__main__":
    main()