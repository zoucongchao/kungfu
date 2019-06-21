import os
import click
import kungfu.yijinjing.journal as kfj
from kungfu.log import create_logger


@click.group(invoke_without_command=True)
@click.option('-f', '--home', type=str, help='kungfu home folder')
@click.option('-l', '--log_level', type=click.Choice(['trace', 'debug', 'info', 'warning', 'error', 'critical']),
              default='warning', help='logging level')
@click.option('-n', '--name', type=str, help='name for the process, defaults to command if not set')
@click.pass_context
def kfc(ctx, home, log_level, name):
    os.environ['KF_HOME'] = ctx.home = home
    os.environ['KF_LOG_LEVEL'] = log_level

    ctx.logger = create_logger(name, log_level)

    # have to keep locator alive from python side
    # https://github.com/pybind/pybind11/issues/1546
    ctx.locator = kfj.Locator(ctx)

    if ctx.invoked_subcommand is None:
        click.echo(kfc.get_help(ctx))
    else:
        ctx.name = name if name else ctx.invoked_subcommand
    pass


def pass_ctx_from_parent(ctx):
    ctx.home = ctx.parent.home
    ctx.logger = ctx.parent.logger
    ctx.locator = ctx.parent.locator
    ctx.name = ctx.parent.name


def execute():
    kfc(auto_envvar_prefix='KF')