import csv


class HostManager:

    def __init__(self, hosts_file="hosts.csv"):
        self.hosts_file = hosts_file
        self.hosts = []
        self._load_hosts()

    def _load_hosts(self):
        self.hosts = []

        with open(self.hosts_file) as hosts_file:
            fieldnames = ['username', 'ip', 'port']
            hosts = csv.DictReader(hosts_file, fieldnames=fieldnames)
            for host in hosts:
                self.hosts.append(host)

    def exists(self, username):
        if self.check_loaded(username):
            return True

        self._load_hosts()

        if self.check_loaded(username):
            return True
        print "User is OK"
        return False

    def register(self, host):
        exists = self.exists(host["username"])
        fieldnames = ['username', 'ip', 'port']
        hosts_file = open(self.hosts_file, "a")
        writer = csv.DictWriter(hosts_file, fieldnames=fieldnames)
        writer.writerow(host)

    def check_loaded(self, username):
        for host in self.hosts:
            if host["username"] == username:
                return True

        return False

    def delete(self, username):
        newlist = [host for host in self.hosts if not host["username"] == username]
        self.hosts = newlist
        fieldnames = ['username', 'ip', 'port']
        hosts_file = open(self.hosts_file, "w")
        writer = csv.DictWriter(hosts_file, fieldnames=fieldnames)
        writer.writerows(newlist)

    def get_user(self, user):
        user_info = [host for host in self.hosts if host["usernmae"] == user]
        print user_info
        return user_info

