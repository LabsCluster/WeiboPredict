# 新浪微博预测大赛仓库
比赛相关内容请见：http://tianchi.aliyun.com/competition/information.htm?spm=0.0.0.0.Uon8Tx&amp;raceId=5

更多内容请见Wiki:https://github.com/DGideas/WeiboPredict/wiki

##致谢

感谢 @lightslife 提供R语言的实现

#赛题数据备忘
* 训练数据由<code>\t</code>依次分隔为：用户id, 微博id, 时间, 转发数, 评论数, 赞数, 内容
* 预测数据由<code>\t</code>依次分隔为：用户id, 微博id, 时间, 内容

#关于赛题的数据
* 训练数据共有<code>45671</code>不同的用户发布的<code>1626750</code>条微博
* 预测数据共有<code>24818</code>不同的用户发布的<code>275331</code>条微博
* 两文件用户有<code>23603</code>交集，根据作差计算得出，预测数据有<code>1215</code>个从未出现过的新用户
* 额外地，共同存在的用户在训练数据共发布了<code>1335158</code>条微博
* 共同存在的用户在预测数据共发布了<code>265042</code>条微博
* 我们将基本没人点赞的用户定义为垃圾用户(无歧视)，则有<code>21035</code>个垃圾用户

#文件说明
* <code>utrain.txt</code>训练用户列表(<code>45671</code>个)
* <code>upredict.txt</code>预测用户列表(<code>24818</code>个)
* 特别地，因为文件过大，并没有将官方提供的原始训练和预测文件同步到git上

#关于作答
* 如果提交结果均为<code>0,0,0</code>, 相关的准确率是<code>33.815878%</code>

#33.815878%
