# 意义：
主要研究多层次多尺度的网络态势可视化方法，实现态势的整体展示和分析；针对态势估计算法中的不确定性，研究可视交互方法，实现人在回路，提高算法的准确率和适用性。


# 研究内容
## 目标节点、链路、通联等变化行为的分析
大规模动态网络可视化技术研究。
## 网络重点节点分析筛选
多层次数据整体态势可视分析技术、多维对比可视分析技术。
## 与态势感知算法结合的可视化分析
基于数据融合的安全态势可视分析技术。

# 系统
## 系统主界面
![](https://ws1.sinaimg.cn/large/86d5b437gy1g4lrt0ga3zj21dg0mtaqj.jpg)
## 大规模动态网络可视化技术研究——多种布局方式
![](https://ws1.sinaimg.cn/large/86d5b437gy1g4lrvdtgfvj218x0lcay6.jpg)
## 大规模动态网络可视化技术研究——大规模网络布局
10000个节点的网络，低配置5秒内绘制完成：将布局和渲染分离，提高绘制效率。这里采用了GPU加速。
![](https://ws1.sinaimg.cn/large/86d5b437gy1g4lrwnab6ej20ym0gv7wh.jpg)
## 大规模动态网络可视化技术研究——时变网络
可以通过框选全局时段时间轴来选中全局中的某段时间，然后再通过框选选中时段时间轴来对数据的时间粒度进一步细分，最终将处理好的数据以选中的布局算法可视化出来。——有一部分网络数据是有时间属性的，例如通话记录。针对这种动态的网络，我们采用了时间轴交互，来动态的可视化这些数据。
![](https://ws1.sinaimg.cn/large/86d5b437gy1g4lrxc87sej20y807m40t.jpg)
## 网络重点节点分析筛选
![](https://ws1.sinaimg.cn/large/86d5b437gy1g4lrxi8sdtj21dg0mttpt.jpg)
![](https://ws1.sinaimg.cn/large/86d5b437gy1g4lry3y2jcj217n0k67gv.jpg)
## 与态势感知算法结合的可视化分析——网络通联分析
选中单个节点时，以树状结构显示网络联通情况。根节点为选中的节点，叶子节点为选中节点在当前图中的邻居节点。为了进一步展示通联情况的变化，加入时间属性的展示，在每个叶子节点右侧用线段代表其在全局时间范围的每分钟是否出现。鼠标悬浮会显示具体时间段。点击通联、链路视图中的节点，可以将其加入/移除分析节点列表。该功能目的在于进一步探索感兴趣节点。

![](https://ws1.sinaimg.cn/large/86d5b437gy1g4ls0r7lb2j21840fmang.jpg)
## 与态势感知算法结合的可视化分析——链路变化与节点属性变化分析

提供两种类型的属性变化分析来支持交互的态势感知。一是显示所有选中节点的网络拓扑属性随时间的变化，统计的节点属性包括：度中心性（degree centrality）、特征向量中心性（eigenvector centrality）、核心度（k core）、聚类系数和可达节点比例。鼠标悬浮显示折线代表的属性。用黄色框表示当前选中时间段。点击上方节点标签切换当前要显示的节点。二是用堆叠直方图显示选中节点每分钟的进出流量/各协议的分布。可以通过上方单选框进行切换。鼠标悬浮显示具体数据。

![](https://ws1.sinaimg.cn/large/86d5b437gy1g4ls1fswuej20i90aegml.jpg)
节点链路变化分析
![](https://ws1.sinaimg.cn/large/86d5b437gy1g4ls1mkc86j20i707eabe.jpg)
节点属性变化分析
 
## 与态势感知算法结合的可视化分析——多层网络
![](https://ws1.sinaimg.cn/large/86d5b437gy1g4ls3du97mj20r60l1jvh.jpg)

3个层次的网络之间的关联关系，跨层次的交互分析

![](https://ws1.sinaimg.cn/large/86d5b437gy1g4ls4f9v3yj20q40crgoe.jpg)


## 与态势感知算法结合的可视化分析——伴随关系分析
![](https://ws1.sinaimg.cn/large/86d5b437gy1g4ls5etxqxj21dg0mt10n.jpg)


# 使用
## 前端
### npm install 
### 启动
#### npm run dev，开发模式
#### npm run build，编译，编译后dist文件下，包含一个index.html文件，和static文件夹，上传的服务器即可访问

## 后端 基于python3
### 启动 python server.py （连接数据库，处理数据）

运行sh rsynch.sh 项目目录到vis.pku.edu.cn/networksecurity







