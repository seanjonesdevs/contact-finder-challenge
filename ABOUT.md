ABOUT

Candidate

Sean Jones

Approach

I started by creating a plan before reviewing the clarification document or writing any solution code. My goal was to build a simple contact-finder that prioritizes accuracy over volume and avoids returning contacts that cannot be reasonably verified.

The solution reads the company CSV, checks the available mock providers, combines the results, assigns a confidence score, and determines whether a contact can be returned automatically or should be flagged for human review.

Confidence Logic

My confidence score is based on the strength and agreement of available sources.

Confidence increases when:

* Multiple sources identify the same person
* Contact information is complete
* The contact appears to be a decision-maker
* Enrichment confidence is high

Confidence decreases when:

* Only a single source is available
* Information cannot be cross-verified
* The provider confidence is low
* The contact role is unclear

Any result below the required threshold of 70 is returned with an empty contact field and marked for human review.

Design Decisions

I prioritized precision over recall. A verified and traceable contact is more valuable than multiple low-confidence guesses.

Every returned contact includes source information so the result can be audited and reviewed later if needed.

The solution also supports situations where no contact can be confidently identified by returning a human-review state rather than making assumptions.

AI Usage

I used AI tools to help understand requirements, organize my planning process, and speed up development. Final implementation decisions, assumptions, and scoring logic were reviewed and adjusted by me.

Future Improvements

If this were expanded beyond the challenge, I would:

* Improve confidence scoring with weighted source reliability
* Add stronger contact matching and deduplication
* Support additional enrichment providers
* Add logging and reporting for human-review cases
* Build a simple interface for reviewing flagged results