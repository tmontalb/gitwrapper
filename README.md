# gitwrap

`gitwrap` is a safer command-line wrapper around common Git operations.
The goal is to provide guardrails around potentially destructive commands, support dry-run workflows, and produce consistent machine-readable output suitable for automation.

## Motivation

Git is a powerful tool, but some commands can have irreversible consequences when used incorrectly.

For example:

```bash
git clean -fd
```

can permanently remove untracked files and directories.

`gitwrap` provides a safer interface by:

* Requiring explicit confirmation before destructive operations
* Supporting a dry-run mode to preview changes
* Returning consistent YAML output for scripting and automation
* Providing a foundation that can be extended to other infrastructure tools

## Features

Current supported commands:

### Git status

```bash
python gitwrap.py status
```

Example output:

```yaml
success: true
stdout: |
  On branch main
  nothing to commit
stderr: ""
```

---

### Safe git clean

```bash
python gitwrap.py clean
```

Before executing:

```text
This will permanently delete ALL untracked files. Continue? [y/N]:
```

The command requires explicit confirmation.

---

### Dry-run mode

Any command can be executed in dry-run mode:

```bash
python gitwrap.py --dry-run clean
```

Example output:

```yaml
success: true
dry_run: true
command: git clean -fd
```

The command is displayed but not executed.

---

# Installation

## Requirements

* Python 3.9+
* Git

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Display available commands:

```bash
python gitwrap.py --help
```

Examples:

```bash
python gitwrap.py status

python gitwrap.py clean

python gitwrap.py --dry-run clean
```

---

# Project Structure

```
gitwrap/
├── gitwrap.py              # CLI entry point
├── git_ops.py              # Git command execution and safety logic
├── confirmation.py         # User confirmation handling
├── output.py               # YAML output formatting
├── requirements.txt
└── tests/
    └── test_git_ops.py
```

---

# Design Decisions

## Separation of concerns

The implementation separates:

* CLI argument parsing
* Git operation logic
* Confirmation workflows
* Output formatting

This allows Git operations to be tested independently and makes it easier to add additional commands.

---

## Safety first

Commands are categorized based on risk.

Read-only commands such as:

```bash
git status
```

can execute immediately.

Potentially destructive commands such as:

```bash
git clean
```

require explicit user confirmation unless the user intentionally bypasses the protection with:

```bash
--force
```

---

## Machine-readable output

All commands return structured YAML output instead of human-oriented text.

This makes the tool easier to integrate into:

* CI/CD pipelines
* automation workflows
* monitoring systems
* higher-level orchestration tools

---

# Testing Strategy

The main testing goals are:

* Validate command behavior
* Ensure destructive operations require confirmation
* Verify dry-run behavior
* Test failure scenarios

Example:

```bash
pytest
```

Future improvements:

* Mock subprocess execution instead of invoking Git directly
* Add integration tests using temporary Git repositories
* Validate YAML schemas

---

# Handling Edge Cases

Examples considered:

## Not running inside a Git repository

Expected behavior:

```yaml
success: false
error: Not a git repository
```

---

## User cancels a destructive operation

Expected behavior:

```yaml
success: false
cancelled: true
```

---

## Git command failure

The wrapper returns:

* exit status
* stdout
* stderr

allowing automation systems to handle failures consistently.

---

# Future Extensions

The same wrapper pattern could be extended beyond Git.

Examples:

## Kubernetes

Instead of:

```bash
kubectl delete namespace production
```

provide:

```bash
kube-wrap delete namespace production
```

with:

* impact analysis
* dependency checks
* confirmation
* dry-run support

---

## AWS CLI

Instead of:

```bash
aws ec2 terminate-instances
```

provide:

* resource validation
* dependency detection
* approval workflows
* audit logging

---

## Docker

Potential safeguards:

* prevent deleting running containers
* display image/container dependencies
* require confirmation for destructive actions

---

# Summary

`gitwrap` demonstrates a pattern for building safer operational tooling:

1. Provide a simple interface
2. Add safety guardrails
3. Make automation-friendly output a default
4. Design components for extension

The goal is not to replace Git, but to make common operational workflows safer and more reliable.
