from selenium import webdriver
from time import sleep
from PIL import Image, ImageEnhance  # 获取图片验证码模块
import pytesseract, unittest, time
from selenium.webdriver.common.keys import Keys
import win32com.client  # 上传文件模块
import HTMLTestRunner

from TestRunner import createTestRunner
from sendEmail import sEmail


class NhyktTest(unittest.TestCase):
    global timelast, Phone, courseName

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("https://admin.tiac.youkehudong.com/")
        cls.driver.implicitly_wait(5)
        cls.driver.find_element_by_css_selector('[class="loginChange"]').click()

    @classmethod
    def tearDownClass(cls):
        print("-----------测试结束！结果发送中。。。-----------")

    def GetCode(self):  # 获取图片验证码

        # 浏览器页面截屏
        self.driver.get_screenshot_as_file(r"D:\\a.png")

        # 定位验证码位置及大小
        location = self.driver.find_element_by_id('s-canvas').location

        size = self.driver.find_element_by_id('s-canvas').size

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        # 从文件读取截图，截取验证码位置再次保存
        img = Image.open(r"D:\\a.png").crop((left, top, right, bottom))

        img = img.convert('L')  # 转换模式：L | RGB

        img = ImageEnhance.Contrast(img)  # 增强对比度

        img = img.enhance(2.0)  # 增加饱和度

        img.save(r"D:\\a.png")

        # 再次读取识别验证码
        img = Image.open(r"D:\\a.png")

        code = pytesseract.image_to_string(img).replace(' ', '')
        # code= pytesser.image_file_to_string(screenImg)
        return code.strip()

    def test001Login(self):  # admin登录
        sleep(1)
        self.driver.find_elements_by_css_selector('span > input')[0].send_keys('admin')
        self.driver.find_elements_by_css_selector('span > input')[1].send_keys('a123456')
        code = self.GetCode()
        # 输入验证码
        self.driver.find_elements_by_css_selector('span > input')[2].send_keys(code)
        self.driver.find_element_by_css_selector('span > button').click()

        while True:
            # 判断是否有这个元素
            try:
                warn = self.driver.find_element_by_css_selector('[class="ant-form-explain"]')
            except:
                break
            if warn:
                self.driver.find_element_by_id('s-canvas').click()
                code = self.GetCode()
                inp = self.driver.find_elements_by_css_selector('span > input')[2]
                # 清除输入框内容
                inp.send_keys(Keys.CONTROL + 'a')
                inp.send_keys(Keys.DELETE)
                # 输入验证码
                inp.send_keys(code)
                self.driver.find_element_by_css_selector('span > button').click()

            else:
                break

        return print('登录成功')

    def test007AddLiveCourse(self):
        global courseName
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[2]/div').click()
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[2]/ul/li[3]').click()
        sleep(1)
        self.driver.find_element_by_xpath('//*[@class="button_group"]/button[1]').click()
        # 输入课程名称
        timelast = int(time.time() * 10000) % 10000
        courseName = 'rock课程' + str(timelast)
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-input"]').send_keys(courseName)
        # 点击上传封面
        self.driver.find_element_by_css_selector('[class="ant-upload"]').click()
        sh = win32com.client.Dispatch("WScript.shell")
        sleep(1)
        sh.Sendkeys('D:\\a.png\n')  # \n == 回车
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-btn ant-btn-primary"]').click()
        # 选择学科
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-select-selection__rendered"]').click()
        self.driver.find_element_by_css_selector(
            '[class="ant-select-dropdown-menu-item ant-select-dropdown-menu-item-active"]').click()
        # 选择上课年级
        self.driver.find_element_by_css_selector('[class="ant-tag"]').click()
        sleep(1)
        self.driver.find_elements_by_css_selector('[class="input-radio"]')[6].click()
        self.driver.find_elements_by_css_selector('[class="ant-btn ant-btn-primary"]')[1].click()
        # 输入课程简介
        self.driver.switch_to.frame('ueditor_0')
        self.driver.find_elements_by_css_selector('[class="view"]')[1].send_keys('测试课程简介')
        # 回到之前的iframe
        self.driver.switch_to.default_content()
        # 点击提交
        sleep(1)
        self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
        # 获取温馨提示弹窗
        warning = self.driver.find_element_by_css_selector('[class="ant-modal-confirm-content"]').text
        if warning:
            print('课程新增成功')
            print('课程管理测试成功')
        else:
            print('课程新增不成功')
        # 点击以后再说
        self.driver.find_elements_by_css_selector('[class="ant-btn"]')[1].click()
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[2]/ul/li[3]').click()
        # 选择去查看
        sleep(1)
        self.driver.find_element_by_css_selector(' tr:nth-child(1) > td:nth-child(9) > a:nth-child(1)').click()
        # 滑到页面最下面点击去排课
        self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-btn ant-btn-primary"]').click()
        return courseName

    def test008CreateLive(self):
        global courseName
        # 进入快速排课,输入上课老师
        self.driver.find_element_by_css_selector('[class="ant-select ant-select-enabled ant-select-no-arrow"]').click()
        self.driver.find_elements_by_css_selector('[class="ant-select-search__field"]')[1].send_keys('rock')
        sleep(1)
        self.driver.find_element_by_css_selector('[class="title"]').click()

        # 选择开课日期为今天
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-calendar-picker"]').click()
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-calendar-today-btn "]').click()
        # 选择开课时间
        nowTime = time.strftime('%H%M', time.localtime(time.time()))
        sleep(1)
        self.driver.find_elements_by_css_selector('[class="ant-time-picker-input"]')[0].click()
        allHour = self.driver.find_elements_by_xpath('//*[@class="ant-time-picker-panel-select"][1]/ul/li')
        allMinute = self.driver.find_elements_by_xpath('//*[@class="ant-time-picker-panel-select"][2]/ul/li')
        browserHour = self.driver.find_elements_by_css_selector('[class="ant-time-picker-panel-select-option-selected"]')[0]
        browserMinute = self.driver.find_elements_by_css_selector('[class="ant-time-picker-panel-select-option-selected"]')[1]
        nowMinute = nowTime[2] + nowTime[3]
        nowHour = nowTime[0] + nowTime[1]
        if int(nowMinute) > 59:
            subscript1 = int(browserHour.text)+1  # 下标
            allHour[subscript1].click()
        else:
            subscript2 = int(browserMinute.text)+2
            allMinute[subscript2].click()

        self.driver.find_elements_by_css_selector('[class="ant-time-picker-input"]')[1].click()
        etime = str(int(nowHour)+1)+':'+str(nowMinute)
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-time-picker-panel-input "]').send_keys(etime)
        self.driver.find_element_by_css_selector('[class="title"]').click()
        # 输入直播名称
        self.driver.find_elements_by_css_selector('[class="ant-input"]')[0].send_keys('rock测试直播')
        self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
        # 点击提交
        self.driver.find_element_by_css_selector('[class="addForm ant-btn ant-btn-primary"]').click()
        liveCourse = self.driver.find_element_by_css_selector(' tr:nth-child(1) > td:nth-child(7)')
        if courseName == liveCourse.text:
            print('排课成功')
        return print('排课管理测试成功')

    def test009TeacherLogin(self):
        self.driver.execute_script('window.open("https://admin.tiac.youkehudong.com")')
        allHandles = self.driver.window_handles
        self.driver.switch_to.window(allHandles[-1])
        self.driver.find_element_by_css_selector('[class="loginChange"]').click()
        sleep(1)
        self.driver.find_elements_by_css_selector('span > input')[0].send_keys('T2010030489953')
        self.driver.find_elements_by_css_selector('span > input')[1].send_keys('a123456')
        code = self.GetCode()
        # 输入验证码
        self.driver.find_elements_by_css_selector('span > input')[2].send_keys(code)
        self.driver.find_element_by_css_selector('span > button').click()

        while True:
            # 判断是否有这个元素
            try:
                warn = self.driver.find_element_by_css_selector('[class="ant-form-explain"]')
            except:
                break
            if warn:
                self.driver.find_element_by_id('s-canvas').click()
                code = self.GetCode()
                inp = self.driver.find_elements_by_css_selector('span > input')[2]
                # 清除输入框内容
                inp.send_keys(Keys.CONTROL + 'a')
                inp.send_keys(Keys.DELETE)
                # 输入验证码
                inp.send_keys(code)
                self.driver.find_element_by_css_selector('span > button').click()

            else:
                break
        ele = self.driver.find_element_by_css_selector('[title="rock"]')
        if ele:
            pass
        else:
            print('未登录')
        return print('老师登录成功')

    def test010TeacherLive(self):
        course = self.driver.find_element_by_css_selector(' tr:nth-child(1) > td:nth-child(5)').text
        # 点击进入直播
        self.driver.find_element_by_css_selector(' tr:nth-child(1) > td:nth-child(9) > span:nth-child(2) > a').click()
        # 获取所有句柄
        sleep(1)
        allHandles = self.driver.window_handles
        # 切换到最后一个句柄
        self.driver.switch_to.window(allHandles[-1])
        # 点击 三次下一步
        self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[0].click()
        self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[1].click()
        self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[1].click()
        # 点击 进入课堂
        self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[1].click()
        # 点击 上课
        self.driver.find_elements_by_css_selector('[class="tic-btn headerbtn start"]')[0].click()
        # 判断是否上课
        sleep(1)
        ele = self.driver.find_element_by_css_selector('[class="left-time menu-course__time"]')
        if ele:
            print(course + '上课成功')
        else:
            print('未上课')
        return print('老师直播测试成功')

    def test011StudentLogin(self):
        self.driver.execute_script('window.open("https://student.tiac.ykhdedu.com/login")')
        allHandles = self.driver.window_handles
        self.driver.switch_to.window(allHandles[-1])
        self.driver.find_element_by_css_selector('[class="blue_color"]').click()
        sleep(1)
        self.driver.find_elements_by_css_selector('span > input')[0].send_keys('S1992071833190')
        self.driver.find_elements_by_css_selector('span > input')[1].send_keys('a123456')
        code = self.GetCode()
        # 输入验证码
        self.driver.find_elements_by_css_selector('span > input')[2].send_keys(code)
        self.driver.find_element_by_css_selector('span > button').click()

        while True:
            # 判断是否有这个元素
            try:
                warn = self.driver.find_element_by_css_selector('[class="ant-form-explain"]')
            except:
                break
            if warn:
                self.driver.find_element_by_id('s-canvas').click()
                code = self.GetCode()
                inp = self.driver.find_elements_by_css_selector('span > input')[2]
                # 清除输入框内容
                inp.send_keys(Keys.CONTROL + 'a')
                inp.send_keys(Keys.DELETE)
                # 输入验证码
                inp.send_keys(code)
                self.driver.find_element_by_css_selector('span > button').click()

            else:
                break

        studentName = self.driver.find_element_by_css_selector('[class="username"]').text
        if studentName:
            print('学生登录成功')

        return

    def test012StudentIntoLive(self):
        # 点击进入直播
        self.driver.find_element_by_xpath('//*[@class="option_item online"]/span').click()
        sleep(2)
        allHandles = self.driver.window_handles
        self.driver.switch_to.window(allHandles[-1])
        sleep(2)
        ele = self.driver.find_element_by_css_selector('[class="left-time menu-course__time"]')
        if ele:
            print('学生进入直播间成功')

        self.driver.switch_to.window(allHandles[2])
        # 老师关闭直播
        self.driver.find_element_by_css_selector('[class="tic-btn headerbtn end red"]').click()
        self.driver.find_element_by_css_selector('[class="ivu-btn ivu-btn-primary ivu-btn-large"]').click()
        return print('学生进入直播间测试正常')




if __name__ == '__main__':
    createTestRunner(r"D:\PythonObjects\nhyktObject",
                     "t2.py",
                     r"D:\PythonObjects\nhyktObject\report.html",
                     "南海云课堂管理后台自动化测试报告",
                     "主要流程测试")
    # sleep(1)
    # sEmail()