# 蓝奏云解析下载程序

## 项目介绍

- 开发时间：2022年11月2日
- 作者：欧阳鹏

## 适用场景

- 带密码
- 不带密码
- 会员
- 非会员

## 程序分析

- 测试用例

  - 会员：https://www.lanzouw.com/iDTGl0btyk0f
  - 非会员：https://oyp.lanzoub.com/iqols07398pi

- 第一次解析

  - 无密码非会员
    
    ```html
    <iframe class="ifr2" name="1667366406" src="/fn?UjQGbAhiA2MJblcxVDNQYVM6DzJULVEnUWsGMQdtADcFMlM3XDdQMgRmBmAAYlZxASwGZl9iAnNVO1MyBzVRO1I3BigIaAMgCSpXalRp" frameborder="0" scrolling="no"></iframe>
    ```

  - 无密码会员

    ```html
    <iframe class="n_downlink" name="1667366666" src="/fn?AWcFbwtuVTNSNAZmUTIHNVo2VWVRKFYgBT8GMQVvUWYEM1A0DmUEZlU1BWUCYAYhAy8DO1Y4UXVVJVs4VmhRIwFoBTULOFVqUmEGKVE4B1FaN1UnUX0_c" frameborder="0" scrolling="no"></iframe>
    ```

## 调用示例

```py
url = 'https://www.lanzouw.com/iDTGl0btyk0f'
lan = LanzouJiexi(url)
downUrl = lan.getDownloadUrl()
print('下载地址: ' + downUrl)
```