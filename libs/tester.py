
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#________________________________________#
from .config import TestConfig
from .process import TestProcess
from .utils import TestUtils

class SiteTester(TestUtils):
    def __init__(self,*,log_path=None,screen_path=None,config=None,run_dir=""):
        self.config = TestConfig(config)
        self.config.set('run_dir', run_dir)
        self.set_desired()
        self.screen_path = screen_path
        _service_args = ["--verbose", "--log-path={}".format(
                            self.get_main_folder()+"chrome.log")]
        self.set_chrome_options()
        self.driver = webdriver.Chrome(
                    chrome_options=self.chrome_options,
                    service_args=_service_args,
                    desired_capabilities=self.d
                    )
        self.wait = WebDriverWait(self.driver, 80)
        self.process = TestProcess(self.config, self.driver, self.wait)

    def set_desired(self):
        self.d = DesiredCapabilities.CHROME
        self.d['loggingPrefs'] = { 'browser':'ALL' }

    def set_chrome_options(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
