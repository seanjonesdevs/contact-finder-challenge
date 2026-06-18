PLAN

Understanding of the Problem

We have a list of companies with only a company name and mailing address. The goal is to identify the most relevant person to contact regarding unpaid accounts, such as an owner, CFO, accounts payable manager, or office manager. Not every contact will be available or verifiable, so the system must prioritize accuracy and confidence over guessing.



Architecture

I would build a pipeline that processes each company record and searches multiple data sources for possible contacts.

The workflow would be:

1. Load company data from the CSV.
2. Search multiple sources for potential contacts.
3. Normalize and combine the results.
4. Remove duplicate contacts.
5. Assign a confidence score based on supporting evidence.
6. Return the best contact along with source information and confidence level.
7. Flag low-confidence or unverifiable results for human review.

This approach allows the system to scale while maintaining transparency and traceability.


Sources and Strategy

I would use multiple source types rather than relying on a single provider.

Potential sources include:

* Business databases
* Company websites
* Professional networking data
* Public business records
* Contact enrichment providers

Using multiple sources helps improve accuracy because information can be cross-checked. If several sources return the same person and role, confidence increases significantly.



Quality and Verification

Deduplication

Contacts would be deduplicated using:

* Name matching
* Email matching
* Phone matching
* Role matching

This prevents the same person from appearing multiple times.

Confidence Scoring

Confidence scores would be based on factors such as:

* Number of sources confirming the contact
* Match between company and contact
* Match between role and desired decision-maker
* Freshness and completeness of the information

Example:

* 90-100 = Strongly verified
* 70-89 = Likely correct
* 50-69 = Possible match
* Below 50 = Needs human review

Provenance

Every contact should include source information showing where the data came from.

This makes all results traceable and easier to audit.

Cannot Verify State

If a contact cannot be verified with sufficient confidence, the system should return a “cannot verify” result instead of guessing.

Avoiding false positives is more important than returning a questionable contact.



Privacy and Compliance

I would only use data from approved and compliant sources.

I would not:

* Scrape private information
* Bypass access controls
* Collect sensitive personal data
* Use information that violates privacy regulations

The system should prioritize responsible data collection and maintain clear source tracking.



Clarifying Questions

Question 1

What confidence score should trigger human review?

Why it matters:

This determines when a result is considered reliable enough for automation.

Default assumption:

Any score below 70 requires human review.

What changes:

Different thresholds would affect how many contacts are automatically accepted versus manually reviewed.



Question 2

Are generic company emails acceptable if no decision-maker can be verified?

Why it matters:

Some companies may not have publicly available contact information for a specific person.

Default assumption:

Generic emails are acceptable but should receive a lower confidence score.

What changes:

If generic emails are not acceptable, the system would return “cannot verify” more frequently.



Question 3

Which data sources are approved for use?

Why it matters:

The design may change depending on available providers and compliance requirements.

Default assumption:

Multiple approved business and enrichment sources are available.

What changes:

The source selection, confidence scoring, and verification process would be adjusted based on the approved providers.