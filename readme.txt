aliyun-python-sdk-alidns
aliyun-python-sdk-domain
aliyun-python-sdk-core-v3


# 开启一分钟启动
* * * * * python3 /xxx/xxx.py

# 开启crotab日志（ubuntu可能没有开启）

1. sudo vim /etc/rsyslog.d/50-default.conf
2. 将cron.*前面的#去掉
3. 重启日志服务：sudo service rsyslog restart
4. 等一会日志就会在：/var/log 下

