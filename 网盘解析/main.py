from 蓝奏云解析.main import LanzouJiexi


class Jiexi:
    def __init__(self):
        self.jiexiList = [['蓝奏云解析', 'lanzouJiexi']]
        for i in range(len(self.jiexiList)):
            print('[' + str(i) + ']', self.jiexiList[i][0])
        self.selectType()

    def selectType(self):
        try:
            jiexiTypeIndex: int = int(input('请输入序号: '))
            self.jiexiType: str = self.jiexiList[jiexiTypeIndex][1]
        except:
            print('输入有误')
            print('-' * 20)
            self.selectType()
            return
        self.start()

    def start(self):
        try:
            self.__getattribute__(self.jiexiType)()
            input('解析完成, 回车继续')
            print('-' * 20)
            self.__init__()
        except:
            print('解析失败')
            self.start()

    def lanzouJiexi(self):
        lanzou = LanzouJiexi(input('请输入文件分享链接: '))
        downUrl: str = lanzou.getDownloadUrl()
        print('下载链接: ' + downUrl)


if __name__ == '__main__':
    Jiexi()
