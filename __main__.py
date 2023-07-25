import argparse
import subprocess
import sys

from getpass import getpass
from hashlib import sha256


def main(**args):
	if not args["value"]:
		if args["hide"] is True:
			args["value"] = getpass("")
		else:
			args["value"] = input()

	size = args.setdefault("size", 64)

	result = sha256(args["value"].encode()).hexdigest()[:size]

	if args["clip"]:
		try:
			subprocess.run(
				["xclip", "-selection", "clipboard"],
				input=result.encode(),
				check=True
			)
		except FileNotFoundError:
			print("Error: xclip not found")
			sys.exit()

	else:
		print(result)


if __name__ == "__main__":
	p = argparse.ArgumentParser()
	p.add_argument("-v", "--value", type=str, help="Value to be transformed")
	p.add_argument("-s", "--size", type=int, help="Size of the final output")
	p.add_argument(
		"--hide",
		action="store_true",
		help="Hide the text value when typing"
	)
	p.add_argument(
		"-c",
		"--clip",
		action="store_true",
		help="Copy the output to clipboard"
	)
	args = p.parse_args()

	main(**vars(args))
