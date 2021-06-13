import os,sys,ctypes
import datetime
import platform
import get_ip_utils

hostLocation = ''
addr2ip = {}
sites = []

def loadSites():
    with open('sites.txt','r',encoding='UTF-8') as sitefile:
        line = sitefile.readline()
        while line:
            if not line.startswith('#'):
                sites.append(line.strip('\n'))
            line = sitefile.readline()

def checkPlatform():
    global hostLocation
    if platform.system() == 'Windows':
        hostLocation = hostLocation + r'C:\Windows\System32\drivers\etc\hosts'
    elif platform.system() == 'Linux':
        hostLocation = hostLocation + r"/etc/hosts"
    else:
        print('\nOnly Work For Windows/Linux\n')
        raise

def dropDuplication(line):
    if ('#managed by autogithubhosts' in line) or ('#github.com start' in line) or ('#github.com end' in line):
        return True
    return False

def getIp():
    global sites
    for site in sites:
        trueip=get_ip_utils.getIpFromipapi(site)
        if trueip != None:
            addr2ip[site] = trueip

def updateHost():
    global addr2ip
    today = datetime.date.today()
    with open(hostLocation, "r") as f1:
        f1_lines = f1.readlines()
        with open("temphost", "w") as f2:
            for line in f1_lines:
                if dropDuplication(line) == False:
                    f2.write(line)
            f2.write('\n#github.com start' +
                     ' **** ' + str(today) +' update ****\n')
            for key in addr2ip:
                f2.write(addr2ip[key] + "\t" + key + "\t# managed by autogithubhosts\n")
    os.remove(hostLocation)
    os.rename("temphost",hostLocation)

if __name__ == '__main__':
    print('载入列表...')
    loadSites()
    print('检测平台类型...')
    checkPlatform()
    print('获取ip...')
    getIp()
    print('写入文件...')
    updateHost()
    print('操作完成')