from numpy.lib.function_base import append
import pandas as pd 
import matplotlib.pyplot as plt
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
