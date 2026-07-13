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

    def clean_preview(self):
        """
        Returns the list of files that git clean would remove.
        Uses git clean dry-run mode (-n).
        """

        proc = subprocess.run(
            ["git", "clean", "-fdn"],
            capture_output=True,
            text=True
        )

        if proc.returncode != 0:
            return {
                "success": False,
                "stderr": proc.stderr
            }

        files = []

        for line in proc.stdout.splitlines():
            if line.startswith("Would remove "):
                files.append(
                    line.replace("Would remove ", "")
                )

        return {
            "success": True,
            "files": files
        }

    def clean(self, force=False):

        # First determine what would be deleted
        preview = self.clean_preview()

        if not preview["success"]:
            return preview

        files = preview["files"]

        # Nothing to clean
        if not files:
            return {
                "success": True,
                "message": "No untracked files to remove"
            }

        # Show impact before destructive operation
        if not force:

            print("The following files will be deleted:")

            for file in files:
                print(f"  {file}")

            confirmed = ask_confirmation(
                "Continue?"
            )

            if not confirmed:
                return {
                    "success": False,
                    "cancelled": True,
                    "files": files
                }

        return self.run(["git", "clean", "-fd"])