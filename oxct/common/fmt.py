import click


def echo_error(text):
    return click.echo(click.style(text, fg="red"))
