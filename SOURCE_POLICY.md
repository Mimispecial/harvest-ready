# Source Policy

## Authoritative source collection

The stored lot label and context, advisory boundary, ordered readiness signs, round label, and grower's declared observation. No sensor, weather service, or farm record is fetched.

Those normalized on-chain values are the complete authoritative collection for consensus. A reviewer can reconstruct the exact packet without trusting a mutable external page.

## No autonomous retrieval

This contract performs no HTTP request, web search, URL rendering, oracle lookup, file download, or hidden enrichment. A URL, filename, checksum, or source label inside user text remains an untrusted declaration; validators are not asked to open it.

## Collection responsibility

The deployer and participants must provide complete, lawfully usable, non-secret material. On-chain storage proves which normalized bytes were considered; it does not prove authorship, completeness, ownership, provenance, or real-world truth.

## Normalization and limits

Text inputs normalize CRLF or CR to LF, trim surrounding whitespace, and enforce field-specific minimum and maximum lengths. Collection sizes and revision loops are capped. Model output uses closed categories, fixed-order masks, or compact codes and fails closed on extra, missing, malformed, or out-of-range values.

## Prompt-injection boundary

Evidence is serialized as sorted JSON and surrounded by named START/END delimiters. The prompt states that the packet is data, never instructions. Each validator independently replays the assessment before a result can enter state.

## Interpretation boundary

Observations are self-declared and are not verified against sensors or images. The result is not agronomy, food-safety, weather, or regulatory advice. Applications must disclose these limits beside results and use a fresh deployment when the authoritative source collection or policy changes.
