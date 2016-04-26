# coding=utf-8
"""
Instituto Tecnológico de Costa Rica
Ingeniería en Computación
Redes de Computadoras
Profesor: Kevin Moraga
Estudiantes:
    Daniel Solís Méndez
    Melvin Elizondo Pérez
I Semestre 2016
"""

import csv


class HostManager:
    """
    Class that takes control of the hosts connected
    to each of the routers.
    """

    def __init__(self, hosts_file="hosts.csv"):
        self.hosts_file = hosts_file
        self.hosts = []
        self._load_hosts()

    def _load_hosts(self):
        """
        Keeps in memory the hosts connected to a fast check.
        """
        self.hosts = []
        with open(self.hosts_file) as hosts_file:
            fieldnames = ['username', 'ip', 'port']
            hosts = csv.DictReader(hosts_file, fieldnames=fieldnames)
            for host in hosts:
                self.hosts.append(host)

    def exists(self, username):
        """
        Checks if a username is connected to a router.
        :param username: user to check.
        :return: True or False.
        """
        if self.check_loaded(username):
            return True

        self._load_hosts()

        if self.check_loaded(username):
            return True
        return False

    def register(self, host):
        """
        Registers a new host in the router.
        Add host info to the hosts file.
        :param host: host object to register.
        """
        exists = self.exists(host["username"])
        fieldnames = ['username', 'ip', 'port']
        hosts_file = open(self.hosts_file, "a")
        writer = csv.DictWriter(hosts_file, fieldnames=fieldnames)
        writer.writerow(host)

    def check_loaded(self, username):
        """
        Checks if a username is loaded in the hosts list.
        :param username: user to check.
        :return: True if loaded, False if not.
        """
        for host in self.hosts:
            if host["username"] == username:
                return True

        return False

    def delete(self, username):
        """
        Deletes a username from the hosts list
        when this gets disconnected.
        :param username: user to delete
        """
        newlist = [host for host in self.hosts if not host["username"] == username]
        self.hosts = newlist
        fieldnames = ['username', 'ip', 'port']
        hosts_file = open(self.hosts_file, "w")
        writer = csv.DictWriter(hosts_file, fieldnames=fieldnames)
        writer.writerows(newlist)

    def get_user(self, user):
        """
        Returns the information of the specified user
        :param user: user to query.
        :return: information object
        """
        user_info = [host for host in self.hosts if host["username"] == user]
        return user_info[0]

    def get_users(self):
        """
        Returns the list of hosts connected
        to the router.
        """
        self._load_hosts()
        return self.hosts

