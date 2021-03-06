"""iocage exec module."""
import logging
from subprocess import Popen

from iocage.lib.ioc_json import IOCJson
from iocage.lib.ioc_list import IOCList
from iocage.lib.ioc_start import IOCStart


class IOCExec(object):
    """Run jexec with a user inside the specified jail."""

    def __init__(self, command, uuid, tag, path, host_user="root",
                 jail_user=None, plugin=False, plugin_dir=None):
        self.command = command
        self.uuid = uuid
        self.tag = tag
        self.path = path
        self.host_user = host_user
        self.jail_user = jail_user
        self.plugin = plugin
        self.plugin_dir = plugin_dir
        self.lgr = logging.getLogger('ioc_exec')

    def exec_jail(self):
        # TODO: Exec fib support
        if self.jail_user:
            flag = "-U"
            user = self.jail_user
        else:
            flag = "-u"
            user = self.host_user

        if self.plugin:
            self.path = self.plugin_dir

        jid = IOCList().get_jid(self.uuid)[0]
        if not jid:
            self.lgr.info("{} ({}) is not running".format(self.uuid, self.tag) +
                          ", starting jail.")
            conf = IOCJson(self.path).load_json()

            IOCStart(self.uuid, self.path, silent=True).start_jail(self.tag,
                                                                   conf)
            self.lgr.info("\nCommand output:")

        Popen(["jexec", flag, user, "ioc-{}".format(self.uuid)] +
              list(self.command)).communicate()
