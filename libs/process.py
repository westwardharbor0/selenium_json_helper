from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from .consoler import TestConsole
from .logger import TestLogger

class TestProcess(TestLogger, TestConsole):
    def __init__(self, config, driver, wait):
        #begin the init of class
        self.driver = driver
        self.config = config
        self.wait = wait
        self._lines = []
        self.testing = self.config.get('tests')
        self.base = self.config.get('run_dir') + "/tests/" + self.config.get('paths test')
        self.folder = self.base+self.stamp()
        self.mfolder(self.folder)
        try:
            for test in self.testing:
                self.start_env()
                #load all test and run them
                self.test_name = test['folder']
                self.mfolder(self.folder+"/"+self.test_name)

                init_errs = False
                if 'initial_errors' in test:
                    init_errs = test['initial_errors']

                self.store_console(init_errs)

                self.progress_log('Starting test')
                #try:
                self.prepare_test(test)
                #except Exception as e:
                #    print('________________________________________')
                #    print(e)
                #    self.error_log('\n'+str(e))
                #    print('________________________________________')
                self.end_test()
        except Exception as ex:
            self.raise_msg(str(ex))



    #__________________________________
    def prepare_test(self, test):
        for stage in test['stages']:
            self.prepare_stage(stage, test)

    def prepare_stage(self, stage, test):
        typ = stage['type']
        if typ == "input":
            self.type_input(stage, test)
        elif typ == "button":
            self.type_button(stage, test)
        elif typ == "path":
            self.type_path(stage, test)
        elif typ == "wait":
            self.set_wait(stage, test)
        else:
            self.raise_msg("Not know type of stage yet {}".format(typ))
        time.sleep(5)
        #self.set_wait(stage, test, False)
    #__________________________________
    #__________________________________
    def restart_env(self):
        self.stop_env()
        self.start_env()

    def start_env(self):
        self.driver.get(self.config.get('url'))

    def stop_env(self):
        self.driver.close()

    def end_test(self):
        self.progress_log('___Ending test')
        self.stop_env()
        self.chmod(self.get_main_folder()+'/tests')

    def raise_msg(self, msg):
        self.error_log(msg)
        time.sleep(5)
        self.end_test()
        raise Exception(msg)
    #__________________________________
    #__________________________________
    def set_wait(self, stage, test, log=True):
        cont = stage['continue_on']
        if 'time' in cont:
            time.sleep(float(cont['time']))
            self.progress_log('___Waiting {}s'.format(cont['time']))
        elif 'element' in cont:
            b = By.CLASS_NAME if ('.' in cont['element']) else By.ID
            el = cont['element'].replace('#','').replace('.','')
            self.wait.until(EC.visibility_of_element_located((b, el)));
            self.progress_log('___Waiting on element')
        elif 'not_element' in cont:
            b = By.CLASS_NAME if ('.' in cont['not_element']) else By.ID
            el = cont['not_element'].replace('#','').replace('.','')
            self.wait.until(EC.invisibility_of_element_located((b, el)));
            self.progress_log('___Waiting on not_element')
        elif 'clickable' in cont:
            b = By.CLASS_NAME if ('.' in cont['clickable']) else By.ID
            el = cont['clickable'].replace('#','').replace('.','')
            self.wait.until(EC.element_to_be_clickable((b, el)));
            self.progress_log('___Waiting on clickable')
        else:
            self.raise_msg("Not know type of stage continue yet")

        if 'error_control' in stage:
            time.sleep(5)
            err = self.check_logs_code(stage['error_control'])
            if err:
                self.progress_log('___Got some error in console {}'.format(code))
                self.raise_msg("Code {} detected after stage ".format(code))
        self.make_screenshot(stage, test)

    def make_screenshot(self, stage, test):
        self.progress_log('___Taking screenshot')
        if test['screenshot']:
            folder = self.folder+"/"+test['folder']
            self.mfolder(folder)
            folder += "/screens"
            self.mfolder(folder)
            folder += "/"
            self.driver.save_screenshot(folder+self.stamp()+".png")


    def type_input(self, stage, test):
        self.progress_log('___Input action "{}"'.format(stage['value']))
        element = self.get_selector(stage['selector'])
        element.send_keys(stage['value'])

    def type_button(self, stage, test):
        self.make_screenshot(stage, test)
        self.progress_log('___Button action')
        element = self.get_selector(stage['selector'])
        element.click()
        self.make_screenshot(stage, test)

    def type_path(self, stage, test):
        self.progress_log('___Path action {}'.format(stage['action']))
        self.make_screenshot(stage, test)
        element = self.driver.find_element_by_xpath(stage['selector'])
        if stage['action'] == 'click':
            element.click()
        elif stage['action'] == 'input':
            element.send_keys(stage['value'])
        else:
            self.raise_msg('Unknown action on path')
