# Contribution Guidelines

Suggestions are welcome, from both users and vendors. Open a pull request to add, update, or remove an entry. If you are unsure where something fits, or you are suggesting a product you do not work on, use the [suggestion form](https://github.com/ai-gateways/awesome-ai-gateways/issues/new?template=suggest-an-entry.yml) instead.

## What belongs here

- Software that sits in the request path for LLM, MCP, or agent-to-agent (A2A) traffic and applies routing, access control, limits, guardrails, or logging to it.
- Specifications, standards, guides, and articles that help people run or choose such a gateway.

SDKs that only wrap provider APIs inside an application, model hosting services, and observability tools without a gateway are out of scope.

## Requirements for an entry

- **Open source projects** must be public, documented, not archived, and have a commit on the default branch within the last six months. Projects should have at least 200 GitHub stars or be maintained by an established company or foundation.
- **Commercial products** must be generally available, with self-serve sign-up or published pricing rather than a waitlist, and have a public product or documentation page that describes the gateway capability the entry claims.
- **Every claim must be verifiable** on the linked page or repository. Benchmark numbers belong only in entries whose linked source publishes them.
- **One entry per product.** Put it in the section that matches its main purpose. Section intros can mention products from other sections that also handle that traffic type.

Vendors are welcome to add their own products. Disclose the connection in the pull request, and expect descriptions to be edited for neutral wording.

## Entry format

```markdown
- [Name](link) - One-sentence factual description (`License`, `Language`).
```

- Link open source projects to their repository and commercial products to the page that describes the gateway feature.
- Any other link, in a resource section or inside a description, must point to the exact section of the page, using a heading anchor or a `#:~:text=` fragment when the page has no anchors.
- Use the [SPDX identifier](https://spdx.org/licenses/#preamble) that GitHub reports for the repository, followed by the main implementation language. Use `Proprietary` for commercial products and for AI features that need a paid edition. Specifications, guides, and articles take no tags.
- Write one sentence in US English, under 280 characters, that says what the software does. Name the main capabilities; skip slogans, superlatives, and comparisons with other entries.
- Keep each section in alphabetical order, ignoring case.
- Do not use em dashes or en dashes. The hyphen between the link and the description is the only separator.

## Pull requests

- Add one product per pull request, and fill in the pull request template, including your affiliation.
- Use a title such as `Add Name`, `Update Name`, or `Remove Name`.
- To remove an entry, say why (archived, unmaintained, discontinued, or no longer a gateway) and link the evidence.

## How pull requests are reviewed

1. **Automated review.** Within a few minutes, a bot comments on the pull request and labels it `needs changes` or `ready for review`. The comment updates on every push. It checks:
   - the entry format, tags, sentence length, marketing language, and dashes;
   - alphabetical order and duplicate products or links;
   - that every link loads and every section anchor or `#:~:text=` fragment exists on the page;
   - for GitHub repositories, whether the project is archived, when it last had a commit, its star count, and whether the license tag matches;
   - [awesome-lint](https://github.com/sindresorhus/awesome-lint#usage) on the whole list.
2. **Maintainer review.** A maintainer checks what a script cannot: that the product fits the section, that each claim matches the linked page, that the wording is neutral, and that the project clears the adoption bar.

Warnings are not blocking on their own. A maintainer may still merge a pull request with a warning, such as a page that blocks automated requests, after checking it by hand.

### Check your entry locally

The checker needs only Python 3.9 or later:

```sh
python3 .github/scripts/review.py check README.md
python3 .github/scripts/review.py check README.md --network
```

The first command runs the format, order, and duplicate checks. The second also loads every link and queries GitHub, which takes a minute or two.

## Keeping the list current

A scheduled job rechecks every entry each week and opens a `List health report` issue when a link breaks, an anchor moves, or a repository is archived or goes quiet for six months. To report a problem yourself, use the [report form](https://github.com/ai-gateways/awesome-ai-gateways/issues/new?template=report-an-entry.yml).

Entries can be removed when a project is archived, stops being maintained, or no longer matches its description.
