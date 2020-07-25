import asyncio
import logging

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait

from scrapy_ajax_utils.selenium.driver import Webdriver
from scrapy_ajax_utils.selenium.request import SeleniumRequest
from scrapy_ajax_utils.utils import extract_domain_from_url

logger = logging.getLogger(__name__)


class SeleniumDownloadMiddleWare(object):
    """For selenium.

    注意：
        缓存 cookies 需要浏览器 User-Agent 请求头版本
        与设置脚本(或 Request)中的默认请求头保持一致
        否则某些网站可能会对此做验证 导致 cookies 无效
    """

    def __init__(self, creator):
        self.creator = creator
        self.cached_cookies = {}
        self._driver = None

    @property
    def driver(self):
        if self._driver is None:
            self._driver = self.creator.driver()
        return self._driver

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dm = cls(_make_driver_creator_from_settings(settings))
        crawler.signals.connect(dm.closed, signal=signals.spider_closed)
        return dm

    def process_request(self, request, spider):
        if not isinstance(request, SeleniumRequest) or self.has_cached_cookies(request):
            return
        return self.process_by_driver(request, spider, self.driver)

    def has_cached_cookies(self, request):
        if not request.cache_cookies:
            return False

        for domain in self.cached_cookies:
            if domain in request.url:
                request.cookies = self.cached_cookies[domain]
                return True
        return False

    def process_by_driver(self, request, spider, driver):
        driver.get(request.url)

        # 检查请求是否携带Cookies
        if request.cookies:
            if isinstance(request.cookies, list):
                for cookie in request.cookies:
                    driver.add_cookie(cookie)
            else:
                for k, v in request.cookies.items():
                    driver.add_cookie({'name': k, 'value': v})
            driver.get(request.url)

        if request.wait_until:
            WebDriverWait(driver, request.wait_time).until(request.wait_until)

        # Execute javascript code and save the result to meta.
        if request.script:
            request.meta['js_result'] = driver.execute_script(request.script)

        if request.handler:
            request.handler(driver, request, spider)

        for cookie_name, cookie_value in request.cookies.items():
            driver.add_cookie(
                {
                    'name': cookie_name,
                    'value': cookie_value
                }
            )
        request.cookies = driver.get_cookies()
        request.meta['driver'] = driver

        if request.cache_cookies:
            domain = extract_domain_from_url(request.url)
            self.cached_cookies[domain] = request.cookies
        else:
            body = str.encode(driver.page_source)
            return HtmlResponse(
                driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )

    def closed(self):
        if self._driver is not None:
            self._driver.quit()
            logger.debug('Selenium closed')


class SeleniumNoBlockingDownloadMiddleWare(SeleniumDownloadMiddleWare):
    """
    需设置 TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
    参考：https://doc.scrapy.org/en/latest/topics/asyncio.html
    """
    lock = asyncio.Lock()

    @classmethod
    def from_crawler(cls, crawler):
        max_drivers = crawler.settings.get('SELENIUM_MAX_DRIVERS', 5)
        dm = cls(_make_driver_creator_from_settings(crawler.settings), max_drivers)
        crawler.signals.connect(dm.closed, signal=signals.spider_closed)
        return dm

    def __init__(self, creator, max_drivers):
        super().__init__(creator)
        self.max_drivers = max_drivers
        self.loop = asyncio.get_event_loop()
        self.launched_drivers = []

    async def process_request(self, request, spider):
        if not isinstance(request, SeleniumRequest) or self.has_cached_cookies(request):
            return

        async with self.lock:
            if len(self.launched_drivers) < self.max_drivers:
                self.launched_drivers.append(DriverItem(self.creator.driver()))

        for driver_item in self.launched_drivers:
            if driver_item.is_idle:
                driver_item.is_idle = False
                response = await self.loop.run_in_executor(None, self.process_by_driver, request, spider, driver_item.driver)
                driver_item.is_idle = True
                return response
        else:
            # Maybe next time ..
            request.dont_filter = True
            return request

    def closed(self):
        for driver_item in self.launched_drivers:
            driver_item.driver.quit()
        super().closed()


class DriverItem(object):

    def __init__(self, driver):
        self.driver = driver
        self.is_idle = True


def _make_driver_creator_from_settings(settings):
    headless = settings.getbool('SELENIUM_HEADLESS', True)
    disable_image = settings.get('SELENIUM_DISABLE_IMAGE', True)
    driver_name = settings.get('SELENIUM_DRIVER_NAME', 'chrome')
    executable_path = settings.get('SELENIUM_DRIVER_PATH')
    user_agent = settings.get('USER_AGENT')
    creator = Webdriver(headless=headless,
                        disable_image=disable_image,
                        driver_name=driver_name,
                        executable_path=executable_path,
                        user_agent=user_agent)
    return creator
