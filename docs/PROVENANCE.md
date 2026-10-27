# Source provenance and reconstruction declaration

**Audit date: 2026-10-27.**

## Confirmed original publication evidence

- **2025-12-05**: `WhitePaper_ATDA_Privacy_Preserving_Detection_2025_v5.pdf`, author V. Panov, original source document recovered through the owner's connected Google Drive. It introduces the dual Path A/B architecture, baseline contamination safeguards, legal limits, non-contact sensing horizon and public defensive-publication intent. Source: https://drive.google.com/file/d/1lEXMtkPDWbe5ruQFORrCpHwERX4Ba9fw/view (access may require owner permission).
- **2025-12-05 04:40 UTC**: Public GitHub repository creation date (GitHub repository metadata).
- **2026-01-30 10:47 UTC**: Historical GitHub root commit `a754b3fe1c2bb4dcc132febb3f1e1e35059a99f1` by `V.Panov`; tree SHA `d1a09b765e74311688408741443b18a993d87890`. GitHub independently reports **a single actual blob** `ATDA_Privacy_Safety_Manifest_v1.json`. Although the commit message names PDFs, Python code, README and CI, none of these files appears in the commit tree. Link: https://github.com/slavonslavon50-web/ATDA-WhitePaper/commit/a754b3fe1c2bb4dcc132febb3f1e1e35059a99f1
- The historical `.json` is **Markdown-like narrative, not parseable JSON**. It is intentionally preserved unchanged as a primary historical exhibit.
- Owner discussions in January 2026 referred to v4.32/v4.35 and v5.0 Fortress Python sources and appendix files, but those original bytes have NOT been recovered from the GitHub tree, and no copy was found in currently accessible Drive search results. Thus exact byte-for-byte recovery is **not** claimed.

## What is NEW and must not be backdated

The 27 October 2026 implementation in `src/` and associated tests are **new independent reconstructions** of the public architectural rules, not originals from 2025 or 2026-01. The privacy proof corrects an unsupported full-mechanism pure ε-DP claim. The PQC annex cites algorithm standards published after the original concept and does not rewrite the historical artifact. The documentation does not establish that NIST was influenced by this repository; a claim would require specific provenance evidence beyond chronological proximity.

## Rules for future release/academic citation

1. Cite the 2025 white paper as an architectural publication with its original date and author.
2. Cite this repository's 2026 v1.2 source code as an audited **reference reconstruction**, specifying the actual GitHub commit.
3. Do NOT backdate generated files, retroactively alter the root commit, or assert unpublished PDFs were part of that commit.
4. Maintain the root historical file and the original white paper in an immutable evidence archive; optional SHA-256 should be computed from bytes with preserved metadata when accessible.
5. Keep government-only submission documents and sensitive detection thresholds OUT of the public repository.
6. Publish each revision with changed algorithms, test results and known limitations in the changelog.
