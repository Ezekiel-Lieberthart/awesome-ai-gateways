#!/usr/bin/env python3
"""Checks entries in README.md against the rules in contributing.md.

Usage:
  review.py check [README.md] [--network]     Check a local file (static checks, optionally links).
  review.py pr --pr NUMBER [--lint] [--post]  Review a pull request and optionally post the result.
  review.py full [--issue]                    Check every entry on main, optionally update the report issue.

Uses only the Python standard library. Reads GITHUB_TOKEN (or GH_TOKEN) for GitHub API calls and
GITHUB_REPOSITORY for the repository (defaults to ai-gateways/awesome-ai-gateways).
"""

import argparse
import concurrent.futures
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

REPO = os.environ.get("GITHUB_REPOSITORY", "ai-gateways/awesome-ai-gateways")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
UA = "Mozilla/5.0 (compatible; awesome-ai-gateways-review/1.0; +https://github.com/ai-gateways/awesome-ai-gateways)"
COMMENT_MARKER = "<!-- awesome-ai-gateways-review -->"
ISSUE_MARKER = "<!-- awesome-ai-gateways-maintenance -->"

SOFTWARE_SECTIONS = {
    "AI Gateways",
    "MCP Gateways",
    "Agent Gateways",
    "API Gateways with AI Features",
    "Cloud and Platform AI Gateways",
    "Model Routers and Aggregators",
    "Inference Gateways",
}
# Sections whose main links must point to an exact section of the page.
DEEP_LINK_SECTIONS = {"Specifications and Standards", "Guides", "Articles"}
RESOURCE_SECTIONS = DEEP_LINK_SECTIONS | {"Related Lists"}
SKIP_SECTIONS = {"Contents", "Contributing"}

MAX_DESCRIPTION = 280  # visible characters, excluding the license and language tags
MIN_STARS = 200
MAX_STALE_DAYS = 183

KNOWN_LICENSES = {
    "0BSD", "AGPL-3.0", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "BSL-1.0", "BUSL-1.1",
    "CC0-1.0", "Elastic-2.0", "EPL-2.0", "GPL-2.0", "GPL-3.0", "ISC", "LGPL-2.1", "LGPL-3.0",
    "MIT", "MIT-0", "MPL-2.0", "SSPL-1.0", "Unlicense", "Zlib",
}
MARKETING_WORDS = [
    "best", "fastest", "leading", "industry-leading", "world's", "world-class", "powerful",
    "blazing", "blazingly", "revolutionary", "next-gen", "next-generation", "state-of-the-art",
    "cutting-edge", "game-changer", "game-changing", "seamless", "seamlessly", "robust",
    "leverage", "leverages", "unlock", "unlocks", "supercharge", "supercharges", "effortless",
    "effortlessly", "ultimate", "unparalleled", "unmatched", "incredible", "amazing", "awesome",
    "#1", "10x", "magical",
]
MARKETING_RE = re.compile(r"(?<![\w#-])(" + "|".join(re.escape(w) for w in MARKETING_WORDS) + r")(?![\w-])", re.I)
ENTRY_RE = re.compile(r"^- \[(?P<name>[^\]]+)\]\((?P<url>[^)\s]+)\) - (?P<desc>.+)$")
TAGS_RE = re.compile(r" \((?P<tags>`[^`]+`(?:, `[^`]+`)*)\)\.$")
INLINE_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


# ---------------------------------------------------------------- parsing

class Entry:
    def __init__(self, section, line_no, raw, name, url, desc):
        self.section, self.line_no, self.raw = section, line_no, raw
        self.name, self.url, self.desc = name, url, desc
        m = TAGS_RE.search(desc)
        self.tags = [t.strip("`") for t in m.group("tags").split(", ")] if m else []
        self.text = desc[: m.start()] + "." if m else desc
        self.visible = INLINE_LINK_RE.sub(r"\1", self.text)
        self.inline_links = [u for _, u in INLINE_LINK_RE.findall(self.text)]

    @property
    def license(self):
        return self.tags[0] if self.tags else None

    @property
    def language(self):
        return self.tags[1] if len(self.tags) > 1 else None


