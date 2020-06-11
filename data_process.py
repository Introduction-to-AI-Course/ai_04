import re
import  jieba
import pandas as pd
def data_process(file='file2.xlsx'):
    data=pd.read_excel(r'infile/附件2.xlsx')
    data['内容']=data['留言主题']+data['留言详情']
    datas=data[['内容','一级标签']]
    theme=['城乡建设','环境保护','交通运输','教育文体','劳动和社会保障','商贸旅游','卫生计生']
    n=613
    a=datas[datas['一级标签']==theme[0]].sample(n)
    for i in theme[1:]:
        b=datas[datas['一级标签']==i].sample(n)
        a=pd.concat([a,b],axis=0)
    data_new=a

    data_dup=data_new['内容'].drop_duplicates()
    data_qmin=data_dup.apply(lambda x:re.sub('x',' ',x))

    jieba.load_userdict('data/newdic1.txt')
    data_cut=data_qmin.apply(lambda x:jieba.lcut(x))

    stopWords=pd.read_csv(r'data/stopword.txt',encoding='GB18030',sep='hahah')
    stopWords= ['≮', '≯', '≠', '≮', ' ', '会', '月', '日', '–','！','，','。','\u3000','，','\xa0','\t','\n']+list(stopWords.iloc[:,0])
    data_after_stop=data_cut.apply(lambda x:[i for i in x if i not in stopWords])
    labels=data_new.loc[data_after_stop.index,'一级标签']
    adata=data_cut.apply(lambda x:' '.join(x))
    return adata,data_after_stop,labels

