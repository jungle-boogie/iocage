"""CLI command to fetch a jail RELEASE."""
import click

from iocage.lib.ioc_fetch import IOCFetch

__cmdname__ = "fetch_cmd"
__rootcmd__ = True


@click.command(name="fetch", help="Fetch a version of FreeBSD for jail usage.")
@click.option("--http", "-h", default=False,
              help="Have --server define a HTTP server instead.", is_flag=True)
@click.option("--file", "-f", "_file", default=False,
              help="Use a local file directory for root-dir instead of FTP or"
                   " HTTP.", is_flag=True)
@click.option("--server", "-s", default="ftp.freebsd.org",
              help="FTP server to login to.")
@click.option("--user", "-u", default="anonymous", help="The user to use.")
@click.option("--password", "-p", default="anonymous@",
              help="The password to use.")
@click.option("--auth", "-a", default=None, help="Authentication method for "
                                                 "HTTP fetching. Valid "
                                                 "values: basic, digest")
@click.option("--release", "-r", help="The FreeBSD release to fetch.")
@click.option("--plugin", "-P", help="The plugin to fetch.")
@click.argument("props", nargs=-1)
@click.option("--count", "-c", default=1)
@click.option("--root-dir", "-d", help="Root directory " +
                                       "containing all the RELEASEs.")
def fetch_cmd(http, _file, server, user, password, auth, release, plugin,
              root_dir, props, count):
    """CLI command that calls fetch_release()"""
    if plugin:
        if count == 1:
            IOCFetch(server, user, password, auth, "", root_dir,
                     http=http, _file=_file).fetch_plugin(plugin, props, 0)
        else:
            for j in xrange(1, count + 1):
                IOCFetch(server, user, password, auth, "", root_dir,
                         http=http, _file=_file).fetch_plugin(plugin, props, j)
    else:
        IOCFetch(server, user, password, auth, release,
                 root_dir, http=http, _file=_file).fetch_release()
