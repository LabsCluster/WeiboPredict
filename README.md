# 新浪微博预测大赛DGideas开源仓库
比赛相关内容请见：http://tianchi.aliyun.com/competition/information.htm?spm=0.0.0.0.Uon8Tx&amp;raceId=5

#赛题数据备忘
* 训练数据由\t依次分隔为：用户id, 微博id, 时间, 转发数, 评论数, 赞数, 内容
* 预测数据由\t依次分隔为：用户id, 微博id, 时间, 内容

#关于赛题的数据
* 训练数据共有<code>45671</code>不同的用户发布的<code>1626750</code>条微博
* 预测数据共有<code>24818</code>不同的用户发布的<code>275331</code>条微博
* 两文件用户有<code>23603</code>交集，根据作差计算得出，预测数据有<code>1215</code>个从未出现过的新用户。
* 我们将大规模群发的用户定义为垃圾用户，则有<code>未计算</code>个垃圾用户

#文件说明
* <code>utrain.txt</code>训练用户列表(<code>45671</code>个)
* <code>upredict.txt</code>预测用户列表(<code>24818</code>个)
* 特别地，因为文件过大，并没有将官方提供的原始训练和预测文件同步到git上
