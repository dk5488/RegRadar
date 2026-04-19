# Implementation Plan: Scraper Verification & Fixes

Our primary objective is to verify that **every single scraper** actively fetches real, usable regulatory data without being blocked by WAFs (like Akamai) or failing due to broken HTML layouts. Since some endpoints are heavily protected or have unique structures, they must be tested and patched individually.

Per your instructions, each scraper will be isolated, tested, fixed, and committed to its own dedicated `F-**` feature branch.

## High-Level Strategy

To avoid regressions, the global HTTP `safe_get` engine must first be finalized. We migrated `base.py` to use `curl_cffi` to spoof Chrome TLS fingerprints securely (avoiding Cloudflare/Akamai 403s globally). This global change must be our baseline.

For each scraper in our registry, the following loop will be executed:
1. **Branch Creation**: Check out an isolated branch (e.g., `F-07-mca-scraper`).
2. **Targeted Test Execution**: Run an isolated test extracting data purely using that specific class. 
3. **Diagnosis**: If the test fails (e.g., `403 Forbidden`, `CSS Selector Mismatch`, `Encoding Error`), evaluate the specific government HTML payload.
4. **Resolution**: Apply tailored XPath configurations, pagination logic, or fallback mechanisms.
5. **Validation & Commit**: Verify `RawDocument` objects are successfully hydrated, print the results, and commit.

## Proposed Execution Order

Given the sheer volume of 19 scrapers in the registry, we will start with the hardest and highest-priority Central sources, moving down sequentially:

### Phase 1: Critical Central Sources 
*   **F-07**: MCA Scraper (Fix remaining pagination/sub-URL structures).
*   **F-08**: RBI Scraper (Implement robust RSS override and HTML fallback).
*   **F-09**: CBIC Scraper (Verify GST notifications indexing).
*   **F-10**: SEBI Scraper (Test their specific RSS feed).

### Phase 2: Crucial Labour & Tax
*   **F-11**: EPFO Scraper
*   **F-12**: ESIC Scraper
*   **F-13**: Income Tax Dept / CBDT

### Phase 3: Gazette & Trade
*   **F-** : Gazette of India, DGFT, FSSAI, BIS, IRDAI

### Phase 4: State-Level Pipelines
*   **F-** : Karnataka, Maharashtra, Tamil Nadu, Delhi, Gujarat

## Open Questions

Before I begin spinning up the isolated test script and branching off to fix **MCA (`F-07`)** and **RBI (`F-08`)**:
1. Do you want me to process these sequentially until we get through the entire list, or focus strictly on Phase 1 for now?
2. Since `base.py` was altered to support the `curl_cffi` WAF bypass, I will commit this to a root `F-06-base-client` branch first so all subsequent scraper branches inherit the WAF-bypass logic. Does this sound correct?