def parse(text):
    """Returns (entries, problems). Problems are list items in content sections that do not parse."""
    entries, problems, section = [], [], None
    for no, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if line.startswith("#") or section is None or section in SKIP_SECTIONS:
            continue
        if line.startswith("- "):
            m = ENTRY_RE.match(line)
            if m:
                entries.append(Entry(section, no, line, m["name"], m["url"], m["desc"]))
            else:
                problems.append((section, no, line))
    return entries, problems


def url_key(url):
    p = urllib.parse.urlsplit(url)
    host = p.netloc.lower().removeprefix("www.")
    return host + p.path.rstrip("/").lower()


# ---------------------------------------------------------------- static checks

def static_findings(entry):
    """Returns a list of (level, message) for one entry. Levels: error, warning."""
    out = []
    if "—" in entry.raw or "–" in entry.raw:
        out.append(("error", "Uses an em dash or en dash. Use commas or rephrase; the only dash allowed is the separator."))
    first = entry.desc.split(" ", 1)[0]
    if not re.search(r"[A-Z0-9]", first) and not first.startswith(("`", '"', "(")):
        out.append(("error", "Description must start with an uppercase letter."))
    if not entry.desc.endswith("."):
        out.append(("error", "Description must end with a period."))
    if entry.desc.lower().startswith(entry.name.lower()):
        out.append(("error", "Description should not repeat the name. Start with what the software is or does."))
    if re.search(r"[.!?] [A-Z]", entry.visible[:-1]):
        out.append(("warning", "Looks like more than one sentence. Entries are a single sentence."))
    words = sorted({m.group(1).lower() for m in MARKETING_RE.finditer(entry.visible)})
    if words:
        out.append(("error", "Marketing language: " + ", ".join(f"`{w}`" for w in words) + ". Describe what it does instead."))
    if len(entry.visible) > MAX_DESCRIPTION:
        out.append(("warning", f"Description is {len(entry.visible)} characters; keep it under {MAX_DESCRIPTION} by naming the main capabilities only."))
    if entry.section not in SOFTWARE_SECTIONS | RESOURCE_SECTIONS:
        out.append(("warning", f"Section `{entry.section}` is not known to the checker; add it to .github/scripts/review.py."))
    if entry.section in SOFTWARE_SECTIONS:
        if not entry.tags:
            out.append(("error", "Missing tags. End with (`License`, `Language`). for open source or (`Proprietary`). for commercial products."))
        elif entry.license == "Proprietary":
            if len(entry.tags) > 1:
                out.append(("error", "Proprietary entries take a single tag: (`Proprietary`)."))
        else:
            if base_license(entry.license) not in {base_license(l) for l in KNOWN_LICENSES}:
                out.append(("warning", f"`{entry.license}` is not a common SPDX identifier. Use the identifier GitHub shows for the repository."))
            if len(entry.tags) != 2:
                out.append(("error", "Open source entries take two tags: (`License`, `Language`)."))
    elif entry.tags and entry.section in RESOURCE_SECTIONS:
        out.append(("warning", "License and language tags are only used in software sections."))
    if entry.section in DEEP_LINK_SECTIONS and "#" not in entry.url:
        out.append(("error", "Links in this section must point to the exact section of the page, using a heading anchor or a `#:~:text=` fragment."))
    for u in entry.inline_links:
        if u.startswith("http") and "#" not in u:
            out.append(("error", f"Link in the description must point to an exact section: <{u}>"))
    return out


