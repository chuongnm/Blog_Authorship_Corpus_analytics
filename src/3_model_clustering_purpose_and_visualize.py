#### STEP 3 MODEL FOR CLUSTERING PURPOSE  #########

#remove extremly long post
model_purpose = data_blog[(data_blog['#words'] > 0) & (data_blog['#words'] <= 300)] 


from sklearn.feature_extraction.text import TfidfVectorizer
#vectorize and embbed text data by Tfidf
tfidf_vect = TfidfVectorizer(max_df=0.8, min_df=2, stop_words='english')#modify size of vocab:max_features=2000
doc_term_matrix = tfidf_vect.fit_transform(model_purpose['post'].values.astype('U'))

#use NMF to factorize to optional number of purpose
from sklearn.decomposition import NMF
nmf = NMF(n_components=3) #set number component 
nmf.fit(doc_term_matrix)

#print top 10 word in each three purprose
for i,topic in enumerate(nmf.components_):
    print(f'Top 10 words for purpose #{i}:')
    print([tfidf_vect.get_feature_names()[i] for i in topic.argsort()[-10:]])
    print('\n')

#label the topic_values for each post
topic_values = nmf.transform(doc_term_matrix)
model_purpose['purpose'] = topic_values.argmax(axis=1)


#set detail purpose for each post base on topic_values and meaning of top 10 words with highest probabilities 
conditions = [(model_purpose['purpose']==0),(model_purpose['purpose']==1),(model_purpose['purpose']==2)]
values = ['sharing_information','sharing_diary','sharing_emotion']
model_purpose['purpose_detail'] = np.select(conditions, values)


#BAR CHART FOR NUMBER OF POST BY GENDER AND PURPOSE
#create data for plotting
purpose_data = pd.pivot_table(model_purpose,values='#words', index='purpose_detail',
                    columns='gender', aggfunc=np.count_nonzero)

#plotting bar chart
ax=purpose_data.plot.bar(rot=0)
ax.set_ylabel('number of post')
plt.show()

#AREA CHART FOR TOTAL NUMBER OF WORD IN POST BY PURPOSE IN 2004
#create data for the total number of word
topic_data_avgword = model_purpose[['purpose_detail','datetime','#words']].copy()
topic_data_avgword=topic_data_avgword.loc[topic_data_avgword['datetime']<='2004-08-31']
topic_data_avgword=topic_data_avgword.loc[topic_data_avgword['datetime']>='2004-01-01']
topic_data_avgword['month_year'] = topic_data_avgword['datetime'].dt.strftime('%Y-%m')
del topic_data_avgword['datetime']
topic_data_avgword = pd.pivot_table(topic_data_avgword,values='#words', index='month_year',
                    columns='purpose_detail', aggfunc=np.sum)

#set unit: million words
topic_data_avgword = topic_data_avgword.div(1e6,fill_value=None)


#plotting area chart
ax=topic_data_avgword.plot.area(rot=90)
ax.set_ylabel('total number of posted word (million)')
plt.show()

