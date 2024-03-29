import unittest

from scraperai import SeleniumCrawler
from scraperai.crawlers.webdriver import WebdriversManager, SelenoidSettings, DefaultChromeWebdriver
from scraperai.crawlers.webdriver.manager import TooManySessions
from .settings import selenoid_capabilities, SELENOID_URL


class TestWebdrivers(unittest.TestCase):
    test_url = 'https://apple.com'
    test_substr = '<link rel="canonical" href="https://www.apple.com/">'

    def test_local_driver_connection(self):
        driver = DefaultChromeWebdriver()
        driver.get(self.test_url)
        self.assertTrue(self.test_substr in driver.page_source)
        driver.quit()

    def test_remote_driver_connection(self):
        webmanager = WebdriversManager(selenoids=[
            SelenoidSettings(url=SELENOID_URL, max_sessions=1, capabilities=selenoid_capabilities)
        ])
        driver = webmanager.create_driver()
        driver.get(self.test_url)
        self.assertTrue(self.test_substr in driver.page_source)
        driver.quit()

    def test_remote_driver_limits(self):
        webmanager = WebdriversManager(selenoids=[
            SelenoidSettings(url=SELENOID_URL, max_sessions=1, capabilities=selenoid_capabilities)
        ])
        driver = webmanager.create_driver()
        driver.get(self.test_url)
        self.assertTrue(self.test_substr in driver.page_source)
        self.assertRaises(TooManySessions, webmanager.create_driver)
        driver.quit()

    def test_remote_driver_recreation(self):
        webmanager = WebdriversManager(selenoids=[
            SelenoidSettings(url=SELENOID_URL, max_sessions=2, capabilities=selenoid_capabilities)
        ])
        driver = webmanager.create_driver()
        driver.get(self.test_url)
        driver_url = driver.url
        driver_session_id = driver.get_session_id()

        driver = webmanager.from_session_id(driver_url, driver_session_id)
        self.assertTrue(self.test_substr in driver.page_source)
        driver.quit()

    def test_click_button(self):
        driver = DefaultChromeWebdriver()
        driver.get('https://xn--80akogvo.xn--k1abfdfi3ec.xn--p1ai/goods-company/view/39')
        xpath = "//*[@class='ajax-pagination-more']"
        crawler = SeleniumCrawler(driver)
        crawler.highlight_by_xpath("//*[@class='product']", 'red', 5)
        crawler.highlight_by_xpath("//*[@class='product']//a[@class='product_img']/@href", 'red', 5)
        crawler.get_screenshot_as_base64()
        crawler.click(xpath)
        driver.quit()


if __name__ == '__main__':
    unittest.main()
