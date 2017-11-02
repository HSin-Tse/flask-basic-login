# 埋点版本 埋点业务 t1 ctl pg blk bt goto vlu

# 5.9.2
 2.1.5 1.轮播图 click mlive head pager image url productid,pos,pid
## 抓包
ajmd {"ctl":"mlive","pg":"head","blk":"pager","bt":"image","goto":"http://m.ajmide.com/touch /pages/shopping/life/recommend.htm?id=121","t1":"click"}
### 反馈
vlu 遗失

pos 遗失
productid 遗失 (hold)

# 5.9.3
2.1.5 1.轮播图 click mlive head pager image url productid,pos,pid
## 抓包
{"ctl":"mlive","pg":"bar","blk":"block","bt":"recommend","goto":"ept","vlu":{"pos": 0},"t1":"click"}
{"ctl":"mlive","pg":"bar","blk":"block","bt":"recommend","goto":"ept","vlu":{"pos": 1},"t1":"click"}
{"ctl":"mlive","pg":"bar","blk":"block","bt":"recommend","goto":"ept","vlu":{"pos": 2},"t1":"click"}
### 反馈
bt all the same

# 5.9.4
2.1.5 1.推荐 click mlive recommend list infor mliveproduct productid,pos,pid
## 抓包
{"ctl":"mlive","pg":"recommend","blk":"list","bt":"infor","goto":"mliveproduct","vlu":{"productid": 125},"t1":"click"}
### 反馈
pos 遗失

# 5.9.5
2.1.5 1.优品 click mlive great list infor mliveproduct productid,pos,pid
## 抓包
{"ctl":"mlive","pg":"great","blk":"list","bt":"infor","goto":"mliveproduct","vlu":{"productid": 125},"t1":"click"}
### 反馈
pos 遗失

# 5.9.6
## 抓包
{"ctl":"mlive","pg":"bonus","blk":"list","bt":"infor","goto":"topicdetail","vlu":{"bonusid": 12853558},"t1":"click"}
2.1.5 1.福利 click mlive bonus list infor topicdetail pos,pid,bonusid
### 反馈
pos 遗失