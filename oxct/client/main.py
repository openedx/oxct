import json
import sys
from urllib.request import urlopen
from urllib.parse import urlencode

import click

from oxct.__about__ import __version__
from oxct.common import fmt, exceptions


class Context:
    def __init__(self, host):
        self.oxct_host = host


def main():
    try:
        cli()  # pylint: disable=no-value-for-parameter
    except exceptions.OxctError as e:
        fmt.echo_error(e.message)
        sys.exit(1)


@click.group()
@click.version_option(version=__version__)
@click.option(
    "-h",
    "--host",
    default="https://oxct.overhang.io",
    envvar="OXCT_HOST",
    help="oxct host",
)
@click.pass_context
def cli(context, host):
    context.obj = Context(host)


@click.group(name="community", help="Display information about the Open edX community")
def community_command():
    pass


@click.group("members", help="Display information about Open edX community members")
def members_command():
    pass


@click.command("list", help="List active community members")
@click.option("-t", "--tag", help="Limit to users with this tag")
@click.pass_obj
def members_list(context, tag):
    endpoint = "/community/members"
    if tag:
        endpoint += "?" + urlencode({"tag": tag})
    for member in make_request(context.oxct_host, endpoint)["members"]:
        print(single_line_format_member(member))


@click.command("show", help="Show profile of a community member")
@click.argument("username")
@click.pass_obj
def members_show(context, username):
    member = make_request(context.oxct_host, f"/community/members/{username}")
    print(single_line_format_member(member))
    print(member["bio"]["txt"])


@click.group("tags", help="Display community tags")
@click.pass_obj
def tags_command(context):
    for tag in make_request(context.oxct_host, "/community/tags")["tags"]:
        print(tag)


@click.command("list", help="Display community tags")
def tags_list():
    pass


def make_request(host, endpoint):
    # TODO we should probably catch http and deserializatrion errors here
    response = urlopen(f"{host}{endpoint}")
    return json.loads(response.read())


def single_line_format_member(member):
    return f"@{member['username']} {member['name']} ❤️  x {member['likes_received']}"


members_command.add_command(members_list)
members_command.add_command(members_show)
tags_command.add_command(tags_list)
community_command.add_command(members_command)
community_command.add_command(tags_command)
cli.add_command(community_command)


if __name__ == "__main__":
    main()
