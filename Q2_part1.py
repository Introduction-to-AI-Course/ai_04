# -*- coding:utf8 -*-
import jieba
import gensim
import pandas as pd
from gensim import corpora, models, similarities
import jieba
import re
import datetime

def run():
	data=pd.read_excel(r'infile\附件3.xlsx')
	data['内容']=data['留言详情']#+data['留言详情']
	datax=data['内容'].apply(lambda x:re.sub('x',' ',x))

	jieba.load_userdict(r'data\newdic1.txt')
	data['内容']=data['留言主题']#+data['留言详情']
	datax=data['内容'].apply(lambda x:re.sub('x',' ',x))

	jieba.load_userdict('data/newdic1.txt')
	data_cut=datax.apply(lambda x:jieba.lcut(x))
	stopWords = pd.read_csv(r'data/stopword.txt', encoding='GB18030', sep='hahah')
	stopWords = ['≮', '≯', '≠','≮', ' ', '会', '月', '日', '–', '！', '，', '。', '\u3000', '，', '\xa0', '\t', '\n'] + list(stopWords.iloc[:, 0])
	data_after_stop = data_cut.apply(lambda x: [i for i in x if i not in stopWords])
	data['新内容']=data_after_stop
	data['编号']=0
	for i in range(1,len(data)+1):
		data['编号'][i-1]=i;


	#相似度分类

	for i in range(1,len(data)+1):
		for j in range(i+1,len(data)+1):
			if data['编号'][j-1]==j:
				texts=[data['新内容'][i-1],['想要']]
				# 建立词典
				dictionary = corpora.Dictionary(texts)
				num_features = len(dictionary.token2id)
				# 基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
				corpus = [dictionary.doc2bow(text) for text in texts]
				# 关键词转换为稀疏向量
				kw_vector = dictionary.doc2bow(data['新内容'][j-1])
				# 4、创建【TF-IDF模型】，传入【语料库】来训练
				tfidf = models.TfidfModel(corpus)
				# 5、用训练好的【TF-IDF模型】处理【被检索文本】和【搜索词】
				tf_texts = tfidf[corpus]
				tf_kw = tfidf[kw_vector]
				sparse_matrix = similarities.SparseMatrixSimilarity(tf_texts, num_features)
				similar = sparse_matrix[tf_kw]
				#print(similar[0])
				if similar[0]>0.60:
					data['编号'][j-1]=data['编号'][i-1]
			else:
				continue

	#newdata=data['新内容'].groupby([data['编号']])
	newdata=data.groupby('编号')

	data=data.sort_values('编号')
	data['留言时间']=pd.to_datetime(data['留言时间'])

	sumarray=[]
	timearray=[]
	sum=0
	flag=data['编号'][0]
	maxtime=data['留言时间'][0].to_pydatetime()
	mintime=data['留言时间'][0].to_pydatetime()
	#前n-1行
	for index,row in data.iterrows():
		if row['编号']==flag:
			sum=sum+1
			if (row['留言时间'].to_pydatetime())>=maxtime:
				maxtime=row['留言时间'].to_pydatetime()
			else:
				mintime=row['留言时间'].to_pydatetime()
		else:
			sumarray.append(sum)
			sum=1
			timearray.append((maxtime-mintime).days)
			maxtime=row['留言时间'].to_pydatetime()
			mintime=row['留言时间'].to_pydatetime()
		flag=row['编号']
	#第n行
	sumarray.append(sum)
	timearray.append((maxtime-mintime).days)

	decidearray=[]
	sign=0
	for x in sumarray:
		for y in range(x):
			if timearray[sign]!=0:
				decidearray.append(x / timearray[sign])
			else:
				decidearray.append(0)
		sign=sign+1

	data['热点问题评分']=[x for x in decidearray]
	data=data[~data['热点问题评分'].isin([0])]
	data=data.sort_values(by=['热点问题评分','留言编号'],ascending=[False,True])

	number=0
	idarray=[]
	test=decidearray[0]

	df=pd.DataFrame(columns=['留言编号', '留言用户', '留言主题', '留言时间', '留言详情', '点赞数', '反对数', '热点问题评分'])
	for index,row in data.iterrows():
		if row['热点问题评分']!=test:
			number=number+1
		test=row['热点问题评分']
		if number>5:
			break
		else:
			idarray.append(number)
		df.loc[index]=[row['留言编号'],row['留言用户'],row['留言主题'],row['留言时间'],row['留言详情'],row['点赞数'],row['反对数'],row['热点问题评分']]
	df.insert(0,'问题ID',[x for x in idarray])
	dv=df
	dv.to_excel('outfile/热点问题留言明细表含热度指数.xlsx',index=False)
	del df['热点问题评分']
	df.to_excel('outfile/热点问题留言明细表.xlsx',index=False)

