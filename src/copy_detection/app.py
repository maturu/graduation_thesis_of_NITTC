import glob
from docx import Document
from GetWebInfomation import GetWebInfomation
from PlagiarismDetection import PlagiarismDetection
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main():
    args = sys.argv
    if len(args) >= 2:
        if args[1] in ['--download','-d']:
            theme = input("Enter homework theme >>")
    alpha, k = 0, 0
    while True:
        if alpha in [5, 10, 15, 20]:
            break
        alpha = int(input("alpha=5,10,15,20 >>"))
    while True:
        if k in [10, 20, 30]:
            break
        k = int(input("k=10,20,30 >>"))

    corpus = []
    path = './data/simulation_repo/*.docx'
    docx_paths = glob.glob(path)
    docx_paths.sort()
    print(docx_paths)
    for dp in docx_paths:
        text = ""
        doc = Document(dp)
        for para in doc.paragraphs:
            text = text + para.text
        corpus.append(text)

    if len(args) >= 2:
        if args[1] in ['--download','-d']:
            gwi = GetWebInfomation(corpus, theme, k, docx_paths)
            print(gwi.query)
            gwi.get()

    webinfo = []
    for c in corpus:
        stack = []
        for i in range(0, k):
            fnum = corpus.index(c)
            fpath = "./data/webinfo/"+str(fnum)+"-"+str(i)+".txt"
            f = open(fpath, "r", encoding="utf-8")
            stack.append(f.read())
        webinfo.append(stack)

    pd = PlagiarismDetection(alpha, docx_paths)
    pd.compare(corpus, webinfo)
    print(pd.rpart_)
    print(pd.wpart_)
    print(pd.rate_)

    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    x_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    plt.bar(x, pd.rate_, align="center", width=0.5)
    plt.grid(True)
    plt.xticks(x, x_num)
    plt.savefig('result.png')

if __name__ == '__main__':
    main()
