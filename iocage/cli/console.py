"""Allows a user to console into an iocage jail."""
import logging
from subprocess import Popen

import click

from iocage.lib.ioc_json import IOCJson
from iocage.lib.ioc_list import IOCList
from iocage.lib.ioc_start import IOCStart

__cmdname__ = "console_cmd"
__rootcmd__ = True


@click.command(name="console", help="Login to a jail.")
@click.argument("jail")
@click.option("--force", "-f", default=False, is_flag=True)
def console_cmd(jail, force):
    """
    Runs jexec to login into the specified jail. Accepts a force flag that
    will attempt to start the jail if it is not already running.
    """
    lgr = logging.getLogger('ioc_cli_console')
    # TODO: setfib support
    jails, paths = IOCList("uuid").get_datasets()

    _jail = {tag: uuid for (tag, uuid) in jails.iteritems() if
             uuid.startswith(jail) or tag == jail}

    if len(_jail) == 1:
        tag, uuid = next(_jail.iteritems())
        path = paths[tag]

        iocjson = IOCJson(path)
        conf = iocjson.load_json()
        login_flags = conf["login_flags"].split()
        status = IOCList().get_jid(uuid)[0]
    elif len(_jail) > 1:
        lgr.error("Multiple jails found for"
                  " {}:".format(jail))
        for t, u in sorted(_jail.iteritems()):
            lgr.error("  {} ({})".format(u, t))
        raise RuntimeError()
    else:
        raise RuntimeError("{} not found!".format(jail))

    if not status and not force:
        raise RuntimeError("{} ({}) is not running!".format(uuid, tag))

    if not status and force:
        lgr.info("{} ({}) is not running".format(uuid, tag) +
                 ", starting jail.")
        IOCStart(uuid, path, silent=True).start_jail(jail, conf)
        status = True

    if status:
        Popen(["jexec", "ioc-{}".format(uuid), "login"] +
              login_flags).communicate()
