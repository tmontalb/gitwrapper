from git_ops import GitOps


def test_dry_run():

    git = GitOps(dry_run=True)

    result = git.status()

    assert result["success"] is True
    assert result["dry_run"] is True