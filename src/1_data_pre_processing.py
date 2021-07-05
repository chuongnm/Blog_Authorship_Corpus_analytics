#NOTICE: read the README file before run the code
#link for the raw data: https://u.cs.biu.ac.il/~koppel/BlogCorpus.htm
#####STEP 1: DATA PRE-PROCESSING#######
##set the deffault link
import os
os.chdir("link") #link to folder of extracted data


#STEP 1.1: BLOGGER DATA####
#create all file list
blogger_list=os.listdir("link") #link to folder of extracted data



#set function convert list to string
def ListToStr(s):
    str1 = ""
    for ele in s:
        str1 += ele
    # return string   
    return str1  

#convert file list to string
blogger_data = ListToStr(blogger_list)
blogger_data = blogger_data.replace('xml','xml\n')

#convert to string
import io
blogger_data = io.StringIO(blogger_data)


#convert string to dataframe
import pandas as pd
blogger_data = pd.read_csv(blogger_data, sep=".",names=['id','gender','age',
                                                        'industry','astrology','file_name'])
#set orginal file_name after split
blogger_data['file_name'] = blogger_list


#STEP 1.2: PARSING BLOG CONTENT 
#use BS to parse XML#
from bs4 import BeautifulSoup   

#set data_blog 
data_blog =pd.DataFrame(columns=['file_name','date','post'])

#for loop to extract each file
for i in blogger_list:
    file = open(i,'r',encoding='latin1') #open file xml
    contents = file.read() #convert to string
    
    #parse xml
    soup = BeautifulSoup(contents,'xml')
    date = soup.find_all('date') #take all date content
    post = soup.find_all('post') #take all post content
    
    data = [] #create blank list
    for i in range(0,len(date)):
        rows = [file.name,date[i].get_text(),post[i].get_text()] #split content of each post and date
        data.append(rows) # merge to list
        df = pd.DataFrame(data,columns = ['file_name','date', 'post']) #convert to dataframe
    data_blog = data_blog.append(df) #merge to data_blog


#check missing value
print(data_blog.isnull().sum()) 

#create blogger info for data_blog from data_blogger 
data_blog=data_blog.merge(blogger_data\
                          [['file_name','id','gender','age','industry','astrology']]\
                              , on='file_name', how='right')


#set new variable for date, keep the original variable    
data_blog['datetime'] = data_blog['date']

 


#STEP 1.3  STANDARDLIZING DATE
#list month with other langue
month_convert  =  ['janvier', 'mars', 'avril', 'mai', 'juin', 'juillet', '', 'agosto',
                   'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
                   'septiembre', 'octubre', 'noviembre', 'diciembre', 'Junho', 'Maio',
                   'juni', 'Aprill', 'Setembro', 'Novembro', 'Agosto', 'september',
                   'Julho', 'ottobre', 'giugno', 'luglio', 'toukokuu', 'Dezember',
                   'Januar', 'Februar', 'Mai', 'Juni', 'Juli', 'Jaanuar', 'Juuni',
                   'Juuli', 'Abril', 'juli', 'august', 'maart', 'mei', 'maj',
                   'czerwiec', 'lipiec', 'augustus', 'elokuu', 'septembrie',
                   'noiembrie', 'ianuarie', 'februarie', 'iulie', 'augusti', 'Avgust',
                   'Outubro', 'Dezembro', 'Janeiro', 'Fevereiro', 'kolovoz', 'lipanj',
                   'desember', 'septembre', 'octobre', 'novembre','Augustus','Augusti',
                   'Januaryy','Februaryy']

#respective list month with english 
month_eng   =     ['January','March','April','May','June','July','','August',
                   'January','February','March','April','May','June','July',
                   'September','October','November','December','June','May',
                   'June','April','September','November','August','September',
                   'July','October','June','July','May','December',
                   'January','February','May','June','July','January','June',
                   'July','April','July','August','March','May','May',
                   'June','July','August','August','September',
                   'November','January','February','July','August','August',
                   'October','December','January','February','August','June',
                   'December','September','October','November','August','August',
                   'January','February']

#standardlize month with english by for loop
for i in range(0,72):
    data_blog['datetime']=data_blog.datetime.str.replace(month_convert[i],month_eng[i])


#check month
month = data_blog['datetime'].str.split(',').str[1]
month.unique()


#parse date to datetime format  
from dateutil.parser import parse
#set function for convert date
def convertdate(s):
    str1 = []
    for i in data_blog['datetime']:
        try:
            ele = parse(i)
        except:
            ele = 'nan'
        str1.append(ele)
    return str1

#set list date_time
data_time = convertdate(data_blog['date'])

#set datetime variable
data_blog['datetime'] = data_time

#remove observations don't have publish date 
data_blog=data_blog.dropna()


#extract weekday from date
data_blog['weekday']=pd.to_datetime(data_blog['datetime']).dt.dayofweek
days = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
data_blog['weekday']=data_blog['weekday'].apply(lambda x: days[x])


#extract month from date
data_blog['month']=pd.to_datetime(data_blog['datetime']).dt.month
months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
          7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
data_blog['month']=data_blog['month'].apply(lambda x: months[x])

#extract year from date
data_blog['year']=pd.to_datetime(data_blog['datetime']).dt.year


#STEP 1.4 REMOVE URLLINK (THIS WILL BE SLOW)
from urllib.parse import urlparse
#set function to remove urllink
def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

#remove url link
data_blog['post'] = [' '.join(y for y in x.split() if not is_url(y)) for x in data_blog['post']]


#back up original post
data_blog['post_original'] = data_blog['post']

 

#STEP 1.5 CLEANSING BLOG CONTENT
#decontraction
import re
def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase
data_blog['post'] = data_blog['post'].apply(decontracted)

#replace dot by space
data_blog['post']=data_blog['post'].str.replace('.',' ')


#remove puntuation, number, and stopword
from nltk.corpus import stopwords
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

#set function to remove 
def clean_text(text):
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace symbols which are in REPLACE_BY_SPACE_RE by space
    text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE  
    #text = text.replace('x', '')
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove stopwors from text
    return text

#apply function to remove puntuation, number, and stopword
data_blog['post'] = data_blog['post'].apply(clean_text)
data_blog['post'] = data_blog['post'].str.replace('\d+', '')


#remove meaningless word
word_remove = [' ive ',' im ',' didnt ',' dont ']
for i in word_remove:
    data_blog['post']=data_blog['post'].str.replace(i,' ')


#count number of word in each post
count = data_blog['post'].str.split().str.len()

#creat word number variable (number of word in each post after normalizing) 
data_blog['#words'] = count
