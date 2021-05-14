import docx2txt
from datetime import date, timedelta
import os
import io
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')


class Helper:
    def __init__(self):
        self.stop_words = stopwords.words('english')

    def cleanTextAndTokenize(self, text):

        # KEEP ALPHABATES, SPACE
        # LOWER CASE
        text = re.sub('[^A-Za-z ]+', ' ', text).lower()
        tokens = word_tokenize(text)
        cleanToken = []
        for token in tokens:
            if(token not in self.stop_words):
                cleanToken.append(token)
        return cleanToken

    # def createDictionary(self, ex):
    #     '''
    #     url = "https://hrlanesprodstorage1.blob.core.windows.net/public/master.json"
    #     master = requests.get(url)
    #     data = master.json()
    #     '''
    #     path = os.getcwd()+"/"
    #     with open(path+"master.json", encoding='utf-8') as dataFile:
    #         data = json.load(dataFile)

    #     obj_ind = data['IndustryData']
    #     broad = data['BroadAreaData']
    #     country = data['countryData']
    #     exp = [i['value'] for i in data['ExperienceData']]
    #     ind = {}
    #     for i in obj_ind:
    #         ind[i['value']] = i['label']
    #     farea = {}
    #     subf = {}
    #     for f in broad:
    #         farea[f['value']] = f['label']
    #         if 'sub' in f:
    #             subf[f['value']] = f['sub']
    #     con = {}
    #     for c in country:
    #         con[c['value']] = c['label']

    #     #dictionary: {(func_area, exp): [(cand_id1, match_text), (cand_id2, match_text)..], ...}
    #     hard_filter = []
    #     for i in farea:
    #         for j in exp:
    #             hard_filter.append((i,j))
    #     try:
    #         d = pickle.load("dictionary.pkl", "rb+")
    #     except:
    #         d = {}
    #         for filter in hard_filter:
    #             d[filter] = []

    #     for item in ex:
    #         text = ''
    #         hp_text = ''
    #         if 'ProfileName' in item['ProfileSummaryInfo']:
    #             text+=item['ProfileSummaryInfo']['ProfileName']
    #             hp_text+=item['ProfileSummaryInfo']['ProfileName']
    #         if 'Industry' in item['ProfileSummaryInfo']:
    #             text+=' '
    #             text+=ind[item['ProfileSummaryInfo']['Industry']]
    #         if 'FunctionalAreas' in item['ProfileSummaryInfo'] and item['ProfileSummaryInfo']['FunctionalAreas']!= None:
    #             for i in range(len(item['ProfileSummaryInfo']['FunctionalAreas'])):
    #                 if 'FunctionValue' in item['ProfileSummaryInfo']['FunctionalAreas'][i]:
    #                     f = item['ProfileSummaryInfo']['FunctionalAreas'][i]['FunctionValue']
    #                     text += ' '
    #                     text+=farea[f]
    #                     for j in range(len(item['ProfileSummaryInfo']['FunctionalAreas'][i]['SubFunValue'])):
    #                         sf = item['ProfileSummaryInfo']['FunctionalAreas'][i]['SubFunValue'][j]
    #                         for s in data[subf[f]]:
    #                             text+=' '
    #                             hp_text+=' '
    #                             if s['value']==sf:
    #                                 text+=s['label']
    #                                 hp_text+=s['label']
    #                                 break
    #         if 'FileName' in item['ProfileSummaryInfo'] and item['ProfileSummaryInfo']['FileName'] != None:
    #             fname = item['ProfileSummaryInfo']['FileName']
    #             userid = item['_id']
    #             fpath = 'https://hrlanesprodstorage1.blob.core.windows.net/container'+str(userid)+'/resume/'+fname+'?sv=2019-10-10&ss=b&srt=co&sp=r&se=2099-06-08T13:36:56Z&st=2020-06-08T05:36:56Z&spr=https&sig=Nx2rJ734l%2BBiTpJGpReuNizfg%2BgGa1jlyFs8cXjE76I%3D'
    #             try:
    #                 r = requests.get(fpath)
    #                 f = io.BytesIO(r.content)
    #                 reader = PyPDF2.PdfFileReader(f)
    #                 pages =  reader.getNumPages()
    #                 pdftext = ''
    #                 for i in range(pages):
    #                     pdftext += reader.getPage(i).extractText()
    #                     text+=' '
    #                     text+=pdftext
    #             except:
    #                 text+=' '
    #         if 'EducationDetails' in item['ProfileSummaryInfo'] and item['ProfileSummaryInfo']['EducationDetails']!= None:
    #             text+=' '
    #             for i in range(len(item['ProfileSummaryInfo']['EducationDetails'])):
    #                 text+=item['ProfileSummaryInfo']['EducationDetails'][i]['AreaOfStudy']
    #                 text+=' '
    #                 text+=item['ProfileSummaryInfo']['EducationDetails'][i]['Degree']
    #                 text+=' '
    #                 text+=item['ProfileSummaryInfo']['EducationDetails'][i]['Description']
    #                 text+=' '
    #         if 'EmploymentDetails' in item['ProfileSummaryInfo'] and item['ProfileSummaryInfo']['EmploymentDetails']!= None:
    #             for i in range(len(item['ProfileSummaryInfo']['EmploymentDetails'])):
    #                 text+=item['ProfileSummaryInfo']['EmploymentDetails'][i]['Company']
    #                 text+=' '
    #                 text+=item['ProfileSummaryInfo']['EmploymentDetails'][i]['Location']
    #                 text+=' '
    #                 text+=con[item['ProfileSummaryInfo']['EmploymentDetails'][i]['Country']]
    #                 text+=' '
    #                 text+=item['ProfileSummaryInfo']['EmploymentDetails'][i]['Title']
    #                 text+=' '
    #                 text+=item['ProfileSummaryInfo']['EmploymentDetails'][i]['Role']
    #                 text+=' '
    #         if 'ProjectDetails' in item['ProfileSummaryInfo']and item['ProfileSummaryInfo']['ProjectDetails']!= None:
    #             for i in range(len(item['ProfileSummaryInfo']['ProjectDetails'])):
    #                 text+=item['ProfileSummaryInfo']['ProjectDetails'][i]['Title']
    #                 text+=' '
    #                 text+=item['ProfileSummaryInfo']['ProjectDetails'][i]['RoleAndResponsibility']
    #                 text+=' '
    #                 text+=item['ProfileSummaryInfo']['ProjectDetails'][i]['DescriptionAndDeliverables']
    #                 text+=' '
    #         if 'OtherDetailsInfo' in item:
    #             text+=item['OtherDetailsInfo']['Overview']
    #             text+=' '
    #         if 'LocationInfo' in item:
    #             text+=item['LocationInfo']['City']
    #             text+=' '
    #         if 'ExperienceLevel' in item['ProfileSummaryInfo']:
    #             e = item['ProfileSummaryInfo']['ExperienceLevel']
    #             for i in range(len(item['ProfileSummaryInfo']['FunctionalAreas'])):
    #                 fid = item['ProfileSummaryInfo']['FunctionalAreas'][i]['FunctionValue']
    #                 if (fid,e) not in d:
    #                     d[(fid,e)] = []
    #                 d[(fid,e)].append((item['_id'], self.cleanTextAndTokenize(text), self.cleanTextAndTokenize(hp_text)))
    #     return d

    # def create_tfidf(self, name, documents, included, flag):
    #     #name: (fid, e)
    #     #documents: JD or HP based on flag (0: JD; 1: HP)
    #     #included: corresponding candidate IDs for included documents
    #     path = os.getcwd()+"/active/"  #forward slash

    #     if flag==0:
    #         '''
    #             JD
    #         '''
    #         dict_name = "_resume.dict"
    #         model_name = "_tfidf.model"
    #         sim_obj_name = "_similarity_index.0"
    #         with open(path+str(name)+"_doc_included.list", "wb+") as fp:
    #             pickle.dump(included, fp)
    #     elif flag==1:
    #         '''
    #             HP
    #         '''
    #         dict_name = "_hp_resume.dict"
    #         model_name = "_hp_tfidf.model"
    #         sim_obj_name = "_hp_similarity_index.0"
    #     dictionary = gensim.corpora.Dictionary(documents)
    #     with open(path+str(name)+dict_name, "wb+") as fp:
    #         pickle.dump(dictionary, fp)
    #     corpus = [dictionary.doc2bow(text) for text in documents]
    #     model = gensim.models.TfidfModel(corpus)
    #     model.save(path+str(name)+model_name)
    #     index_tmpfile = get_tmpfile('similarity_object')
    #     similarity_object = gensim.similarities.Similarity(index_tmpfile,model[corpus],num_features=len(dictionary))
    #     similarity_object.save(path+str(name)+sim_obj_name)

    # def compute_similarity(self, name, cleanToken_jd, cleanToken_hp):
    #     try:
    #         '''
    #             JD
    #         '''
    #         path = os.getcwd()+"/active/"  #forward slash
    #         dictionary_jd = gensim.corpora.Dictionary.load(path+str(name)+"_resume.dict")
    #         model_jd = gensim.models.TfidfModel.load(path+str(name)+"_tfidf.model")
    #         similarity_obj_jd = gensim.similarities.Similarity.load(path+str(name)+"_similarity_index.0")
    #         doc_included = list(pickle.load(open(path+str(name)+"_doc_included.list", "rb+")))
    #         cleaned_bow_jd = dictionary_jd.doc2bow(cleanToken_jd) #bag of words of job description
    #         cleaned_tfidf_jd = model_jd[cleaned_bow_jd] #tfidf of JD
    #         sim_scores_jd = similarity_obj_jd[cleaned_tfidf_jd]
    #         '''
    #             HW (subfn + title)
    #         '''

    #         dictionary_hp = gensim.corpora.Dictionary.load(path+str(name)+"_hp_resume.dict")
    #         model_hp = gensim.models.TfidfModel.load(path+str(name)+"_hp_tfidf.model")
    #         similarity_obj_hp = gensim.similarities.Similarity.load(path+str(name)+"_hp_similarity_index.0")
    #         cleaned_bow_hp = dictionary_hp.doc2bow(cleanToken_hp) #bag of words of job description
    #         cleaned_tfidf_hp = model_hp[cleaned_bow_hp] #tfidf of JD
    #         sim_scores_hp = similarity_obj_hp[cleaned_tfidf_hp]

    #         scores = []
    #         for i in range(len(doc_included)):
    #             scores.append((sim_scores_jd[i]+sim_scores_hp[i],doc_included[i]))
    #         return scores
    #     except:
    #         return []

    # def recommend(self, ex, fn, cleanToken_jd, cleanToken_hp):
    #     '''
    #         Function takes in experience, functional area, tokenized job description and recommends candidate IDs
    #     '''
    #     result_scores = []
    #     for i in range(int(ex)-1, int(ex)+2):
    #         if i>0 and i<5:
    #             name = (int(fn),i)
    #             scores = self.compute_similarity(name, cleanToken_jd, cleanToken_hp)
    #             if len(scores)!=0:
    #                 for s in scores:
    #                     result_scores.append(s)
    #     sscores = []
    #     if(len(result_scores)!=0):
    #         result_scores.sort(reverse = True)
    #         for (i,j) in result_scores:
    #             sscores.append((j,i))
    #     return sscores

    #     '''
    #     name = (int(fn),int(ex))
    #     try:
    #     '''
    #             #JD
    #     '''
    #         l = []
    #         path = os.getcwd()+"/active/"  #forward slash
    #         dictionary_jd = gensim.corpora.Dictionary.load(path+str(name)+"_resume.dict")
    #         model_jd = gensim.models.TfidfModel.load(path+str(name)+"_tfidf.model")
    #         similarity_obj_jd = gensim.similarities.Similarity.load(path+str(name)+"_similarity_index.0")
    #         doc_included = list(pickle.load(open(path+str(name)+"_doc_included.list", "rb+")))
    #         cleaned_bow_jd = dictionary_jd.doc2bow(cleanToken_jd) #bag of words of job description
    #         cleaned_tfidf_jd = model_jd[cleaned_bow_jd] #tfidf of JD
    #         sim_scores_jd = similarity_obj_jd[cleaned_tfidf_jd]
    #     '''
    #             #HW (subfn + title)
    #     '''

    #         dictionary_hp = gensim.corpora.Dictionary.load(path+str(name)+"_hp_resume.dict")
    #         model_hp = gensim.models.TfidfModel.load(path+str(name)+"_hp_tfidf.model")
    #         similarity_obj_hp = gensim.similarities.Similarity.load(path+str(name)+"_hp_similarity_index.0")
    #         cleaned_bow_hp = dictionary_hp.doc2bow(cleanToken_hp) #bag of words of job description
    #         cleaned_tfidf_hp = model_hp[cleaned_bow_hp] #tfidf of JD
    #         sim_scores_hp = similarity_obj_hp[cleaned_tfidf_hp]
    #         scores = []

    #         for i in range(len(doc_included)):
    #             scores.append((sim_scores_jd[i]+sim_scores_hp[i],doc_included[i]))
    #         scores.sort(reverse = True)
    #         sscores = []
    #         for (i,j) in scores:
    #             sscores.append((j,i))

    #         return sscores

    #     except:
    #         return []
    #     '''
    # def extract_text_from_url(self, url):
    #     try:
    #         if(url.endswith('.pdf')):
    #             r = requests.get(url)
    #             f = io.BytesIO(r.content)
    #             reader = PyPDF2.PdfFileReader(f)
    #             pages =  reader.getNumPages()
    #             text = ''
    #             for i in range(pages):
    #                 text += reader.getPage(i).extractText()
    #             return text
    #         elif(url.endswith('.docx')):
    #             text+= docx2txt.process(url).decode('utf8')
    #             return text
    #     except:
    #         text+=' '
    #         return text

    # def create_backup(self):
    #     #upload files from local to blob
    #     yesterday = str(date.today() - timedelta(days=1))
    #     connect_str = "DefaultEndpointsProtocol=https;AccountName=hrlanesprodstorage1;AccountKey=uMn+xHl9M/BPjlduv2UORBzY8PUeitrL264NI04Y9qS+XzB0W30EyCj9Sa3z9vtrnMWb3GZqFhWqifN5TSmH/g==;EndpointSuffix=core.windows.net"
    #     # Create the BlobServiceClient object which will be used to create a container client
    #     blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    #     path = os.getcwd()+'/active/'
    #     files= []
    #     for r, d, f in os.walk(path):
    #         for filename in f:
    #             blob_client = blob_service_client.get_blob_client(container='cand-recom', blob = yesterday+"/"+filename)
    #             with open(os.path.join(r, filename), "rb") as data:
    #                blob_client.upload_blob(data, overwrite=True)

    #     #run build model
    #     #save new files on local (create tfidf does this)
