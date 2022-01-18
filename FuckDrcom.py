'''
Author: MonChen
Date: 2021-01-10 13:23:43
LastEditTime: 2021-10-17 18:39:54
'''
import os
import urllib.request
import urllib.parse
import sys, time, subprocess, platform
import argparse

def parse_fuckdrcom_args():
    parser = argparse.ArgumentParser(description="Fuck Dr.com in SZU.")

    parser.add_argument('--account', type=str, default='sumsch',
                        help='Login account.')
    parser.add_argument('--passwd', type=str, default='sumsch',
                        help='Login password.')
    parser.add_argument('--verbose', action='store_true',
                        help='Print ping log.')
    parser.add_argument('--monitor', action='store_true',
                        help='Monitoring network state and auto login.')
    parser.add_argument('--logout', action='store_true',
                        help='Logout.')
    
    args = parser.parse_args()

    return args

class FuckDrom():
    def __init__(self, args):
        self.account = args.account
        self.passwd = args.passwd
        self.isVerbose = args.verbose
        self.isMonitor = args.monitor
        self.isLogout = args.logout

        self.pingUrl = "www.baidu.com"

    def fuckIt(self):
        if self.isLogout == True:
            response = self.logout()
            if response == True:
                print("Logout success!")
            else:
                print("Logout Fail!")
            return
        
        if self.isMonitor == True:
            while True:
                response = self.ping()
                print("Ping result: ",response)
                if response == False:
                    response = self.login()
                    if response == True:
                        print("Login success!")
                    else:
                        print("Login Fail!")
                time.sleep(10)
            return

        response = self.login()
        if response == True:
            print("Login success!")
        else:
            print("Login Fail!")
    

    def ping(self):
        url = self.pingUrl
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """
        # Option 
        param = ['','']
        param[0] = '-n' if platform.system().lower()=='windows' else '-c'
        param[1] = '-w'
        # Building the command. Ex: "ping -c 1 -w 1000 www.baidu.com"
        command = ['ping', param[0], '1', param[1], '5000', url]
        devNull = open(os.devnull,'w')
        res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # print("res.returncode:",res.returncode)
        return res.returncode == 0

    def login(self):
        data = {
            'DDDDD': self.account,  
            'upass': self.passwd,  
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
        # print("Login: Lenth of page:",len(page))
        if len(page) == 6379:
            return True
        else:
            return False

    def logout(self):
        url = 'http://192.168.254.220/F.htm'
        request = urllib.request.Request(url)
        page = urllib.request.urlopen(request).read()
        page = page.decode('gb2312')
        # print("Lenth of page:",len(page))
        if len(page) == 9870:
            return True
        else:
            return False



if __name__ == "__main__":
    args = parse_fuckdrcom_args()
    fuckDrcom = FuckDrom(args)
    fuckDrcom.fuckIt()

    

