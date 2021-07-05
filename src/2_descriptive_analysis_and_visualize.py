### STEP 2: DESCRIPTIVE STATISTIC #################
#import library for plotting
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#### STEP 2.1: ANALYZING BLOGGER INFORMATION ##########

# HISTOGRAM OF BLOGGERS AGE
#compute mean, std, mode
mean = blogger_data['age'].mean()
std = blogger_data['age'].std()
mode = blogger_data['age'].mode()

#plotting histogram
plt.hist(blogger_data['age'], bins=np.arange(14, 50, 1))
plt.ylabel('frequency')
plt.xlabel('age')
plt.title("mean = %.2f, std = %.2f, mode=%.2f" % (mean, std, mode),\
          fontsize=10)
plt.show()




#BAR CHART FOR NUMBER OF BLOGGERS BY GENDER AND ASTROLOGY
#create data for blooger number by astrology and gender
df = blogger_data[['astrology','gender']]
df=pd.DataFrame(df.value_counts())
df.reset_index(inplace=True)
df=df.rename(columns={0: "#blogger"})
df=df.pivot(index='astrology',columns = 'gender', values = '#blogger')

#plotting bar chart
ax=df.plot.bar()
ax.legend(bbox_to_anchor=(1.0, 1.0))
ax.set_ylabel('number of blogeers')
plt.show()



#HEATMAP FOR NUMBER OF BLOOGERS BY GENDER AND INDUSTRY
#create data for blooger number by industry and gender
df = blogger_data[['industry','gender']]
df=pd.DataFrame(df.value_counts())
df.reset_index(inplace=True)
df=df.rename(columns={0: "#blogger"})
df=df.pivot(index='industry',columns = 'gender', values = '#blogger')

#filter for major industry
df=df.loc[(df['female']+df['male'])>200]

#plotting heatmap
sns.heatmap(df,annot = True, fmt="d",cmap="YlGnBu")
plt.show()






##### STEP2.2 ANALYZING BLOG CONTENT ########

#HISTOGRAM OF WORD NUMBER IN BLOGS
#compute mean, std, mode
mean = data_blog['#words'].mean()
std = data_blog['#words'].std()
mode = data_blog['#words'].mode()


#plotting histogram of word number
plt.hist(data_blog['#words'],bins=np.arange(0,400,1))
plt.ylabel('frequency')
plt.xlabel('#words')
plt.title("mean = %.2f, std = %.2f, mode=%.2f" % (mean, std, mode),\
          fontsize=10)
plt.show()


#LINE CHART FOR TOTAL NUMBERS OF POST IN EACCH MONTH 
#create time data
time_data = data_blog[['datetime','#words']].copy()
time_data=time_data.loc[time_data['datetime']<='2004-08-31']
time_data['month_year'] = time_data['datetime'].dt.strftime('%Y-%m')
del time_data['datetime']

#count number of post in each month
time_data_post=time_data.groupby(['month_year']).count()
time_data_post = time_data_post.div(1e3,fill_value=None)
time_data_post=time_data_post.rename(columns={'#words':'total number of post'})

#plotting line chart for number of post
ax=time_data_post.plot(rot=90,legend=None)
ax.set_xlabel('date')
ax.set_ylabel('number of post (thousand)')
plt.show()


#LINE CHART FOR TOTAL NUMBERS OF WORDS IN EACCH MONTH
#sum number of word of posts in each month
time_data_word=time_data.groupby(['month_year']).sum()
time_data_word = time_data_word.div(1e6,fill_value=None)
time_data_word=time_data_word.rename(columns={'#words':'total number of words (million)'})

#plotting line chart for numbers of word
ax=time_data_word.plot(rot=90,color='green',legend=None)
ax.set_xlabel('date')
ax.set_ylabel('number of posted word (million)')
plt.show()


#BUBBLE CHARTS FOR AVERAGE WORD PER POST BY WEEKDAY AND MONTH
#create orders for charts
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul','Aug','Sep','Oct','Nov','Dec']
day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

#create two way table for total number word by weekday and month
wordmd = pd.pivot_table(data_blog,values='#words', index='month',
                    columns='weekday', aggfunc=np.sum)
wordmd = wordmd.reindex(month_order, axis=0)
wordmd = wordmd.reindex(day_order, axis=1)


#count number of post by weekday and month
post_num=data_blog.loc[:, ['datetime','month','weekday']]
post_num = pd.crosstab(index=post_num['month'],columns=post_num['weekday'])
post_num = post_num.reindex(month_order, axis=0)
post_num = post_num.reindex(day_order, axis=1)


#compute average word per post
word_per_post = wordmd.div(post_num,fill_value=None)

#transform to dataframe for ploting
avg_word_post=word_per_post.melt()
avg_word_post=word_per_post.reset_index().melt(id_vars=['month']).\
    set_index(['weekday', 'month'])
avg_word_post.reset_index(inplace=True)
avg_word_post=avg_word_post.rename(columns={'value':'avg_word'})
#remove missing value
avg_word_post['avg_word']=avg_word_post['avg_word'].fillna(0)


#plotting
#set color
cmap = sns.cubehelix_palette(start=2.8,rot=-.1,gamma=0.5, as_cmap=True)

#set bubble size
minsize = min(avg_word_post['avg_word'])
maxsize = max(avg_word_post['avg_word'])

#plotting bubble chart for average word per post
ax = sns.scatterplot(x='weekday', y='month', 
                     hue='avg_word', size='avg_word', sizes=(minsize*3, maxsize*3),
                    palette=cmap,
                    data=avg_word_post,label='avg #words')
ax.legend(loc='right', bbox_to_anchor=(1.25, 0.5), ncol=1,fontsize=8)
ax.invert_yaxis()
plt.show()




#WORD CLOUD, THIS WILL BE SLOW
from wordcloud import WordCloud
#set data for word cloud
sentences = data_blog['post'].tolist()
sentences_as_one_string = " ".join(sentences) #convert to string

#plotting
plt.figure(figsize = (20,20))
plt.imshow(WordCloud().generate(sentences_as_one_string))

#delete data after plotting to save memory
del sentences 
del sentences_as_one_string

