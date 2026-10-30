# Contribution Guidelines

Suggestions are welcome, from both users and vendors. Open a pull request to add, update, or remove an entry, or open an issue if you are unsure where something fits.

## What belongs here

- Software that sits in the request path for LLM, MCP, or agent-to-agent (A2A) traffic and applies routing, access control, limits, guardrails, or logging to it.
- Specifications, standards, guides, and articles that help people run or choose such a gateway.

SDKs that only wrap provider APIs inside an application, model hosting services, and observability tools without a gateway are out of scope.

## Requirements for an entry

- **Open source projects** must be public, documented, not archived, and have a commit on the default branch within the last six months. Projects should have at least 200 GitHub stars or be maintained by an established company or foundation.
- **Commercial products** must have a public product or documentation page that describes the gateway capability the entry claims.
- **Every claim must be verifiable** on the linked page or repository. Benchmark numbers belong only in entries whose linked source publishes them.
- **One entry per product.** Put it in the section that matches its main purpose. Section intros can mention products from other sections that also handle that traffic type.

## Entry format

```markdown
- [Name](link) - One-sentence factual description (`License`, `Language`).
```

- Link open source projects to their repository and commercial products to the page that describes the gateway feature. Links to documentation and articles should point to the most relevant section, using a heading anchor or a `#:~:text=` fragment when the page has no anchors.
- Use the [SPDX identifier](https://spdx.org/licenses/#preamble) of the license that covers the gateway features, followed by the main implementation language. Use `Proprietary` for commercial products and for AI features that need a paid edition.
- Write one sentence in US English that says what the software does. Skip slogans, superlatives, and comparisons with other entries.
- Keep each section in alphabetical order, ignoring case.
- Do not use em dashes or en dashes. The hyphen between the link and the description is the only separator.

## Pull requests

- Add one product per pull request, and say how you are connected to it, if at all.
- Use a title such as `Add Name` or `Update Name`.
- Check spelling and grammar, and run [awesome-lint](https://github.com/sindresorhus/awesome-lint#usage) before submitting.

Entries can be removed when a project is archived, stops being maintained, or no longer matches its description.
