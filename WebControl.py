import datetime
import os
import re
import sys

block_list = []
loopbackIP= "127.0.0.1"
hosts_path = r"C:\Windows\System32\drivers\etc\hosts" #Hosts文件路径
blocklist_path = "\\".join(os.path.abspath(sys.argv[0]).split("\\")[:-1]) + r"\Block_List.ini" #配置文件路径
print(blocklist_path)

if not os.path.exists(blocklist_path):
    with open(blocklist_path,"w",encoding="UTF-8") as blocklist:
        blocklist_DefaultMsg = "# Format:[Hostname.SLD.TLD], for example:www.example.com"
        blocklist.write(blocklist_DefaultMsg)
        print("未检测到配置文件，正在生成……")
with open(blocklist_path,"r",encoding="UTF-8") as blocklist:
    blocklist_lines = blocklist.readlines()
    for blocklist_line in blocklist_lines:
        blocklist_line = blocklist_line.strip().replace("\n","")
        if not re.match(r"#",blocklist_line) and re.match("^[0-9A-Za-z]+\.[0-9A-Za-z]+\.[0-9A-Za-z]+$",blocklist_line):
            block_list.append(blocklist_line)

work_am_start = datetime.time(9, 0, 0, 0) #上午上班时间
work_am_end = datetime.time(12, 10, 0, 0) #上午下班时间
work_pm_start = datetime.time(14, 0, 0, 0) #下午上班时间
work_pm_end = datetime.time(17, 40, 0, 0) #下午下班时间

with open(hosts_path,"r",encoding="UTF-8") as f:
    lines = f.readlines()
time_now = datetime.datetime.now().time()

with open(hosts_path,"w",encoding="UTF-8") as f_w:
    web_block_start = False
    for line in lines:
        if r"#_Web_Block_Start" in line:
            f_w.write(line)
            web_block_start = True
            if time_now >= work_am_start and time_now < work_am_end: #上午办公时间限制网页打开
                print("检测到上午上班时间，开始添加网站限制规则。")
                for dname in block_list:
                    print("正在写入", dname)
                    f_w.write( loopbackIP + " " + dname + "\n")
                print("规则添加完成！规则总条数为{}。".format(len(block_list).__str__()))
            elif time_now >= work_pm_start and time_now < work_pm_end: #下午办公时间限制网页打开
                print("检测到下午上班时间，开始添加网站限制规则。")
                for dname in block_list:
                    print("正在写入", dname)
                    f_w.write( loopbackIP + " " + dname + "\n")
                print("规则添加完成！规则总条数为{}。".format(len(block_list).__str__()))
            else:print("检测到下班休息时间，清除限制规则。")
        elif r"#_Web_Block_End" in line:
            f_w.write(line)
            web_block_start = False
            continue
        if web_block_start:continue
        f_w.write(line)

os.system(r"ipconfig /flushdns")