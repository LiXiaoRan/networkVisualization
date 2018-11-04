# @Author: wakouboy
# @Date:   2018-08-03 15:39:58
# @Last Modified by:   wakouboy
# @Last Modified time: 2018-11-05 00:43:28
rsync -avz --exclude '.git' client/dist/* shuai.chen@192.168.10.9:/var/www/html/networksecurity/
rsync -avz --exclude '.git' server/* shuai.chen@192.168.10.9:/var/www/html/networksecurity/server