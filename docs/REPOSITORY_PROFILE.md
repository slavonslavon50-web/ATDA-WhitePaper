# GitHub repository profile — maintainer checklist

**27 October 2026.** This file records suggested metadata and publication steps. It **does not** assert that the repository's About, Topics, GitHub Pages or Releases settings have been changed.

## About description (copy exactly)

Privacy-first chemical sensing for critical infrastructure: dual-path alerts, k>=50 aggregate analytics, and hardware PII isolation (research).

## Topics (GitHub Settings / About gear icon)

`critical-infrastructure`, `privacy-engineering`, `chemical-sensing`, `embedded-security`, `differential-privacy`, `post-quantum-cryptography`, `security-research`, `hardware-security`

Add these manually in the GitHub repository's **About** editor; file commits cannot edit GitHub repository metadata. Keep keywords accurate: projects that are not yet field-deployable should not be described as a certified explosives detector.

## Live GitHub Pages status

- GitHub Pages was enabled from `main` / `/docs` and deployment succeeded on 27 October 2026.
- Public demonstration URL: https://slavonslavon50-web.github.io/ATDA-WhitePaper/
- Repository About description and Topics are separate GitHub metadata, and still need the maintainer to save them through the gear icon. The connected integration can edit files but cannot update this repository metadata.

## How to verify or reconfigure GitHub Pages

1. From the repository, open **Settings -> Pages** (requires permissions).
2. Choose **Deploy from a branch**, select **main** and folder **/docs**.
3. Confirm the main site `/` serves `docs/index.html` and the 49-to-50 walkthrough.
4. Verify content from a private browser window and test mobile/keyboard behavior.
5. The site is already deployed; use the public Pages URL above after checking layout in a browser.

No user tracking or analytics scripts are embedded in the HTML storyboard. A GitHub Pages deployment may still generate GitHub-hosted access logs, which are outside this source's control.

## Optional: stable publication and citations

- `CITATION.cff` supplies GitHub's basic citation metadata; it is **not a DOI**.
- Publish a named GitHub Release only after defining licensing and release governance; optional Zenodo archival may provide a DOI.
- Do not backdate the 2026 reconstructed Python code to the 2025 white paper.

## Who the project seeks feedback from

- University privacy and embedded-security researchers (Trinity College Dublin / University College Dublin as potential audiences, without claiming contact or institutional involvement).
- Chemical sensing and embedded electronics manufacturers to critique the proposed HW-01 bench design.
- Critical-infrastructure engineers and standards specialists familiar with NIST, ENISA and IEC 62443 to validate assurance gaps and controls.

Requests should cite concrete technical issues, and must not imply any of these entities endorse ATDA.

## Promotion with evidence, not inflated claims

Lead with the 49/50 script, its CI tests and the explicit limitations. Invite independent review of the PII hardware isolation design and the tension between a hard k-gate and end-to-end DP. Ask for measurable feedback rather than stars.
