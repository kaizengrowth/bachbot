import click

from scrape_humdrum import scrape_humdrum

@click.group()
def cli():
    pass

@click.command()
def extract_melody():
    click.echo("hi")

cli.add_command(scrape_humdrum)
cli.add_command(extract_melody)