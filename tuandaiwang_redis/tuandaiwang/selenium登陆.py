from selenium import webdriver
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#设置chromedriver不加载图片
# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs",prefs)
#
#
# brower = webdriver.Chrome(chrome_options=chrome_opt)
# brower.get('https://passport.tdw.cn/2login?ret=%2F%2Fwww.tdw.cn')
# #brower.get('https://passport.tdw.cn/2login?ret=%2F%2Fwww.tdw.cn')
# brower.find_element_by_css_selector('#username').send_keys('minmin520')
# brower.find_element_by_css_selector('#password').send_keys('minmin520')##loginBtn
# brower.find_element_by_css_selector('#loginBtn').click()##loginBtn

#phantomjs 多进程性能下降严重


browser_type = 'Chrome'

class CookiesGenerator(object):
        def __init__(self , browser_type):
            self.browser_type = browser_type
            self.run()


        def _init_browser(self, browser_type):
            """
            通过browser参数初始化全局浏览器供模拟登录使用
            :param browser: 浏览器 PhantomJS/ Chrome
            :return:
            """
            if browser_type == 'PhantomJS':
                caps = DesiredCapabilities.PHANTOMJS
                caps[
                    "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
                self.browser = webdriver.PhantomJS(desired_capabilities=caps)
                self.browser.set_window_size(1400, 500)
                return self.browser
            elif browser_type == 'Chrome':
                self.browser = webdriver.Chrome()
                return self.browser

        def run(self):
            browser = self._init_browser(browser_type=self.browser_type)
            browser.get('https://passport.tdw.cn/2login?ret=%2F%2Fwww.tdw.cn')
            wait = WebDriverWait(browser, 10)
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#username'))
            )
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#loginBtn')))
            input.send_keys('minmin520')
            browser.find_element_by_css_selector('#password').send_keys('minmin520')  ##loginBtn
            submit.click()


            try :
                success=wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#topinfo > span')))
                print("登陆成功")
                self.close()
            except:
                print("登陆失败")
                self.close()



        def close(self):
            try:
                print('Closing Browser')
                self.browser.close()
                del self.browser
            except TypeError:
                print('Browser not opened')


if __name__ == '__main__':
    CookiesGenerator(browser_type)

