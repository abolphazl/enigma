from rich.prompt import Prompt
from rich.panel import Panel
from enigma import Enigma
from rich import print
import typer
import os


# without any option
def main(read: str = '', write: str = ''):
	
	if read == '':
		message = Prompt.ask("Enter your name")
		print(Panel("[bold green]" + Enigma(message) + "[/bold green]"))
	else:
		try:
			f = open(read)
		except:
			print("file not exists!")
			return
		try:
			if write == '':
				print(Panel("[bold green]" + Enigma(f.read()) + "[/bold green]"))
			else:
				output = open(write, 'w')
				output.write(Enigma(f.read()))
		except:
			print("i can't write file!")


if __name__ == "__main__":
	typer.run(main)