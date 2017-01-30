import click
import requests
import whois

@click.group()
def cli():
  pass


@cli.command()
@click.option('--ip', default='', help="IP that you want to query")
def ipinfo(ip):
  r = requests.get(f"http://ipinfo.io/{ip}")
  if r.status_code ==200:
    click.echo(r.text)
  else:
    click.echo(f"Issue happend:\n{r.raise_for_status}")


@cli.command()
@click.option('--domain', required=True, help='domain you are looking up')
def who(domain):
  w = whois.whois(domain)
  click.echo(w)