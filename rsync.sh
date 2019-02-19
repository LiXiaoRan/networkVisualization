# @Author: wakouboy
# @Date:   2018-08-03 15:39:58
# @Last Modified by:   wakouboy
# @Last Modified time: 2019-02-19 10:50:30
rsync -avz --exclude '.git' --exclude '.vscode' --exclude 'client' * shuai.chen@192.168.10.9:/var/www/html/networksecurity/
# rsync -avz --exclude '.git' --exclude '.vscode' --exclude 'client' * fanxin@120.78.159.140:/alidata/www/graph/