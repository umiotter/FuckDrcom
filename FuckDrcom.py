'''
Author: MonChen
Date: 2021-01-10 13:23:43
LastEditTime: 2021-01-14 15:25:52
'''
import urllib.request
import urllib.parse
import sys, time, subprocess, platform

hostname = "www.baidu.com"

manpage = 'FuckDrcom [option]...\n\t--login [IdNumbers] [password]\n\t--autologin [IdNumbers] [password]\n\t--logout'

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Option for the number of packets as a function of
    param = ['','']
    param[0] = '-n' if platform.system().lower()=='windows' else '-c'
    param[1] = '-w'
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param[0], '1', param[1], '1000', host]

    return subprocess.call(command) == 0

def login(idNums='',passwd=''):
    data = {
        'DDDDD': idNums,  
        'upass': passwd,  
        '0MKKey': r'登　录',
        'v6ip': ''
    }

    url = 'https://drcom.szu.edu.cn/a70.htm'
    header = {
        'Host': '192.168.254.220',
        'Connection': 'keep-alive',
        'Content-Length': '53',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://192.168.254.220',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'DNT': '1',
        'Referer': 'http://192.168.254.220/0.htm',
        'Accept-Encoding': 'gzip, deflate'
    }

    data = urllib.parse.urlencode(data).encode('gb2312')
    request = urllib.request.Request(url, headers=header, data=data)
    page = urllib.request.urlopen(request).read()  
    page = page.decode('gb2312')
    if len(page) == 6491:
        print('Success.')
    else:
        print('Fail, IdNums or password incorrect.')

    # 6491 -> ok
    # 5696 -> error

def logout():
    url = 'http://192.168.254.220/F.htm'
    request = urllib.request.Request(url)
    page = urllib.request.urlopen(request).read()
    page = page.decode('gb2312')
    print('Success.')



if __name__ == "__main__":
    if len(sys.argv)>1:
        option = sys.argv[1]
        if option == '--login' and len(sys.argv) == 4:
            idNums = sys.argv[2]
            passwd = sys.argv[3]
            login(idNums,passwd)
        elif option == '--autologin' and len(sys.argv) == 4:
            while True:
                response = ping(hostname)
                if response == True:
                    print('============Alive============')
                else:
                    idNums = sys.argv[2]
                    passwd = sys.argv[3]
                    print('============Connect Failed, Try to reconnect.============')
                    login(idNums,passwd)
                time.sleep(2)
        elif option == '--logout':
            logout()
        else:
            print(manpage)
    else:
        print(manpage)
    

