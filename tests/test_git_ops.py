from git_ops import GitOps


def test_dry_run():

    git = GitOps(dry_run=True)

    result = git.status()

    assert result["success"] is True
    assert result["dry_run"] is True
    assert result["command"] == "git status --porcelain=v2"


def test_parse_untracked_file():

    git = GitOps()

    output = """
? .gitignore
"""

    result = git.parse_porcelain(output)

    assert result["untracked"] == [".gitignore"]
    assert result["modified"] == []
    assert result["staged"] == []