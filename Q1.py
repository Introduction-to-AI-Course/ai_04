# -*- coding:utf8 -*-
"""
直接运行，可以得到分类准确度，F-Score值，和混淆矩阵热度图
"""
from boto import sns
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sympy.physics.quantum.circuitplot import matplotlib

from data_process import data_process
from  sklearn.model_selection import train_test_split
from  sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import numpy as np
import pandas as pd
from pylab import *
mpl.rcParams['font.sans-serif']=['SimHei']

#模型训练
adata,data_after_stop,labels=data_process()
data_tr,data_te,labels_tr,labels_te=train_test_split(adata,labels,test_size=0.2)

coutVectorizer=CountVectorizer()
data_tr=coutVectorizer.fit_transform(data_tr)
X_tr=TfidfTransformer().fit_transform(data_tr.toarray()).toarray()

data_te=te=CountVectorizer(vocabulary=coutVectorizer.vocabulary_).fit_transform(data_te)
X_te=TfidfTransformer().fit_transform(data_te.toarray()).toarray()
model=MultinomialNB()
#model=GaussianNB()
model.fit(X_tr,labels_tr)
model.score(X_te,labels_te)
print('分类准确度：',sep="")
print(model.score(X_te,labels_te))

###########################################

ypre=model.predict(X_te)
y_pred=list(ypre)
y_true=list(labels_te)
from sklearn.metrics import f1_score, confusion_matrix
print('利用f1_score函数算出来的F-Score：',sep='')
print(f1_score(y_true, y_pred, average='macro'))
#################################################

cm = confusion_matrix(y_true, y_pred,labels=['城乡建设','环境保护','交通运输','教育文体','劳动和社会保障','商贸旅游','卫生计生'])
x_tick=['城乡建设','环境保护','交通运输','教育文体','劳动和社会保障','商贸旅游','卫生计生']
y_tick=['城乡建设','环境保护','交通运输','教育文体','劳动和社会保障','商贸旅游','卫生计生']
# df=pd.DataFrame(columns=['城乡建设','环境保护','交通运输','教育文体','劳动和社会保障','商贸旅游','卫生计生'])
# head=0
# for i in range(len(cm)):
# 	df.loc[head]=cm[head,:]
# 	head=head+1
# df=pd.DataFrame(df,index=x_tick)
# print(df)
#df=pd.DataFrame(cm,index=x_tick,columns=y_tick)

#############画热度图###############################

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# 调用魔法方法 使得每次显示结果时不用调用plt.show()方法
sns.set(style='whitegrid', color_codes=True)

C2= confusion_matrix(y_true, y_pred,labels=['城乡建设','环境保护','交通运输','教育文体','劳动和社会保障','商贸旅游','卫生计生'])
sns.set(font="simhei")#遇到标签需要汉字的可以在绘图前加上这句
sns.heatmap(C2,annot=True,fmt='d', linewidths=.5, cmap='YlGnBu', xticklabels=x_tick, yticklabels=y_tick)
plt.show()

# import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib import cm
# from matplotlib import axes
# def draw_heatmap(data,xlabels,ylabels):
#     cmap = cm.Blues
#     figure=plt.figure(facecolor='w')
#     ax=figure.add_subplot(2,1,1,position=[0.1,0.15,0.8,0.8])
#     ax.set_yticks(range(len(ylabels)))
#     ax.set_yticklabels(ylabels)
#     ax.set_xticks(range(len(xlabels)))
#     ax.set_xticklabels(xlabels)
#     map=ax.imshow(data,interpolation='nearest',cmap=cmap,aspect='auto')
#     cb=plt.colorbar(mappable=map,cax=None,ax=None,shrink=0.5)
#     plt.show()
#
# draw_heatmap(df,x_tick,y_tick)
#






###############画热度图###############################
cm = cm.astype(np.float32)
FP = cm.sum(axis=0) - np.diag(cm)
FN = cm.sum(axis=1) - np.diag(cm)
TP = np.diag(cm)
TN = cm.sum() - (FP + FN + TP)

# Sensitivity, hit rate, recall, or true positive rate
TPR = TP / (TP + FN)
# Specificity or true negative rate
TNR = TN / (TN + FP)
# Precision or positive predictive value
PPV = TP / (TP + FP)
# Negative predictive value
NPV = TN / (TN + FN)
# Fall out or false positive rate
FPR = FP / (FP + TN)
# False negative rate
FNR = FN / (TP + FN)
# False discovery rate
FDR = FP / (TP + FP)

# Overall accuracy
ACC = (TP + TN) / (TP + FP + FN + TN)
ACC_micro = (sum(TP) + sum(TN)) / (sum(TP) + sum(FP) + sum(FN) + sum(TN))
#ACC_macro = np.mean(ACC)  # to get a sense of effectiveness of our method on the small classes we computed this average (macro-average)

F1 = (2 * PPV * TPR) / (PPV + TPR)

F1_macro = np.mean(F1)
print("根据公式定义算出来的F-Score：",sep='')
print(F1_macro)