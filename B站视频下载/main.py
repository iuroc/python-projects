import requests
import re
import json
import os
import time
import sys
from tqdm import tqdm

os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(
    os.path.dirname(sys.argv[0]), 'cacert.pem'
)


class BilibiliDownload:
    '''
    哔哩哔哩视频下载工具, 仅供学习交流使用
    作者: 欧阳鹏
    开发时间: 2022.11.27
    官方网站: https://apee.top
    '''

    quality: dict = {
        16: '360P 流畅',
        32: '480P 清晰',
        64: '720P 高清',
        80: '1080P 高清',
        112: '1080P 高码率',
    }  # 视频分辨率对应信息

    def __init__(self):
        os.system('cls')
        print('\033[1;30m哔哩哔哩视频下载工具, 仅供学习交流使用\n\033[0m')
        self.init_dir('download')
        self.video_url = input('\033[1;32m请输入B站视频链接: \033[0m')  # B站视频链接
        self.cookie = self.get_cookie()
        if not self.video_url:
            self.__init__()
        self.start_download()

    def get_cookie(self):
        '''
        获取Cookie
        '''
        path = 'cookie.txt'
        if not os.path.exists(path):
            open(path, 'w', encoding='utf-8')
            sessdata = ''
        else:
            sessdata = open(path, 'r').read()
        return sessdata

    def get_video_info(self) -> dict:
        '''获取视频信息'''
        r = requests.get(
            self.video_url,
            headers={'cookie': 'SESSDATA=' + self.cookie},
        )
        r.encoding = 'utf-8'
        play_info_search = re.search(
            r'<script>window.__playinfo__=(.*?)</script>', r.text
        )
        video_info_search = re.search(
            r'<script>window.__INITIAL_STATE__=(.*?);', r.text
        )
        if play_info_search and video_info_search:
            play_info_str = play_info_search.group(1)
            video_info_str = video_info_search.group(1)
            play_info: dict = json.loads(play_info_str)
            video_info: dict = json.loads(video_info_str)['videoData']
            video_info['play_info'] = play_info
            return video_info
        else:
            return {}

    def save_file(self, play_info: dict):
        '''
        保存文件
        play_info: 视频播放信息
        '''
        json.dump(
            play_info,
            open('play_info.json', 'w', encoding='utf-8'),
            ensure_ascii=False,
            indent=4,
        )

    def download_m4s(self, url: str, filename: str):
        '''下载 m4s 视频'''
        r = requests.get(
            url,
            headers={
                'referer': 'https://www.bilibili.com',
                'user-agent': 'apee',
            },
            stream=True,
        )
        r.encoding = 'utf-8'
        total = int(r.headers.get('content-length', 0))
        with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in r.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

    def get_support_format(self, play_info: dict) -> list:
        '''
        获取当前支持的分辨率
        play_info: 视频播放信息
        return: 例如 [[80, '25', 'avc1.640032']]
        '''
        formats = []
        for i in play_info['data']['dash']['video']:
            formats.append([i['id'], i['frameRate'], i['codecs']])
        return formats

    def get_download_info(self, video_info: dict, format_info: list) -> dict:
        '''
        获取下载信息
        video_info: 视频信息
        format_info: 视频格式信息
        '''
        play_info = video_info['play_info']
        for i in play_info['data']['dash']['video']:
            if [i['id'], i['frameRate'], i['codecs']] == format_info:
                return {
                    'video_url': i['baseUrl'],
                    'audio_url': self.get_audio_url(play_info, format_info),
                    'title': video_info['title'],
                }
        return {}

    def get_audio_url(self, play_info: dict, format_info: list) -> str:
        '''
        获取音频 URL
        play_info: 视频播放信息
        format_info: 分辨率信息 例如 [32, '30.303']
        '''
        info = [i for i in play_info['data']['dash']['audio']]
        max_id = max([int(i['id']) for i in info])
        for i in info:
            if str(i['id']) == str(max_id):
                return i['baseUrl']
        return ''

    def start_download(self):
        '''
        开始解析下载
        '''
        os.system('cls')
        print('正在解析...')
        video_info = self.get_video_info()
        play_info = video_info['play_info']
        formats = self.get_support_format(play_info)
        os.system('cls')
        print('\033[1;33m' + video_info['title'] + '\n\033[0m')
        print('┌%s┬%s┬%s┬%s┐' % ('─' * 6, '─' * 12, '─' * 8, '─' * 32))
        print(
            '│%s│%s│%s│%s│'
            % ('序号'.center(4), '清晰度'.center(9), '帧率'.center(6), '编码'.center(30))
        )
        print('├%s┼%s┼%s┼%s┤' % ('─' * 6, '─' * 12, '─' * 8, '─' * 32))
        for i in range(len(formats)):
            print(
                '│%s│%s│%s│%s│'
                % (
                    str(i).center(6),
                    self.quality[formats[i][0]].center(10),
                    formats[i][1].center(8),
                    formats[i][2].center(32),
                )
            )
        print('└%s┴%s┴%s┴%s┘' % ('─' * 6, '─' * 12, '─' * 8, '─' * 32))
        try:
            format_code = int(input('\033[1;32m请选择下载的视频质量(序号): \033[0m'))
        except:
            format_code = 0
        download_info = self.get_download_info(video_info, formats[format_code])
        os.system('cls')
        print('\033[1;34m开始下载视频...\033[0m')
        self.download_m4s(download_info['video_url'], 'video.m4s')
        print('\033[1;34m开始下载音频...\033[0m')
        self.download_m4s(download_info['audio_url'], 'audio.m4s')
        print('\033[1;34m开始合并视频...\033[0m')
        download_path = 'download/' + download_info['title'] + '.mp4'
        os.system('cls')
        os.system(
            'ffmpeg -i "video.m4s" -i "audio.m4s" -vcodec copy -acodec copy "%s" -y'
            % download_path
        )
        os.remove('video.m4s')
        os.remove('audio.m4s')
        os.system('cls')
        print('\033[1;36m下载完成, 文件保存在: \033[0m' + download_path)
        input('回车继续...')
        self.__init__()

    def init_dir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)


BilibiliDownload()
