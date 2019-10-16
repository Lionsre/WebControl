import datetime
import os
import sys

block_dict = {}
hosts_path = r"C:\Windows\System32\drivers\etc\hosts" #Hosts文件路径
blocklist_path = os.path.abspath(sys.argv[0]).replace("WebBlock.py","Block_List.txt")
print(blocklist_path)
with open(blocklist_path,"r",encoding="UTF-8") as blocklist:
    blocklist_lines = blocklist.readlines()
    for blocklist_line in blocklist_lines:
        if len(blocklist_line.split(" ")) == 2:
            block_dict[blocklist_line.split(" ")[1].replace("\n","")] = blocklist_line.split(" ")[0]

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
                for dname, ipaddr in block_dict.items():
                    print("正在写入",ipaddr,dname)
                    f_w.write(ipaddr + " " + dname + "\n")
            elif time_now >= work_pm_start and time_now < work_pm_end: #下午办公时间限制网页打开
                for dname, ipaddr in block_dict.items():
                    print("正在写入", ipaddr, dname)
                    f_w.write(ipaddr + " " + dname + "\n")
            else:pass
        elif r"#_Web_Block_End" in line:
            f_w.write(line)
            web_block_start = False
            continue
        if web_block_start:continue
        f_w.write(line)