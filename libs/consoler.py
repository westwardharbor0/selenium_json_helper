


class TestConsole:
    def store_console(self, init_errs=False):
        self._lines = []
        for entry in self.get_console():
            self._lines.append(entry)
            if init_errs:
                res = self.find_errors_entry(entry, init_errs)
                if res:
                    self.raise_msg(
                    'An initial error occurred in test {}'.format(res))
            self.update_log(entry)

        return None

    def get_stored(self):
        return self._lines

    def get_console(self):
        _lines = []
        for entry in self.driver.get_log('browser'):
            #if type(entry) is tuple:
            #    for sub in entry:
            #        _lines.append(sub)
            _lines.append(entry)
        return _lines

    def get_updates(self):
        pairs = zip(self._lines, self.get_console())
        self.store_console()
        diff = [(x, y) for x, y in pairs if x != y]
        ret = []
        for entry in diff:
            if type(entry) is tuple:
                for sub in entry:
                    self.update_log(sub)
                    ret.append(sub)
            else:
                self.update_log(entry)
                ret.append(entry)
        return ret

    def update_log(self, entry):
        self.console_log(self.parse_entry(entry))

    def check_logs_code(self, codes):
        entries = self.get_updates()
        for entry in entries:
            if type(entry) is dict:
                res = self.find_errors_entry(entry, codes)
                if not res:
                    return res
            else:
                print(type(entry))
                print(entry)

        return None

    def find_errors_entry(self, entry, codes):
        for code in codes:
            if code in entry['message']:
                return code
        return None

    def parse_entry(self, entry):
        if type(entry) is tuple:
            entry = entry[0]
        return "{} | {} | {}".format(entry['level'], entry['source'], entry['message'])
