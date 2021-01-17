#from numpy.lib.function_base import append
import pandas as pd
from pandas import DataFrame,Series 
import matplotlib.pyplot as plt
import numpy as np
import json
import demjson
import warnings
warnings.filterwarnings('ignore')
#from wordcloud import WordCloud, STOPWORDS

# 可视化
# 定义字体
plt.rcParams["font.sans-serif"] = "Arial Unicode MS"
#导入三个数据表
predict=pd.read_csv(r'C:\tools\python\lxt1\tmdb_1000_predict.csv')
movies=pd.read_csv(r'C:\tools\python\lxt1\tmdb_5000_movies.csv')
credits=pd.read_csv(r'C:\tools\python\lxt1\tmdb_5000_credits.csv')
#打印三个数据表
#print(predict)
#print(movies)
#print(credits)
#df.inf()
predict.info()
movies.info()
credits.info()
#isnull
#print(predict.isnull())
#print(movies.isnull())
#在movies的release_date中查看缺失项
#print(movies['release_date'].isnull())
#print(movies['release_date'])
#查看movies中哪些有缺失值
print(movies[movies.isnull().values==True])

#查看movies表中的release_date在哪行有缺失值
print(movies[movies['release_date'].isnull().values==True])
#将release_date转化为时间类型
movies["release_date"]=pd.to_datetime(movies["release_date"])
print(movies["release_date"])

#为release_date为空值的项补上从网上查询得到的时间‘2014-06-01’
movies["release_date"]=movies["release_date"].fillna("2014-06-01")
"""
print(movies)
#print(movies["title"]=="America Is Still the Place")
row=movies.iloc[3553]
print(row)
row=movies.iloc[3554]
print(row)
row=movies.iloc[3555]
print(row)
row=movies.iloc[4553]
print(row)
"""
#print(movies[movies.isnull().values==True])
#查看movies里面是否还有缺失值
print(movies['runtime'].isnull())
movies.info()

#打印runtime值缺失的行
print(movies[movies["runtime"].isnull().values==True])


row=movies.iloc[2656]
print(row)
row=movies.iloc[4140]
print(row)

#经过上网查询，这两部缺失runtime的电影的runtime分别为94和240分钟，同样用fillna进行填充
movies["runtime"]=movies["runtime"].fillna(94,limit=1)
movies["runtime"]=movies["runtime"].fillna(240,limit=1)
#其实还有一个更精准的进行填充的方法，即使用movies.loc[2656]=movies.loc[2656].fillna('94,limit=1')
row=movies.iloc[2656]
print(row)
row=movies.iloc[4140]
print(row)

#打印movies中的重复值，从打印出的结果中可以看到没有重复值
print(movies[movies.duplicated()==True])

print(len(movies.id.unique()))

len(movies.id.unique())

#数据分析师最喜欢使用的一个语法
print(movies.describe())


#参考一下网上的写法
#df = df[(df.vote_count >= 50) &(df.budget * df.revenue * df.popularity * df.vote_average !=0)].reset_index(drop = 'True')
movies=movies[(movies.vote_count>=50)&(movies.budget*movies.revenue*movies.popularity*movies.vote_average!=0)].reset_index(drop="True")


movies.info()

#使用merge程序将movies和credits这两个表合并成一张表，便于后续的操作
full = pd.merge(movies, credits, left_on='id', right_on='movie_id', how='left')
print(full)
print(full.loc[2960])

#某些列不在本次研究范围，将其删除
full.drop(['homepage','original_title','overview','spoken_languages','status','tagline','movie_id'],axis=1,inplace=True)
json_column = ['genres','keywords','production_companies','production_countries','cast','crew']


#定义一个json类型的列名列表

json_column = ['genres','keywords','production_companies','production_countries','cast','crew']

