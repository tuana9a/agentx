import argparse
import importlib

parser = argparse.ArgumentParser(prog="agentx-tools")

parser.add_argument("which",
                    help="Which module",
                    choices=["install", "gen"],
                    type=str)

parser.add_argument("remains",
                    type=str,
                    nargs=argparse.REMAINDER,
                    help="Child opts")


def main():
    args = parser.parse_args()
    m = importlib.import_module(f"agentx.cmd.{args.which}")
    m.run(args)