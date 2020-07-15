import ipaddress
import subprocess
from database import database
import re

class Runner:
    def __init__(self, flag_regex):
        self.targets = open('targets.txt').readlines()
        self.targets = list(map(lambda x: ipaddress.ip_address(x), self.targets))

        self.exploits = self.__get_exploits()

        self.flag_regex = re.compile(flag_regex)

    def __get_exploits(self):
        ret = database.get_exploits()
        exploits = []
        for exp in ret:
            exploits.append({'filename':exp[1], 'service_id':exp[3], 'service':exp[4], 'port':exp[5]})
        return exploits

    def do_round(self):
        print("Starting round")
        for exploit in self.exploits:
            print("Running exploit: ", exploit['filename'])
            for target in self.targets:
                res = subprocess.check_output(['./exploits/' + exploit['filename'], str(target), str(exploit['port'])])
                matches = self.flag_regex.findall(res)
                if (matches):
                    for match in matches:
                        database.insert_flag(str(match, 'utf-8'), exploit['service_id'])


