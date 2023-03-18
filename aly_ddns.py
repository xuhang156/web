from aliyunsdkcore.client import AcsClient
import urllib
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
import os
import json

ip_file_path = "D:/ip"
client = AcsClient('LTAI5tF1vwn9CY94D1JSXUzQ', 'B1Id7GwpsCihiVBMUpcHNmC6LAsyEU') 

def write_ip_to_file(ip):
    with open(ip_file_path, 'w') as f:
        f.write(ip)

def get_internet_ip():
    with urllib.request.urlopen('http://www.3322.org/dyndns/getip') as response:
        html = response.read()
        ip = str(html, encoding='utf-8').replace("\n", "")
        print('Get id: ',ip)
    return ip

def ip_is_same(ip):
    if not os.path.isfile(ip_file_path):
        return False
    
    with open(ip_file_path, 'r') as f:
        old_ip = f.read()
    if ip == old_ip:
        print("noupdate"+"\nnew_ip:"+ip+"\nold_ip:"+old_ip)
        return True
    return False

def update_record(RecordId, RR, Type, Value):  # 修改域名解析记录
    from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_RecordId(RecordId)
    request.set_RR(RR)
    request.set_Type(Type)
    request.set_Value(Value)
    response = client.do_action_with_exception(request)

def add_record(domain_name, rr, type, ip_value):  # 添加新的域名解析记录
    from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
    request = AddDomainRecordRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain_name)
    request.set_RR(rr)  # https://blog.zeruns.tech
    request.set_Type(type)
    request.set_Value(ip_value)    
    response = client.do_action_with_exception(request)
    return response

def updte_ddns(ip):
    request = DescribeSubDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName("33521.wang")
    request.set_SubDomain("pi" + '.' + "33521.wang")
    request.set_Type("A")
    response = client.do_action_with_exception(request)  # 获取域名解析记录列表
    des_relsult = json.loads(response)  # 将返回的JSON数据转化为Python能识别的
    print(des_relsult)

    #判断子域名解析记录查询结果，TotalCount为1表示存在这个子域名的解析记录，需要更新解析记录，更新记录需要用到RecordId，这个在查询函数中有返回des_relsult["DomainRecords"]["Record"][0]["RecordId"]
    if des_relsult["TotalCount"] == 0:
        add_record("33521.wang","pi", "A", ip)
        print("域名解析新增成功:")
        
    elif des_relsult["TotalCount"] == 1:
            record_id = des_relsult["DomainRecords"]["Record"][0]["RecordId"]
            update_record(record_id,"pi","A",ip)
            print("域名解析更新成功！")
    else:
        record_id = 0
        print("存在两个子域名解析记录值，请核查删除后再操作！")
        path = './RecordId'
    
def run():
    ip = get_internet_ip()
    if ip_is_same(ip):
        return
    updte_ddns(ip)
    write_ip_to_file(ip)

if __name__ == "__main__":
    run()
    print(client)