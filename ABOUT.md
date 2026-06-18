ABOUT

Candidate

Sean Jones

Approach

I started by creating and committing a plan before reading the clarification document or writing any solution code. My goal was to build a simple contact-finder that prioritized accuracy and traceability over returning a large number of contacts.

The solution reads the company CSV, looks up available information from the mock providers, combines the results, calculates a confidence score, and determines whether a contact can be returned automatically or should be flagged for human review.

Confidence Logic

My confidence scoring is based on the strength and agreement of available sources.

Confidence increases when:

* Multiple providers return the same person
* Contact information is available and complete
* The role appears relevant to collections or financial decision-making
* The enrichment provider reports a strong confidence score
* Multiple sources support the same contact information

Confidence decreases when:

* Only a single source is available
* Information cannot be cross-verified
* The enrichment confidence is low
* The role is unclear or missing
* Sources provide conflicting information

Any result below the required threshold of 70 is returned with an empty contact field and marked for human review.

Design Decisions

I chose to prioritize precision over recall. A smaller set of verified and traceable contacts is more valuable than returning a larger number of uncertain contacts.

Every returned contact includes provenance information so the result can be audited and reviewed later if needed.

When confidence is too low, the system returns a human-review state rather than making assumptions or fabricating a contact.

Reflection

Ambiguity

One ambiguity was determining how much weight should be given to the enrichment provider’s confidence score. The challenge specified that provider confidence should not be treated as the final confidence score, but it did not define exactly how the signals should be combined. I treated provider confidence as one signal among several rather than the primary factor.

Tradeoff

The main tradeoff was precision versus recall. I intentionally used a conservative approach that favors accuracy. This means fewer contacts are automatically returned, but the contacts that are returned have stronger supporting evidence and are easier to trust.

Mistake

My initial scoring approach gave too much credit to a single provider returning contact information. After reviewing the challenge requirements more carefully, I adjusted the logic so that contacts with limited verification would more often be routed to human review.

Review Comment That Changed My Mind

The clarification document stated that a high human-review rate is a positive outcome when records are difficult to verify. Initially I focused on maximizing the number of returned contacts, but after reading that guidance I shifted toward a more conservative scoring strategy that favors correctness and traceability over coverage.

AI Usage

I used AI tools to help understand requirements, organize my thoughts, review assumptions, and speed up development. Final implementation decisions, scoring choices, and design tradeoffs were reviewed and adjusted by me.

Future Improvements

If this were expanded beyond the challenge, I would:

* Improve confidence scoring with weighted source reliability
* Add stronger contact matching and deduplication logic
* Support additional enrichment providers
* Add logging and reporting for human-review cases
* Build a simple review interface for flagged records
* Track historical verification outcomes to improve scoring over time