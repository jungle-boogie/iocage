"""CLI command to run a command inside a jail."""
import logging

import click

from iocage.lib.ioc_exec import IOCExec
from iocage.lib.ioc_list import IOCList

__cmdname__ = "exec_cmd"
__rootcmd__ = True


@click.command(name="exec", help="Run a command inside a specified jail.")
@click.option("--host_user", "-u", default="root",
              help="The host user to use.")
@click.option("--jail_user", "-U", help="The jail user to use.")
@click.argument("jail", required=True, nargs=1)
@click.argument("command", nargs=-1, type=click.UNPROCESSED)
def exec_cmd(command, jail, host_user, jail_user):
    """Runs the command given inside the specified jail as the supplied user."""
    lgr = logging.getLogger('ioc_cli_exec')

    if host_user and jail_user:
        raise RuntimeError("Please only specify either host_user or"
                           " jail_user, not both!")

    jails, paths = IOCList("uuid").get_datasets()
    _jail = {tag: uuid for (tag, uuid) in jails.iteritems() if
             uuid.startswith(jail) or tag == jail}

    if len(_jail) == 1:
        tag, uuid = next(_jail.iteritems())
        path = paths[tag]
    elif len(_jail) > 1:
        lgr.error("Multiple jails found for"
                  " {}:".format(jail))
        for t, u in sorted(_jail.iteritems()):
            lgr.error("  {} ({})".format(u, t))
        raise RuntimeError()
    else:
        raise RuntimeError("{} not found!".format(jail))

    IOCExec(command, uuid, tag, path, host_user, jail_user).exec_jail()