def order_findings(entries):
    """Returns {line_no: message} for entries that break alphabetical order in their section."""
    out, by_section = {}, {}
    for e in entries:
        by_section.setdefault(e.section, []).append(e)
    for items in by_section.values():
        names = [e.name.lower() for e in items]
        expected = sorted(names)
        if names == expected:
            continue
        for e in items:
            others = sorted(n for n in names if n != e.name.lower())
            pos = sum(1 for n in others if n < e.name.lower())
            # An entry is out of place if removing it leaves the rest sorted and it does not fit where it is.
            rest = [n for n in names if n != e.name.lower()]
            if rest == sorted(rest):
                after = others[pos - 1] if pos > 0 else None
                hint = f"after `{display(items, after)}`" if after else "at the top of the section"
                out[e.line_no] = f"Out of alphabetical order; move it {hint}."
        if not any(e.line_no in out for e in items):
            for e in items:
                out[e.line_no] = "Section is not in alphabetical order (ignoring case)."
    return out


def display(items, lowered):
    return next((e.name for e in items if e.name.lower() == lowered), lowered)


def duplicate_findings(entries):
    out, seen_url, seen_name = {}, {}, {}
    for e in entries:
        keys = [(url_key(e.url), seen_url, "link")]
        if e.section in SOFTWARE_SECTIONS:  # a guide may share a product's name
            keys.append((e.name.lower(), seen_name, "name"))
        for key, seen, what in keys:
            if key in seen:
                first = seen[key]
                out.setdefault(e.line_no, []).append(f"Same {what} as `{first.name}` in {first.section}. Each product appears once.")
            else:
                seen[key] = e
    return out


def base_license(spdx):
    return re.sub(r"-(only|or-later)$", "", spdx or "").lower()


# ---------------------------------------------------------------- network checks

