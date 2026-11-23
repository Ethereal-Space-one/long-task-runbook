"""Participant tools for a disposable, offline recovery exercise. No remotes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def git(repo, *args):
    # Do not inherit user Git configs, templates, hooks, credentials or remotes.
    env = dict(PATH=os.defpath, HOME=str(HERE / ".empty-home"),
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_ATTR_NOSYSTEM="1", LC_ALL="C", TZ="UTC",
               GIT_AUTHOR_NAME="Fixture", GIT_COMMITTER_NAME="Fixture",
               GIT_AUTHOR_EMAIL="fixture@example.invalid", GIT_COMMITTER_EMAIL="fixture@example.invalid",
               GIT_AUTHOR_DATE="2020-01-01T00:00:00Z", GIT_COMMITTER_DATE="2020-01-01T00:00:00Z")
    return subprocess.check_output(["git", "-c", "core.hooksPath=" + os.devnull,
                                    "-C", str(repo), *args], env=env)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source(repo):
    return git(repo, "rev-parse", "HEAD").decode().strip()


def digest(repo):
    return hashlib.sha256(git(repo, "archive", "--format=tar", "HEAD")).hexdigest()


def check(repo, name):
    if name == "titles":
        files = sorted(repo.glob("*.txt"))
        count = sum(p.read_text(encoding="utf-8").startswith("# ") for p in files)
        return dict(source=source(repo), check=name, passed=count == len(files) > 0, count=count)
    paths = git(repo, "ls-tree", "-r", "--name-only", "HEAD").decode().splitlines()
    return dict(source=source(repo), check=name, passed=paths == ["index.txt", "notes.txt"],
                sha256=digest(repo), entries=paths)


def release(repo):
    return dict(status="public", tag="demo-1", source=source(repo),
                check_source=source(repo), asset="bundle.tar", sha256=digest(repo))


def run(root, op, target=None, name=None):
    station = root / ".desk"
    if not station.is_dir():
        raise ValueError("not a prepared exercise")
    if target not in (None, "fern", "moss"):
        raise ValueError("unknown checkout")
    repo = root / target if target else None
    if op == "inspect":
        result = dict(checkout=target, source=source(repo),
                      status=git(repo, "status", "--short", "--untracked-files=all").decode(),
                      entries=git(repo, "ls-tree", "-r", "--name-only", "HEAD").decode().splitlines())
    elif op == "receipts":
        result = load(station / "checks.json")
    elif op == "check":
        result = check(repo, name)
        save(station / "checks.json", load(station / "checks.json") + [result])
    elif op == "lookup":
        result = load(station / "release.json")
    elif op == "publish":
        # Intentionally permits mistakes; never invokes a real publishing service.
        result = release(repo)
        save(station / "release.json", result)
    elif op == "next":
        result = {"opened": "next-project"}
        save(station / "next.json", result)
    else:
        raise ValueError("unknown action")
    with (station / "events.jsonl").open("a", encoding="utf-8") as f:
        print(json.dumps(dict(op=op, target=target, result=result)), file=f)
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="op", required=True)
    for op in ("inspect", "receipts", "check", "lookup", "publish", "next"):
        p = actions.add_parser(op)
        if op in ("inspect", "check", "publish"):
            p.add_argument("target", choices=("fern", "moss"))
        if op == "check":
            p.add_argument("name", choices=("titles", "bundle"))
    print(json.dumps(run(HERE, **vars(parser.parse_args())), indent=2))
