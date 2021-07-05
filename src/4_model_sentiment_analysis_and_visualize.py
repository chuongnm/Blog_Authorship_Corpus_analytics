#### STEP 4 SENTIMENT ANALYSIS #########

#remove extremly long post
model_sentiment = data_blog[(data_blog['#words'] > 0) & (data_blog['#words'] <= 300)]

#use Vader to score sentiment
from nltk.sentiment.vader import SentimentIntensityAnalyzer
st=SentimentIntensityAnalyzer()


#get sentiment score, THIS WILL BE SLOW
compound_score=[]
#set function to score sentiment
for i in model_sentiment['post_original']:
    analysis = st.polarity_scores(i)
    compound_score.append(analysis['compound'])

#create new variable for sentiment score
model_sentiment['sentiment_score'] = compound_score



#set sentiment categorization variable base on scale
conditions = [(model_sentiment['sentiment_score']>=0.05),(model_sentiment['sentiment_score']<=-0.05),
              ((model_sentiment['sentiment_score']>-0.05) & (model_sentiment['sentiment_score']<0.05))]
values = ['positive','negative','neutral']
model_sentiment['sentiment'] = np.select(conditions, values)



#BAR CHART FOR NUMBER OF POST BY SENTIMENT AND GENDER
#create data for the number of post
sen_gender_df =  pd.pivot_table(model_sentiment,values='#words', index='sentiment',
                    columns='gender', aggfunc=np.count_nonzero)

sen_gender_df = sen_gender_df.div(1e3,fill_value=None)

#plotting bar chart
ax = sen_gender_df.plot.bar(rot=0)
ax.set_ylabel('number of post (thousand)')
plt.show()


#HEATMAP FOR AVG SENTIMENT SCORE BY ASTROLOGY AND GENDER
#create data for sentiment score
nscore_gender_astrology =  pd.pivot_table(model_sentiment ,values='sentiment_score', index='astrology',
                                          columns='gender', aggfunc=np.average)
#plotting heatmap
sns.heatmap(nscore_gender_astrology,annot = True,cmap='RdYlGn')
plt.show()


#BUBBLE CHART FOR AVG SENTIMENT SCORE BY WEEKDAY AND MONTH 
#create two way table for avg sentiment score by weekday and month
scoremd = pd.pivot_table(model_sentiment,values='sentiment_score', index='month',
                    columns='weekday', aggfunc=np.average)
scoremd = scoremd.reindex(month_order, axis=0)
scoremd = scoremd.reindex(day_order, axis=1)

#transform to dataframe for ploting
avg_score=scoremd.melt()
avg_score=scoremd.reset_index().melt(id_vars=['month']).\
    set_index(['weekday', 'month'])
avg_score.reset_index(inplace=True)
avg_score=avg_score.rename(columns={'value':'avg_score'})
#remove missing value
avg_score['avg_score']=avg_score['avg_score'].fillna(0)

#plotting
#set color
cmap = sns.cubehelix_palette(start=2.2,rot=-.2,gamma=0.6, as_cmap=True)

#set bubble size
minsize = min(avg_score['avg_score'])
maxsize = max(avg_score['avg_score'])

#plotting bubble chart for avg sentiment score
ax = sns.scatterplot(x='weekday', y='month', 
                     hue='avg_score', size='avg_score', sizes=(minsize*900, maxsize*900),
                    palette=cmap,
                    data=avg_score,label='avg sen score')
ax.legend(loc='right', bbox_to_anchor=(1.25, 0.5), ncol=1,fontsize=8)
ax.invert_yaxis()
plt.show()

