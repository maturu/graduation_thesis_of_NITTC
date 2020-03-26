import math
import glob
import re
from textblob import TextBlob
import os
import urllib
import urllib3
import urllib.request
import urllib.parse
import json
import collections as cl
import MeCab
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tqdm import tqdm
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class GetWebInfomation(object):
    """ Get Website Infomation class

    Parameters
    ------------
    corpus : list
        Document group of each report
    theme : str
        Homework theme
    k : int
        Search number of website
    query : list
        Words for Web search extracted from corpus

    Attributes
    ------------
    self : Object

    """
    def __init__(self, corpus, theme="数値計算", k=10, docx_paths=[]):
        self.theme = theme
        self.k = int(k/10)
        self.fname = docx_paths
        self.corpus = self.__remove_noise(corpus)
        self.query = self.query()

    def get(self):
        """ Search and Get website infomation """
        index = 0
        fr = open('result.json', 'r')
        result_json = json.load(fr)
        fr.close()

        fw = open('result.json', 'w')
        for q in self.query:
            items_list = []
            for p in range(1, self.k+1):
                # Google API settings
                QUERY = self.theme+" "+q
                API_KEY = 'AIzaSyAjComOta6ke4BWWBLE49u34mdo_Tx0Jwo'
                CUSTOM_SEARCH_ID = '017928256044772830552:ot_23aweaoy'
                request_url = 'https://www.googleapis.com/customsearch/v1?'
                params = {
                        'key': API_KEY,
                        'q': QUERY,
                        'cx': CUSTOM_SEARCH_ID,
                        'alt': 'json',
                        'lr': 'lang_ja'
                        }

                # web infomation
                params['start'] = p
                request_url = request_url + urllib.parse.urlencode(params)
                try:
                    response = urllib.request.urlopen(request_url)
                    json_body = json.loads(response.read().decode('utf-8'))
                    items = json_body['items']
                except:
                    print('SearchError: can not get the url.')
                items_list.extend(items)

            # download
            options = Options()
            options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
            options.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=options)
            result_json[self.fname[index]] = {}
            for i in range(len(items_list)):
                url = items_list[i]['link']
                print("----------------------------------------------------------------")
                print(url)
                result_json[self.fname[index]]['./data/webinfo/'+str(index)+'-'+str(i)+'.txt'] = {'url': url}
                if "pdf" in url:
                    try:
                        # download pdf information
                        urllib.request.urlretrieve(url, './data/webinfo/'+str(index)+'-'+str(i)+'.pdf')
                        rsrcmgr = PDFResourceManager()
                        rettxt = StringIO()
                        laparams = LAParams()
                        laparams.detect_vertical = True
                        device = TextConverter(rsrcmgr, rettxt, codec='utf-8', laparams=laparams)
                        fp = open('./data/webinfo/'+str(index)+'-'+str(i)+'.pdf', 'rb')
                        interpreter = PDFPageInterpreter(rsrcmgr, device)
                        for page in PDFPage.get_pages(fp, pagenos=None, maxpages=0, password=None,caching=True, check_extractable=True):
                            interpreter.process_page(page)
                        save_file = open('./data/webinfo/'+str(index)+'-'+str(i)+'.txt', 'w')
                        save_file.write(rettxt.getvalue())
                        fp.close()
                        device.close()
                        rettxt.close()
                        save_file.close()
                    except:
                        print("DownloadError: A timeout occurred when downloading a web page or it could not be saved in a file.")
                        save_file = open('./data/webinfo/'+str(index)+'-'+str(i)+'.txt', 'w')
                        save_file.close()
                else:
                    # download web information
                    try:
                        driver.get(url)
                        html = driver.page_source
                        soup = BeautifulSoup(html, "lxml")
                        for s in soup(['script', 'style', 'iflame', 'a', 'img']):
                            s.decompose()
                        # save txt file
                        save_file = open('./data/webinfo/'+str(index)+'-'+str(i)+'.txt', 'w')
                        save_file.write(''.join(soup.stripped_strings))
                        save_file.close()
                    except:
                        print("DownloadError: A timeout occurred when downloading a web page or it could not be saved in a file.")
                        save_file = open('./data/webinfo/'+str(index)+'-'+str(i)+'.txt', 'w')
                        save_file.close()
            driver.quit()
            print("----------------------------------------------------------------")
            index += 1
        json.dump(result_json, fw, indent=4)
        fw.close()

        return self

    def __remove_noise(self, corpus):
        """ Regular Expressions and Morphological Analysis """
        noun_sentence_list = []
        for c in corpus:
            # MeCab
            mecab = MeCab.Tagger('/usr/local/lib/mecab/dic/mecab-ipadic-neologd')
            mecab.parse('')
            node = mecab.parseToNode(c)

            # SlothLib
            slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
            slothlib_file = urllib.request.urlopen(slothlib_path)
            slothlib_stopwords = [line.decode("utf-8").strip() for line in slothlib_file]
            slothlib_stopwords = [ss for ss in slothlib_stopwords if not ss==u'']
            slothlib_stopwords += ['{', '}', '(', ')', "[", "]", '\\', '/', 'displaystyle', 'sqrt', '@']
            slothlib_stopwords += ['｛', '｝', '（', '）', "「", "」", '￥', '＠']
            slothlib_stopwords += ['+', '-', '=', '*']
            slothlib_stopwords += ['＋', 'ー', '＝', '✕', "÷"]

            # extracting only nouns
            noun_words = []
            noun_sentence = ""
            while node:
                if node.feature.startswith('名詞'):
                    word = node.surface
                    noun_words.append('{0}'.format(word))
                node = node.next
            for nw in noun_words:
                if not nw in slothlib_stopwords:
                    noun_sentence = noun_sentence + nw + " "
            noun_sentence = re.sub(r'[0-9]', "", noun_sentence)
            noun_sentence = re.sub(r'[０-９]', "", noun_sentence)
            noun_sentence_list.append(noun_sentence)

        return noun_sentence_list

    def query(self):
        """ Extract search words """
        query_list = []
        for i in range(0, len(self.corpus)):
            query = ""
            for j in range(0, 3):
                # order desc
                keyword, score = sorted(self.tfidf()[i].items(), key=lambda x: -x[1])[j]
                query = query + keyword + " "
            query_list.append(query)
        return query_list

    def tfidf(self):
        """ Calculate TF-IDF of each report """
        tfidf_scores = []
        dict_scores = {}

        alphaReg = re.compile(r'^[a-zA-Z]+$')
        for c in self.corpus:
            blob = TextBlob(c)
            dict_scores = {}
            for word in blob.words:
                if alphaReg.match(word) is not None and len(word) <= 3:
                    continue
                tf = blob.words.count(word) / len(blob.words)
                df = 0
                for c in self.corpus:
                    if word in c:
                        df += 1
                idf = math.log(len(self.corpus) / df)
                dict_scores[word] = tf*idf
            tfidf_scores.append(dict_scores)
        return tfidf_scores

