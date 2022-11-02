import requests
import re
import json


class LanzouJiexi:
    '''
    蓝奏云解析
    '''

    def __init__(self, url: str):
        self.url = url
        self.headers = {'user-agent': 'apee'}

    def getFrameUrl(self) -> str:
        '''
        获取 iframe 的地址
        '''
        r = requests.get(self.url, headers=self.headers)
        r.encoding = 'utf-8'
        yuanma = r.text
        if '<div class="top">' in yuanma:
            pattern = r'<iframe class="ifr2" name="\d{5,}" src="(.*?)"'
        else:
            pattern = r'<iframe class="n_downlink".*?src="(.*?)"'
        url = re.search(pattern, yuanma).group(1)
        return 'https://www.lanzouw.com' + url

    def getPostParam(self, url: str) -> dict:
        '''
        获取 POST 请求参数
        url: iframe URL
        '''
        r = requests.get(url, headers=self.headers)
        r.encoding = 'utf-8'
        yuanma = r.text
        postParam = {'action': 'downprocess', 'websign': '', 'ves': 1}
        postParam['signs'] = re.search(
            r'var ajaxdata = \'(.*?)\'', yuanma).group(1)
        postParam['sign'] = re.search(
            r'var msigns = \'(.*?)\'', yuanma).group(1)
        postParam['websignkey'] = re.search(
            r'var cwebsignkeyc = \'(.*?)\'', yuanma).group(1)
        return postParam

    def getDownloadUrl(self) -> str:
        '''
        获取下载链接
        '''
        frameUrl = self.getFrameUrl()
        postParam = self.getPostParam(frameUrl)
        url = 'https://www.lanzouw.com/ajaxm.php'
        r = requests.post(url, data=postParam, headers={
            'user-agent': self.headers['user-agent'],
            'referer': 'https://oyp.lanzoub.com'
        })
        r.encoding = 'utf-8'
        dataJson = json.loads(r.text)
        return dataJson['dom'] + '/file/' + dataJson['url']


if __name__ == '__main__':
    url = input('请输入URL: ')
    # url = 'https://oyp.lanzoub.com/iqols07398pi'  # 非会员
    # url = 'https://www.lanzouw.com/iDTGl0btyk0f'  # 会员
    lan = LanzouJiexi(url)
    downUrl = lan.getDownloadUrl()
    print('下载地址: ' + downUrl)
