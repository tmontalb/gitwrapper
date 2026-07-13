#!/usr/bin/env python3

import argparse
from git_ops import GitOps
from output import print_yaml

parser = argparse.ArgumentParser(description="Safe Git Wrapper")

parser.add_argument("--dry-run", action="store_true")

sub = parser.add_subparsers(dest="command")

sub.add_parser("status")

clean = sub.add_parser("clean")
clean.add_argument("--force", action="store_true")

args = parser.parse_args()

git = GitOps(args.dry_run)

if args.command == "status":
    result = git.status()

elif args.command == "clean":
    result = git.clean(force=args.force)

else:
    parser.print_help()
    exit(1)

print_yaml(result)