import click
import requests



baseProto = "http://"
baseurl = "192.168.7.4:5000"
baseRequest = baseProto + baseurl
def callContainer(url, container, form):
  r = requests.post(url + "/" + container + "/cli", form)
  if r.status_code == 200:
    return r.text
  else:
    return form
@click.group()
def cli():
  pass


@cli.command()
@click.option('--ip', default='', help="IP that you want to query")
def ipinfo(ip):
  form ={}
  form['ip'] = ip
  click.echo(callContainer(baseRequest, "ipinfo", form))


@cli.command()
@click.option('--domain', required=True, help='domain you are looking up')
def pywhois(domain):
  form = {}
  form['domain'] = domain
  click.echo(callContainer(baseRequest, "pywhois", form))

@cli.command()
@click.option('--port', required=True, help="Port you want more information about")
@click.option('--proto', default='', help="Protocol deliniating by protocol if one such exists")
def whatis(port, proto):
  form = {}
  form['port'] = port
  form['proto'] = proto
  click.echo(callContainer(baseRequest, "whatis", form))

@cli.command()
@click.option("--name", required=True, help="Name of the event being created")
@click.option("--description", default="", help="Description of the event")
@click.option("--analystcomments", default="", help="Analysts Comments about the event")
def event(name, description, analystcomments):
  form={}
  form['name'] = name
  form['description'] = description
  form['AnalystComments'] = analystcomments
  click.echo(callContainer(baseRequest, "event",form))








