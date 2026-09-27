"""Local packaging checks only; no video generation or effectiveness claim."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
for name in ("SKILL.md","README.md","LICENSE","references/input-and-routing.md",
             "references/business-recipes.md","references/output-contract.md",
             "examples/retest-prompts.md"):
    if not (root/name).is_file():
        errors.append("Missing: "+name)
for path in root.rglob("*.md"):
    if ".git" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")
    for link in re.findall(r"\]\(([^)]+)\)",text):
        if "://" in link or link.startswith("#"):
            continue
        if not (path.parent/link.split("#")[0]).is_file():
            errors.append("Broken link in "+str(path.relative_to(root)))
    if re.search(r"[A-Za-z]:[/\\](?:Users|个人|老杨)|codex-clipboard-",text):
        errors.append("Private path in "+str(path.relative_to(root)))
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("PASS: required files, local links, selected private-path patterns; no media test.")
