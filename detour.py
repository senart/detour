import os
import re
import click
from functools import reduce

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def add_color(text, color):
	return color + text + bcolors.ENDC

class Host:
	def __init__(self, url, port, alias_ip):
		self.url = url
		self.port = port
		self.alias_ip = alias_ip


def read_input(input_file):
	hosts = []

	with open(input_file, 'r') as file:
		for index, line in enumerate(file, start=1):
			url = line.split(':')[0].strip()
			port = line.split(':')[1].strip()

			alias_ip = f'127.0.99.{index}'
			hosts.append(Host(url, port, alias_ip))

	return hosts


def ssh_start_command(server, hosts):
	return f'ssh -i ~/.ssh/id_rsa -M -S ssh-control-socket -fnNT {server} ' + ' '.join([f'-L {host.alias_ip}:{host.port}:{host.url}:{host.port}' for host in hosts])


def ssh_stop_command(server):
	return f'ssh -S ssh-control-socket -O exit {server}'


def add_alias_command(hosts):
	return ' && '.join([f'ifconfig lo0 alias {host.alias_ip} 255.255.255.0' for host in hosts])


def delete_alias_command(hosts):
	return ' && '.join([f'ifconfig lo0 delete {host.alias_ip}' for host in hosts])


def execute_command(command):
	click.echo(f'+ {command}')
	os.system(command)


def append_hosts_file(hosts_file, hosts):
	with open(hosts_file, 'a') as file:
		for host in hosts:
			file.write(f'{host.alias_ip}	{host.url}\n')
			click.echo(add_color(f'{host.alias_ip}	{host.url}', bcolors.OKGREEN))


def clean_hosts_file(hosts_file, hosts):
	with open(hosts_file, 'r') as f:
		lines = f.readlines()
	with open(hosts_file, 'w') as f:
		deleted_lines = []
		for line in lines:
			should_write_line = True
			for host in hosts:
				escaped_ip = re.escape(host.alias_ip)
				escaped_url = re.escape(host.url)
				should_write_line = should_write_line and not re.search(
					f'^{escaped_ip}[ \t]*{escaped_url}$', line.strip("\n"))
			if should_write_line:
				f.write(line)
			else:
				deleted_lines.append(line)
		click.echo(add_color(''.join(deleted_lines), bcolors.FAIL))


@click.group()
@click.version_option()
def cli():
	"""Detour.

	This script create an SSH tunnel with specified entries.
	It updates your /etc/hosts file, so that connections to the
	specified entries are possible.
	"""


@cli.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('-s', '--server', help='A server to use for SSH tunneling', required=True)
@click.option('--host-file', 'hosts_file', default='/etc/hosts', show_default=True)
def start(input, server, hosts_file):
	click.echo("Starting script...")

	hosts = read_input(input)

	execute_command(add_alias_command(hosts))
	execute_command(ssh_start_command(server, hosts))
	append_hosts_file(hosts_file, hosts)


@cli.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('-s', '--server', help='A server to use for SSH tunneling', required=True)
@click.option('--host-file', 'hosts_file', default='/etc/hosts', show_default=True)
def stop(input, server, hosts_file):
	click.echo("Stopping script...")

	hosts = read_input(input)

	execute_command(ssh_stop_command(server))
	clean_hosts_file(hosts_file, hosts)
	execute_command(delete_alias_command(hosts))


def main():
	cli()


if __name__ == '__main__':
	main()
