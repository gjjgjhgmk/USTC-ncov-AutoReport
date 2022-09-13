# 中国滑稽大学(University of Ridiculous of China)健康打卡平台自动打卡脚本

![Auto-report action](https://github.com/Kobe972/USTC-ncov-AutoReport/workflows/Auto-report%20action/badge.svg?branch=main)
![School](https://img.shields.io/badge/School-URC-blue.svg)
![Language](https://img.shields.io/badge/language-Python3-yellow.svg)
![GitHub stars](https://img.shields.io/github/stars/Kobe972/USTC-ncov-AutoReport)
![GitHub forks](https://img.shields.io/github/forks/Kobe972/USTC-ncov-AutoReport)

## 说明

**本打卡脚本仅供学习交流使用，请勿过分依赖。开发者对使用或不使用本脚本造成的问题不负任何责任，不对脚本执行效果做出任何担保，原则上不提供任何形式的技术支持。该版本相对于原版本做了如下修改：补充了login的data，使程序能成功登录现在的系统；将data.json改为山西省大同市相应的数据，2022年3月19日改回中区在校数据；根据原版本的pull requests进行了正则表达式以及http->https的改变；改变了requests，json，以及bs4的import顺序，解决了本地终端运行的NameError问题，现亲测本地可以成功运行，action方法也可；增加了验证码识别模块，可以应对新版身份认证系统的验证码机制。**

## 注意
* 中国科学技术大学身份认证系统自8月19日起对不常见IP采取了验证码，现在已破解，抽象成了一个类，代码是ustclogin.py。report.py已做了相应更改，可以照常使用。另外，目前身份认证有一个漏洞：在获取认证界面后再获取验证码图片，然后post的表单showCode填0，验证码放空即可直接跳过验证码。对应模块是ustclogin2.py，但是这个漏洞随时可能被修复，故没有放进代码。如果想整合，把report.py开头的from ustclogin改为 from ustclogin2即可
* **最近打卡系统更新频繁，本仓库会同时更新。如果脚本不能用，可以返回仓库确认更新后重新fork**。
* **记得使用前修改data.json的宿舍！**
* **记得使用前修改data.json的宿舍！**
* **记得使用前修改data.json的宿舍！**
* **记得上传自己的两码！**
* **最好修改一下跨校区理由，不要直接照搬表单！**

## 更新记录

- 20200831：增强稳定性
- 20200827：增加打卡失败重试功能，增加License
- 20200826：为配合学校最新规定，切换至Github Actions实现一天三次打卡（在这个fork版本中改回了一次）
- 20210816：本人fork了之前的脚本，并针对新的健康打卡页面做了修改
- 20210824：基于科大新身份认证的验证码部分添加了验证码识别
- 20220312：修改了Login类，简化了参数，使该模块可以更方便地做其他脚本的开发，也增强了脚本对url更新的适应性。另外对无验证码登录的payload做了调整。
- 20220316：听说出校报备由每周一报改为每日一报，增加自动报备功能（但脚本使用方法不变，只是附带多加了个功能）。
- 20220318：已经实行一日一报，表单和API有略微调整，脚本也相应做了改变。
- 20220319：打卡系统对表单进行了修改，因此相应修改了data.json。
- 20200323：表单再次发生变化，系统生成的start_date和end_date也无法通过验证，脚本进行了相应的修改。
- 20220330：打卡页面添加宿舍信息，报备URL做了略微的修改。**记得使用前修改data.json的宿舍！**
- 20220405：报备页面增加报备理由
- 20220408：上次修改脚本时把daliy改成了daily（妮可经典URL拼错），用burpsuite查出问题并做了修改。同时简化了部分代码。
- 20220526：自动上传两码，并修改了一些API

## 使用方法

0. **写在前面：请在自己fork的仓库中修改，并push到自己的仓库，不要直接修改本仓库，也不要将您的修改pull request到本仓库（对本仓库的改进除外）！如果尚不了解github的基本使用方法，请参阅[使用议题和拉取请求进行协作/使用复刻](https://docs.github.com/cn/github/collaborating-with-issues-and-pull-requests/working-with-forks)和[使用议题和拉取请求进行协作/通过拉取请求提议工作更改](https://docs.github.com/cn/github/collaborating-with-issues-and-pull-requests/proposing-changes-to-your-work-with-pull-requests)。**

1. 将本代码仓库fork到自己的github。

2. 根据自己的实际情况修改`data.json`的数据，参看下文。默认的`data.json`是中校区在校状态。**开发者不保证这些模板的正确性。**

3. 将修改好的代码push至master分支。如果不需要修改 `data.json`，请在 `README.md` 里添加一个空格并push，否则不会触发之后的步骤。**请在自己的仓库中修改，不要pull request到本仓库！**
4. 修改trace.jpg为自己的行程码，safe.jpg修改为健康码。**这一步别忘了！**

5. 点击Actions选项卡，点击`I understand my workflows, go ahead and enable them`.

6. 点击Settings选项卡，点击左侧Secrets，点击New secret，创建名为`STUID`，值为自己学号的secret。用同样方法，创建名为`PASSWORD`，值为自己中国滑稽大学统一身份认证密码的secret。这两个值不会被公开。

   ![secrets](imgs/image-20200826215037042.png)

7. 默认的打卡时间是每天的上午凌晨12:00，可能会有（延后）几分钟的浮动。如需选择其它时间，可以修改`.github/workflows/report.yml`中的`cron`，详细说明参见[安排的事件](https://docs.github.com/cn/actions/reference/events-that-trigger-workflows#scheduled-events)，请注意这里使用的是**国际标准时间UTC**，北京时间的数值比它大8个小时。建议修改默认时间，避开打卡高峰期以提高成功率。

8. 在Actions选项卡可以确认打卡情况。如果打卡失败（可能是临时网络问题等原因），脚本会自动重试，五次尝试后如果依然失败，将返回非零值提示构建失败。

9. 在Github个人设置页面的Notifications下可以设置Github Actions的通知，建议打开Email通知，并勾选"Send notifications for failed workflows only"。请及时查看邮件，如果失败会进行通知。

## 在本地运行测试

要在本地运行测试，需要安装python 3。我们假设您已经安装了python 3和pip 3，并已将其路径添加到环境变量。  
本地测试时，需要先修改report.py中upload.jpg的地址为该文件的绝对地址。

### 安装依赖

```shell
pip install -r requirements.txt
```

### 运行打卡程序

```shell
python report.py [DATA] [STUID] [PASSWORD]
```
其中，`[DATA]`是存放打卡数据的json文件的路径，`[STUID]`是学号，`[PASSWORD]`是统一身份认证的密码明文。

## data.json 数据获取方法

使用 F12 开发者工具抓包之后得到数据，按照 json 格式写入 `data.json` 中。

1. 登录进入 `https://weixine.歪比巴卜.edu.cn/2020/`，打开开发者工具（Chrome 可以使用 F12 快捷键），选中 Network 窗口：

![](./imgs/1.png)

2. 点击确认上报，点击抓到的 `daliy_report` 请求，在 `Headers` 下面找到 `Form Data` 这就是每次上报提交的信息参数。

![](./imgs/2.png)

3. 将找到的 Data 除 `_token` （每次都会改变，所以不需要复制，脚本中会每次获取新的 token 并添加到要提交的数据中）外都复制下来，存放在 `data.json` 中，并参考示例文件转换为对应的格式。

4. 通过push操作触发构建任务，检查上报数据是否正确。

## 许可

MIT License

Copyright (c) 2020 BwZhang

Copyright (c) 2020 Violin Wang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Stargazers over time
[![Stargazers over time](https://starchart.cc/Kobe972/USTC-ncov-AutoReport.svg)](https://starchart.cc/Kobe972/USTC-ncov-AutoReport)
