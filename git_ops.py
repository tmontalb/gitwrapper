import subprocess

from confirmation import ask_confirmation


class GitOps:

    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    def run(self, command):

        if self.dry_run:
            return {
                "success": True,
                "dry_run": True,
                "command": " ".join(command)
            }

        proc = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr
        }

    def status(self):
        return self.run(["git", "status"])

    def clean(self, force=False):

        if not force:

            confirmed = ask_confirmation(
                "This will permanently delete ALL untracked files. Continue?"
            )

            if not confirmed:
                return {
                    "success": False,
                    "cancelled": True
                }

        return self.run(["git", "clean", "-fd"])