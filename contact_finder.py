import csv
import json
from pathlib import Path


CONFIDENCE_THRESHOLD = 70

ROLE_PRIORITY = {
    "accounts payable": 1,
    "ap manager": 1,
    "owner": 2,
    "founder": 2,
    "president": 2,
    "cfo": 3,
    "finance lead": 3,
    "manager": 4,
    "office manager": 4,
    "registered agent": 5,
}


def normalize(value):
    return (value or "").strip().lower()


def role_rank(role):
    role_text = normalize(role)

    for key, rank in ROLE_PRIORITY.items():
        if key in role_text:
            return rank

    return 6


def collect_sources(provider_data):
    sources = []

    for provider_name, data in provider_data.items():
        source_url = data.get("source_url")
        if source_url:
            sources.append(f"{provider_name}:{source_url}")

    return sources


def choose_contact(company_name, provider_data):
    registry = provider_data.get("registry", {})
    listing = provider_data.get("listing", {})
    enrichment = provider_data.get("enrichment", {})

    sources = collect_sources(provider_data)

    registry_name = registry.get("name")
    registry_role = registry.get("role")

    listing_name = listing.get("name")
    listing_phone = listing.get("phone")

    enrichment_email = enrichment.get("email")
    enrichment_phone = enrichment.get("phone")
    provider_confidence = enrichment.get("provider_confidence", 0)

    contact_name = registry_name or listing_name or ""
    contact_role = registry_role or ""

    contact_email_or_phone = (
        enrichment_email
        or enrichment_phone
        or listing_phone
        or ""
    )

    confidence_score = 0

    # Base score from enrichment provider if it exists.
    if provider_confidence:
        confidence_score = provider_confidence

    # Registry gives strong identity/role provenance.
    if registry_name:
        confidence_score += 15

    # Listing gives useful business contact support.
    if listing_phone:
        confidence_score += 8

    # Same/similar name across registry and listing increases confidence.
    if registry_name and listing_name:
        if normalize(registry_name) == normalize(listing_name):
            confidence_score += 10
        elif normalize(registry_name).split()[-1:] == normalize(listing_name).split()[-1:]:
            confidence_score += 5

    # Role quality matters.
    rank = role_rank(contact_role)
    if rank == 1:
        confidence_score += 15
    elif rank == 2:
        confidence_score += 10
    elif rank == 3:
        confidence_score += 8
    elif rank == 4:
        confidence_score += 4
    elif rank == 5:
        confidence_score -= 10

    # Generic emails are weaker than person-specific emails.
    if enrichment_email and enrichment_email.split("@")[0] in ["info", "contact", "sales", "office"]:
        confidence_score -= 12

    # Do not exceed 100 or go below 0.
    confidence_score = max(0, min(100, confidence_score))

    needs_human_review = confidence_score < CONFIDENCE_THRESHOLD

    if needs_human_review:
        return {
            "company_name": company_name,
            "contact_name": "",
            "contact_role": "",
            "contact_email_or_phone": "",
            "confidence_score": confidence_score,
            "source": "; ".join(sources),
            "needs_human_review": "true",
        }

    return {
        "company_name": company_name,
        "contact_name": contact_name,
        "contact_role": contact_role,
        "contact_email_or_phone": contact_email_or_phone,
        "confidence_score": confidence_score,
        "source": "; ".join(sources),
        "needs_human_review": "false",
    }


def main():
    companies_path = Path("challenge/data/companies.csv")
    mock_path = Path("challenge/mocks/enrichment_responses.json")
    output_path = Path("contact_results.csv")

    with companies_path.open(newline="") as file:
        companies = list(csv.DictReader(file))

    with mock_path.open() as file:
        mock_responses = json.load(file)

    results = []

    for company in companies:
        company_name = company["company_name"]
        provider_data = mock_responses.get(company_name, {})
        result = choose_contact(company_name, provider_data)
        results.append(result)

    fieldnames = [
        "company_name",
        "contact_name",
        "contact_role",
        "contact_email_or_phone",
        "confidence_score",
        "source",
        "needs_human_review",
    ]

    with output_path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Wrote {len(results)} rows to {output_path}")


if __name__ == "__main__":
    main()