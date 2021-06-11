import docx2txt
import nltk
from Helper import Helper
# import spacy
import os
import pickle
from pprint import pprint
from fnmatch import fnmatch
from gensim.models import TfidfModel
from gensim import corpora, similarities


# import fse

from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io

resumeList = []

File_Root_Path = "E:\\@Prasoon\\NonGoogleDrive\\@MetalBrain\\HRLanes\\Resumes"
for (root, dirs, files) in os.walk(File_Root_Path, topdown=True):
    for name in files:
        if fnmatch(name, "*.pdf") or fnmatch(name, "*.docx"):
            resumeList.append(os.path.join(root, name))

# List of Tokens of each document
documents = []
document_included = []

helper = Helper()
#spacyEnModel = spacy.load('en_core_web_sm')

# READ ALL FILE FRON LIST AND CREATE documents
for filePath in resumeList:
    print(filePath)
    if (filePath.endswith('.docx')):
        documents.append(helper.cleanTextAndTokenize(
            docx2txt.process(filePath).decode('utf8')))
        document_included.append(filePath)
    elif filePath.endswith('.pdf'):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(
            resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(filePath, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)
        pdfText = fake_file_handle.getvalue()
        documents.append(helper.cleanTextAndTokenize(pdfText))
        # close open handles
        converter.close()
        fake_file_handle.close()
        document_included.append(filePath)

# Store document_included list to show results
with open('saved/document_included.list', 'wb') as fp:
    pickle.dump(document_included, fp)


dictionary = corpora.Dictionary(documents)

corpus = [dictionary.doc2bow(doc) for doc in documents]

dictionary.save("saved/resume.dict")
corpora.MmCorpus.serialize("saved/resume-corpus.mm", corpus)

tfidf = TfidfModel(corpus)
tfidf.save("saved/tfidf.model")

matrixSims = similarities.MatrixSimilarity(tfidf[corpus])
matrixSims.save("saved/tfidf_similarity.index")


# w2vModel = Word2Vec(corpus, min_count=1)
# sifModel = fse.models.Sentence2Vec(w2vModel)
# sentences_emb = sifModel.train(corpus)

# pprint(sentences_emb)