#将各json列转换为字典列表
"""
for column in json_column:
    full[column]=full[column].map(json.loads)

#函数功能：将字典内的键‘name’对应的值取出，生成用'|'分隔的字符串

print(full[column].loc[2960])
"""
for i in json_column:
    full[i]=full[i].apply(json.loads)
print (full)
# 提取name
# 将字典列表转换为以“，”分割的字符串
def get_name(x):
    return ','.join([i['name'] for i in x])

full['cast']=full['cast'].apply(get_name)
print(full['cast'])

#提取director
def get_director(x):
    for i in x:
        if i['job']=='Director':
            return i['name']

full['crew']=full['crew'].apply(get_director)
print(full['crew'])


for j in json_column[0:4]:
    full[j]=full[j].apply(get_name)
print(full['crew'])


#重命名
rename_dict={'cast':'actor','crew':'director'}
full.rename(columns=rename_dict,inplace=True)
full.info()
print(full.head(5))

#备份原始数据框original_full
org_full=full.copy()
full.reset_index().to_csv("TMDB_5000_Movie_Dataset_Cleaned.csv")
#定义一个集合，获取所有的电影类型
genre=set()
for i in full['genres'].str.split(','): 
    #去掉字符串之间的分隔符，得到单个电影类型
    genre=set().union(i,genre) 
    #集合求并集

print(genre)
#去掉多余的单引号
genre.discard('')
print(genre)

#将genre转变成列表
genre_list=list(genre)

#创建数据框-电影类型

genre_df=pd.DataFrame()

#对电影类型进行one-hot编程
for i in genre_list:
    #如果包含类型i，则编码为1，否则编码为0
    genre_df[i]=full['genres'].str.contains(i).apply(lambda x:1 if x else 0)

#把数据框的索引变为年份
genre_df.index=full['release_date']
print(genre_df.head(5))
full.info()

#计算得到每种类型的电影总数目，并降序排列
grnre_sum=genre_df.sum().sort_values(ascending=False)
#可视化
plt.rcParams['font.sans-serif']=['SimHei']
#用来显示中文
grnre_sum.plot(kind='bar',label='genres',figsize=(12,9))
plt.title('不同类型的电影数量总计',fontsize=20)
plt.xticks(rotation=60)
plt.xlabel('电影类型',fontsize=16)
plt.ylabel('数量',fontsize=16)
plt.grid(False)
plt.savefig("不同电影类型数量-条形图.png",dpi=300)
plt.show()

#电影类型饼图
gen_shares=grnre_sum/grnre_sum.sum()

#设置other类，当电影类型所占比例小于1%时，全部归到other类中
others=0.01
gen_pie=gen_shares[gen_shares>=others]
gen_pie['others']=gen_shares[gen_shares<others].sum()

#设置分裂属性
#所占比例小于或等于2%时，增大每块饼片边缘偏离半径的百分比
explode=(gen_pie<=0.02)/10

#绘制饼图
gen_pie.plot(kind='pie',label='',explode=explode,startangle=0,shadow=False,autopct='%3.1f%%',figsize=(8,8))
plt.title('不同电影类型所占百比分',fontsize=20)
plt.savefig("不同电影类型所占百分比-饼图.png",dpi=300)
plt.show()

#电影类型变化趋势（折线图）
#电影类型随时间变化的趋势
gen_year_sum=genre_df.sort_index(ascending=False).groupby('release_date').sum()
gen_year_sum_sub=gen_year_sum[['Drama','Comedy','Thriller','Action','Adventure','Crime','Romance','Science Fiction']]
gen_year_sum_sub.plot(figsize=(12,9))
plt.legend(gen_year_sum_sub.columns)
plt.xticks(range(1915,2018,10))
plt.xlabel('年份',fontsize=16)
plt.ylabel('数量',fontsize=16)
plt.title('不同电影变化趋势',fontsize=20)

plt.grid(False)
plt.savefig("不同电影类型数量-折线图2.png",dpi=600)
plt.show()