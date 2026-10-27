# GitHub repository profile — maintainer checklist

**27 October 2026.** This file records suggested metadata and publication steps. It **does not** assert that the repository's About, Topics, GitHub Pages or Releases settings have been changed.

## About description (copy exactly)

Privacy-first chemical sensing for critical infrastructure: dual-path alerts, k>=50 aggregate analytics, and hardware PII isolation (research).

## Topics (GitHub Settings / About gear icon)

`critical-infrastructure`, `privacy-engineering`, `chemical-sensing`, `embedded-security`, `differential-privacy`, `post-quantum-cryptography`, `security-research`, `hardware-security`

Add these manually in the GitHub repository's **About** editor; file commits cannot edit GitHub repository metadata. Keep keywords accurate: projects that are not yet field-deployable should not be described as a certified explosives detector.

## Optional: publish the HTML storyboard as GitHub Pages

1. From the repository, open **Settings -> Pages** (requires permissions).
2. Choose **Deploy from a branch**, select **main** and folder **/docs**.
3. After GitHub reports a deployment URL, open `/demo-49-to-50.html` or `/` if `docs/index.html` serves as the homepage.
4. Verify content from a private browser window and test mobile/keyboard behavior.
5. Only then share the Pages URL as a live demo; currently the HTML can be downloaded and opened offline.

No user tracking or analytics scripts are embedded in the HTML storyboard. A GitHub Pages deployment may still generate GitHub-hosted access logs, which are outside this source's control.

## Optional: stable publication and citations

- `CITATION.cff` supplies GitHub's basic citation metadata; it is **not a DOI**.
- Publish a named GitHub Release only after defining licensing and release governance; optional Zenodo archival may provide a DOI.
- Do not backdate the 2026 reconstructed Python code to the 2025 white paper.

## Promotion with evidence, not inflated claims

Lead with the 49/50 script, its CI tests and the explicit limitations. Invite independent review of the PII hardware isolation design and the tension between a hard k-gate and end-to-end DP. Ask for measurable feedback rather than stars.
