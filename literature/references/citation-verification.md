# Citation Verification

Before finalizing a citation, verify at least one of:

- DOI
- arXiv ID
- Official paper URL
- Venue proceedings page
- Publisher page
- PubMed ID for biomedical work
- ACL Anthology ID for NLP
- CrossRef metadata

## Do not output final BibTeX when

- author order is uncertain
- title is uncertain
- year/venue is uncertain
- DOI/arXiv/proceedings page is missing

Use `[CITATION NEEDED]` or `[METADATA NEEDS VERIFICATION]` instead.

## Safe citation wording

When a paper is relevant but not fully verified, write:

```text
A related line of work appears to address ..., but citation metadata still needs verification. [CITATION NEEDED]
```
