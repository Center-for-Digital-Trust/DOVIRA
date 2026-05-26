# DOVIRA: Client-Side PII Scrubber & Anonymous Dataset Engine (Open Core)

## Overview
**DOVIRA** (Digital Trust Framework) is an open-source, client-side personal data cleanup engine designed to securely develop and structure AI prompts, meet zero-data-retention requirements, and systematically build sovereign AI training datasets.

## The Problem
Public organizations and NGOs handle highly sensitive citizen data. Sending raw text to cloud-based AI providers risks exposing this data. Furthermore, organizations lose valuable intellectual capital by contributing raw operational data to external AI telemetry without building their own internal knowledge bases.

## The Solution: Zero-Data Retention & Sovereign AI Infrastructure
DOVIRA acts as a local security and data engineering architecture that intercepts text inputs directly on the user's machine:
1. **Local Masking:** Before data leaves the device, DOVIRA detects sensitive entities (emails, phone numbers, document IDs) and replaces them with anonymous tokens.
2. **Safe Cloud Transmission:** The sanitized text is transmitted to the cloud AI for processing via layers like Nudge MD™.
3. **Local Re-Assembly:** Once the AI returns the response, DOVIRA locally maps the tokens back to the original values. 

*Sensitive data never leaves the client's local secure environment.*

## Core Technical Features & Frameworks
* **100% Offline Processing:** The tokenization and masking process requires zero external network dependencies.
* **Individual Work Accounting Framework:** Includes integrated local logging to track prompt engineering efficiency, audit user workflows, and evaluate individual contributions to the organization's prompt repository.
* **Training Dataset Generation:** Automatically compiles sanitized, structured prompt-response pairs into clean, local datasets. This enables organizations to safely train or fine-tune local open-source LLMs without violating GDPR or data protection laws.
* **Deterministic Performance:** Powered by optimized, strict regular expressions (RegEx) ensuring 0ms latency impact on daily operational workflows.

## Institutional Context
Developed and maintained by **Center for Digital Trust (ГО "Центр цифрової довіри")**, Ukraine.

## License
Distributed under the GNU General Public License v3.0 (GPLv3).

## Contact
For audits, deployment inquiries, or public sector pilots:  
**Email:** Center@digitaltrust.living
