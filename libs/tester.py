
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

#________________________________________#
from .config import TestConfig
from .process import TestProcess
from .utils import TestUtils

PROXY = "socks5://localhost:9050"

class SiteTester(TestUtils):
    def __init__(self,*,log_path=None,screen_path=None,config=None,run_dir=""):
        self.config = TestConfig(config)
        self.config.set('run_dir', run_dir)

        self.involve_tor()

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
    
    def involve_tor(self):
        if( not self.config.get("tor") ):
            return

        from stem import Signal
        from stem.control import Controller
        with Controller.from_port(port = self.config.get("tor port")) as c:
            c.authenticate()
            c.signal(Signal.NEWNYM)
            print("Getting new IP from TOR")

    def set_chrome_options(self):
        self.chrome_options = webdriver.ChromeOptions()

        if( self.config.get("random_agent") ):
            from fake_useragent import UserAgent
            ua = UserAgent()
            user_agent = ua.random
            print("Getting a random user-agent")
            self.chrome_options.add_argument('user-agent={}'.format(user_agent))

        if( self.config.get("screen_size") ):
            self.chrome_options.add_argument("window-size={},{}".format(
                self.config.get("screen_size width"),
                self.config.get("screen_size height")
            ))
            print("Window size set to {} x {}".format(
                self.config.get("screen_size width"),
                self.config.get("screen_size height")
            ))

        self.chrome_options.add_argument('--proxy-server={}'.format(PROXY))
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