def http_get(url, timeout=30, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.geturl(), r.read().decode("utf-8", "ignore")


def gh_api(path, method="GET", data=None, accept="application/vnd.github+json", auth=True):
    url = path if path.startswith("http") else f"https://api.github.com/{path.lstrip('/')}"
    headers = {"User-Agent": UA, "Accept": accept, "X-GitHub-Api-Version": "2022-11-28"}
    if TOKEN and auth:
        headers["Authorization"] = f"Bearer {TOKEN}"
    body = json.dumps(data).encode() if data is not None else None
    if body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode("utf-8", "ignore")
        if accept.endswith("raw"):
            return raw
        return json.loads(raw) if raw else None


def page_text(body):
    body = re.sub(r"(?s)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).strip().lower()


def fragment_found(body, fragment):
    if fragment.startswith(":~:text="):
        phrase = urllib.parse.unquote(fragment[len(":~:text="):])
        parts = [p for p in phrase.split(",") if not p.endswith("-") and not p.startswith("-")]
        phrase = re.sub(r"\s+", " ", (parts[0] if parts else phrase)).strip().lower()
        return phrase in page_text(body)
    frag = re.escape(urllib.parse.unquote(fragment))
    return re.search(r"""\b(?:id|name)=["']?(?:user-content-)?""" + frag + r"""["'\s>]""", body.replace("&amp;", "&")) is not None


_page_cache = {}


def check_link(url):
    """Returns a list of (level, message)."""
    base, _, fragment = url.partition("#")
    if base not in _page_cache:
        result = None
        for attempt in range(2):
            try:
                result = http_get(base)
                break
            except urllib.error.HTTPError as e:
                result = ("http", e.code)
                if e.code in (404, 410):
                    break
            except Exception as e:  # DNS, TLS, timeout
                result = ("err", str(e)[:80])
        _page_cache[base] = result
    result = _page_cache[base]
    if result[0] == "http":
        code = result[1]
        if code in (404, 410):
            return [("error", f"Link returns HTTP {code}: <{base}>")]
        return [("warning", f"Could not verify the link (HTTP {code}, often bot protection): <{base}>")]
    if result[0] == "err":
        return [("warning", f"Could not reach <{base}> ({result[1]}).")]
    status, final, body = result
    out = []
    if urllib.parse.urlsplit(final).netloc.lower().removeprefix("www.") != urllib.parse.urlsplit(base).netloc.lower().removeprefix("www."):
        out.append(("warning", f"<{base}> redirects to another site: <{final}>. Link the final page."))
    if fragment and not fragment_found(body, fragment):
        out.append(("error", f"Section `#{fragment[:60]}` was not found on <{base}>. Use a heading anchor that exists in the page HTML or a `#:~:text=` fragment."))
    return out


def github_repo(url):
    m = re.match(r"https://github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?/?(?:#.*)?$", url)
    return (m.group(1), m.group(2)) if m and m.group(1) not in {"orgs", "topics", "sponsors"} else None


def check_github(entry):
    owner, repo = github_repo(entry.url)
    out = []
    try:
        d = gh_api(f"repos/{owner}/{repo}")
    except urllib.error.HTTPError as e:
        return [("error", f"GitHub repository `{owner}/{repo}` not found (HTTP {e.code}).")]
    if d["full_name"].lower() != f"{owner}/{repo}".lower():
        out.append(("warning", f"Repository moved to `{d['full_name']}`; link the new URL."))
    if d.get("archived"):
        out.append(("error", "Repository is archived."))
    last, problem = None, ""
    branch = urllib.parse.quote(d["default_branch"], safe="")
    # Some organizations block other installations' tokens; public data is also readable anonymously.
    for auth in (True, True, False):
        try:
            last = gh_api(f"repos/{d['full_name']}/branches/{branch}", auth=auth)["commit"]["commit"]["committer"]["date"]
            break
        except urllib.error.HTTPError as e:
            problem = f" (HTTP {e.code})"
        except Exception as e:
            problem = f" ({str(e)[:60]})"
    if last:
        age = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(last.replace("Z", "+00:00"))).days
        if age > MAX_STALE_DAYS:
            out.append(("error", f"No commit on the default branch in {age} days (limit: six months)."))
    else:
        out.append(("warning", f"Could not read the latest commit on the default branch{problem}."))
    stars = d.get("stargazers_count", 0)
    if stars < MIN_STARS:
        out.append(("warning", f"{stars} stars, below the {MIN_STARS}-star guideline. Maintainers accept this only for projects run by an established company or foundation."))
    if entry.section in SOFTWARE_SECTIONS and entry.license and entry.license != "Proprietary":
        gh_license = (d.get("license") or {}).get("spdx_id")
        if not gh_license or gh_license == "NOASSERTION":
            out.append(("warning", f"GitHub does not detect a license; a maintainer needs to confirm `{entry.license}`."))
        elif base_license(gh_license) != base_license(entry.license):
            out.append(("error", f"License tag `{entry.license}` does not match `{gh_license}` reported by GitHub."))
        elif gh_license != entry.license:
            out.append(("warning", f"Use `{gh_license}`, the identifier GitHub reports, for consistency."))
        if entry.language and d.get("language") and d["language"] != entry.language:
            out.append(("warning", f"Language tag `{entry.language}` differs from GitHub's `{d['language']}`; keep it only if it is the main implementation language."))
    return out


def network_findings(entries):
    """Returns {line_no: [(level, message)]} for link and repository checks."""
    jobs = {}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for e in entries:
            urls = [e.url] + [u for u in e.inline_links if u.startswith("http")]
            jobs[e.line_no] = [pool.submit(check_link, u) for u in urls]
            if github_repo(e.url) and e.section in SOFTWARE_SECTIONS:
                jobs[e.line_no].append(pool.submit(check_github, e))
        return {no: [f for fut in futs for f in fut.result()] for no, futs in jobs.items()}


# ---------------------------------------------------------------- awesome-lint

IGNORED_LINT_RULES = ("awesome-git-repo-age", "awesome-github")


def run_awesome_lint(readme_text, lint_cmd):
    """Runs awesome-lint on the text in a scratch git repo. Returns (ok, findings)."""
    tmp = tempfile.mkdtemp()
    try:
        with open(os.path.join(tmp, "readme.md"), "w") as f:
            f.write(readme_text)
        # awesome-lint expects a contributing.md next to the readme.
        with open(os.path.join(tmp, "contributing.md"), "w") as f:
            f.write("# Contribution Guidelines\n")
        subprocess.run(["git", "init", "-q"], cwd=tmp, check=True)
        subprocess.run(["git", "remote", "add", "origin", f"https://github.com/{REPO}.git"], cwd=tmp, check=True)
        p = subprocess.run(lint_cmd + ["readme.md"], cwd=tmp, capture_output=True, text=True, timeout=300)
        text = re.sub(r"\x1b\[[0-9;]*m", "", p.stdout + p.stderr)
        lines = [l.strip() for l in text.splitlines() if re.match(r"\s*[✖⚠]\s+\d+:\d+", l)]
        lines = [l for l in lines if not l.endswith(IGNORED_LINT_RULES)]
        return not any(l.startswith("✖") for l in lines), lines
    except Exception as e:
        return True, [f"⚠ awesome-lint did not run: {e}"]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- reports

ICON = {"error": "❌", "warning": "⚠️"}


def esc(text):
    text = re.sub(r"([\\`*_\[\]<>|])", r"\\\1", text)
    return text.replace("@", "@​")


def entry_block(entry, findings):
    lines = [f"**{esc(entry.name)}** in {entry.section} (line {entry.line_no})", ""]
    if findings:
        lines += [f"- {ICON[level]} {msg}" for level, msg in findings]
    else:
        lines.append("- ✅ No problems found.")
    return "\n".join(lines)


def collect(entries, all_entries, text_problems, network):
    order = order_findings(all_entries)
    dups = duplicate_findings(all_entries)
    net = network_findings(entries) if network else {}
    results = []
    for e in entries:
        f = static_findings(e)
        if e.line_no in order:
            f.append(("error", order[e.line_no]))
        f += [("error", m) for m in dups.get(e.line_no, [])]
        f += net.get(e.line_no, [])
        results.append((e, f))
    for section, no, line in text_problems:
        stub = Entry(section, no, line, line[:40], "", "")
        results.append((stub, [("error", "List item does not match `- [Name](link) - Description.`")]))
    return results


def count(results, extra=()):
    levels = [level for _, f in results for level, _ in f] + [level for level, _ in extra]
    return levels.count("error"), levels.count("warning")


# ---------------------------------------------------------------- commands

def cmd_check(args):
    text = open(args.readme).read()
    entries, problems = parse(text)
    results = collect(entries, entries, problems, args.network)
    for e, f in results:
        for level, msg in f:
            print(f"{args.readme}:{e.line_no}: {level}: [{e.name}] {msg}")
    errors, warnings = count(results)
    print(f"{len(entries)} entries, {errors} errors, {warnings} warnings")
    return 1 if errors else 0


def fetch_pr(number):
    pr = gh_api(f"repos/{REPO}/pulls/{number}")
    files = gh_api(f"repos/{REPO}/pulls/{number}/files?per_page=100")
    readme_changed = any(f["filename"] == "README.md" for f in files)
    # Pull request commits are readable from the base repository, even if the fork is gone.
    head = gh_api(f"repos/{REPO}/contents/README.md?ref={pr['head']['sha']}", accept="application/vnd.github.raw") if readme_changed else None
    base = gh_api(f"repos/{REPO}/contents/README.md?ref={pr['base']['sha']}", accept="application/vnd.github.raw")
    return pr, files, base, head


def pr_level_findings(pr, files, added, removed):
    out = []
    other = sorted(f["filename"] for f in files if f["filename"] != "README.md")
    if other:
        out.append(("warning", "Changes files other than README.md: " + ", ".join(f"`{esc(o)}`" for o in other) + ". A maintainer will check these by hand."))
    if len(added) > 1:
        out.append(("warning", f"Adds {len(added)} entries. Open one pull request per product so each can be reviewed on its own."))
    if not re.match(r"^(Add|Update|Remove|Move|Fix|Rename) \S", pr.get("title") or ""):
        out.append(("warning", "Use a title such as `Add Name`, `Update Name`, or `Remove Name`."))
    body = (pr.get("body") or "").lower()
    if added and not re.search(r"affiliation|i work (on|at|for)|i am the (author|maintainer|founder)|i maintain|i built|not affiliated|no affiliation|no connection", body):
        out.append(("warning", "Say how you are connected to the product (for example `I work on it` or `No affiliation`)."))
    for e in removed:
        out.append(("warning", f"Removes `{esc(e.name)}` from {e.section}. Explain why in the description (archived, unmaintained, or no longer a gateway)."))
    return out


def build_pr_report(pr, results, pr_findings, lint):
    errors, warnings = count(results, pr_findings)
    if lint and not lint[0]:
        errors += 1
    if errors:
        head = f"### ❌ {errors} problem{'s' if errors != 1 else ''} to fix" + (f", {warnings} warning{'s' if warnings != 1 else ''}" if warnings else "")
    elif warnings:
        head = f"### ⚠️ No blocking problems, {warnings} warning{'s' if warnings != 1 else ''} to look at"
    else:
        head = "### ✅ All automated checks passed"
    parts = [COMMENT_MARKER, "## Automated review", "", head, ""]
    if not results:
        parts += ["No list entries were added or changed in README.md.", ""]
    for e, f in results:
        parts += [entry_block(e, f), ""]
    if pr_findings:
        parts += ["**Pull request**", ""] + [f"- {ICON[l]} {m}" for l, m in pr_findings] + [""]
    if lint is not None:
        ok, lines = lint
        parts += ["**awesome-lint**", ""]
        parts += ["- ✅ No new problems."] if not lines else [f"- {'❌' if l.startswith('✖') else '⚠️'} `{esc(l[1:].strip())}`" for l in lines[:15]]
        parts.append("")
    parts += [
        "<details><summary>What a maintainer checks next</summary>",
        "",
        "- The product sits in the request path for LLM, MCP, or agent traffic and fits the section.",
        "- Every claim in the description appears on the linked page, in neutral wording.",
        "- Open source: maintained and adopted (200+ stars or an established maintainer). Commercial: generally available with public documentation of the gateway feature.",
        "- The pull request discloses any affiliation.",
        "",
        "</details>",
        "",
        f"<sub>Checks follow [contributing.md](https://github.com/{REPO}/blob/main/contributing.md#entry-format). This comment updates on every push.</sub>",
    ]
    return "\n".join(parts), errors, warnings


def upsert_comment(number, body):
    comments = gh_api(f"repos/{REPO}/issues/{number}/comments?per_page=100")
    mine = [c for c in comments if COMMENT_MARKER in (c.get("body") or "") and c["user"]["type"] == "Bot"]
    if mine:
        gh_api(f"repos/{REPO}/issues/comments/{mine[0]['id']}", "PATCH", {"body": body})
    else:
        gh_api(f"repos/{REPO}/issues/{number}/comments", "POST", {"body": body})


def set_labels(number, add, remove):
    current = {l["name"] for l in gh_api(f"repos/{REPO}/issues/{number}/labels")}
    for name in remove & current:
        try:
            gh_api(f"repos/{REPO}/issues/{number}/labels/{urllib.parse.quote(name)}", "DELETE")
        except urllib.error.HTTPError:
            pass
    if add - current:
        gh_api(f"repos/{REPO}/issues/{number}/labels", "POST", {"labels": sorted(add - current)})


def cmd_pr(args):
    pr, files, base_text, head_text = fetch_pr(args.pr)
    base_entries, _ = parse(base_text)
    if head_text is None:
        results, head_entries, added, removed = [], [], [], []
    else:
        head_entries, problems = parse(head_text)
        base_lines = {e.raw for e in base_entries}
        changed = [e for e in head_entries if e.raw not in base_lines]
        changed_lines = {e.line_no for e in changed}
        base_names = {e.name.lower() for e in base_entries}
        head_names = {e.name.lower() for e in head_entries}
        added = [e for e in changed if e.name.lower() not in base_names]
        removed = [e for e in base_entries if e.name.lower() not in head_names]
        base_raw = set(base_text.splitlines())
        new_problems = [p for p in problems if p[2] not in base_raw]
        results = collect(changed, head_entries, new_problems, network=True)
        # Order problems caused elsewhere in a touched section are reported on the changed entries only.
        results = [(e, f) for e, f in results if e.line_no in changed_lines or e.url == ""]
    pr_findings = pr_level_findings(pr, files, added, removed)
    lint = None
    if args.lint and head_text is not None:
        lint = run_awesome_lint(head_text, args.lint_cmd.split())
    report, errors, warnings = build_pr_report(pr, results, pr_findings, lint)
    print(report)
    if args.post:
        upsert_comment(args.pr, report)
        labels = {"needs changes"} if errors else {"ready for review"}
        if added:
            labels.add("new entry")
        set_labels(args.pr, labels, {"needs changes", "ready for review"} - labels)
    if args.summary and os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(report.replace(COMMENT_MARKER, "") + "\n")
    return 1 if errors else 0


def cmd_full(args):
    text = open(args.readme).read()
    entries, problems = parse(text)
    results = collect(entries, entries, problems, network=True)
    flagged = [(e, f) for e, f in results if f]
    errors, warnings = count(results)
    date = datetime.date.today().isoformat()
    if flagged:
        lines = [ISSUE_MARKER, f"Check of {len(entries)} entries on {date}: {errors} errors, {warnings} warnings.", ""]
        lines += [entry_block(e, f) + "\n" for e, f in flagged]
        lines.append("Errors usually mean a broken link, an archived or unmaintained repository, or a moved anchor. Warnings need a quick manual look.")
        report = "\n".join(lines)
    else:
        report = f"{ISSUE_MARKER}\nCheck of {len(entries)} entries on {date}: no problems found."
    print(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
            fh.write(report.replace(ISSUE_MARKER, "") + "\n")
    if args.issue:
        # Warnings alone (bot-blocked pages, star counts) stay in the job summary; errors open an issue.
        issues = gh_api(f"repos/{REPO}/issues?state=open&labels=maintenance&per_page=50")
        mine = [i for i in issues if ISSUE_MARKER in (i.get("body") or "")]
        if errors and mine:
            gh_api(f"repos/{REPO}/issues/{mine[0]['number']}", "PATCH", {"body": report})
        elif errors:
            gh_api(f"repos/{REPO}/issues", "POST", {"title": "List health report", "body": report, "labels": ["maintenance"]})
        elif mine:
            gh_api(f"repos/{REPO}/issues/{mine[0]['number']}/comments", "POST", {"body": f"No errors in the check of {len(entries)} entries on {date}. Closing."})
            gh_api(f"repos/{REPO}/issues/{mine[0]['number']}", "PATCH", {"state": "closed"})
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("readme", nargs="?", default="README.md")
    c.add_argument("--network", action="store_true", help="also check links and GitHub repositories")
    p = sub.add_parser("pr")
    p.add_argument("--pr", type=int, required=True)
    p.add_argument("--lint", action="store_true", help="run awesome-lint on the pull request README")
    p.add_argument("--lint-cmd", default="npx --yes awesome-lint@2.3.0")
    p.add_argument("--post", action="store_true", help="post or update the review comment and labels")
    p.add_argument("--summary", action="store_true", help="write the report to the job summary")
    f = sub.add_parser("full")
    f.add_argument("readme", nargs="?", default="README.md")
    f.add_argument("--issue", action="store_true", help="open, update, or close the health report issue")
    args = ap.parse_args()
    sys.exit({"check": cmd_check, "pr": cmd_pr, "full": cmd_full}[args.cmd](args))


if __name__ == "__main__":
    main()
