from loadcsv import LoadCSV
from zabbixhost import ZabbixAPI

class Importer:
    def __init__(self, filename, user, password, url):
        self.hostlist = LoadCSV(filename).export()
        self.zabbix = ZabbixAPI(user, password, url)
        self.zabbix.login()

    def debug(self):
        print(self.hostlist)
        for line in self.hostlist:
            print(line['Template'].split(','))
            print(line['Group'])
            print(line['Name'])
            print(line['IP'])

    def chk_ip(self, ip_str):
        sep = ip_str.split('.')
        if len(sep) != 4:
            return False
        for i, x in enumerate(sep):
            try:
                int_x = int(x)
                if int_x < 0 or int_x > 255:
                    return False
            except ValueError as e:
                return False
        return True

    def create_host(self):
        for line in self.hostlist:
            if self.chk_ip(line['IP']) is False:
                continue
            self.zabbix.get_template_id(line['Template'].split(','))
            self.zabbix.get_group_id(line['Group'])
            self.zabbix.create_host(line['Name'], line['IP'], line['Port'])
