# Citation Verification

Before finalizing a citation, verify at least TWO of:
- DOI (CrossRef verification — most reliable)
- arXiv ID (check that it resolves to the correct paper)
- Official proceedings page (publisher website)
- Venue proceedings page (e.g., CVPR open access, ACL Anthology)
- DBLP entry (for CS venues — well-curated)
- Semantic Scholar entry (cross-reference with DOI/arXiv)
- PubMed ID for biomedical work
- ACL Anthology ID for NLP papers

## API-Based Verification

Use the automated scripts:

```bash
# Verify a list of citations
python literature/scripts/verify_citations.py citations.txt --sources crossref,dblp --output verified.md

# Verify BibTeX entries
python literature/scripts/verify_citations.py --bibtex refs.bib --verify-all --output bib_verified.md
```

## Manual Verification Checklist

For each citation, confirm (✓/✗/?):

- [ ] Title matches across sources (at least 2 sources agree)
- [ ] First author name is consistent
- [ ] Year is correct
- [ ] Venue is correct (conference name, journal name)
- [ ] DOI resolves to the correct paper
- [ ] arXiv ID resolves to the correct paper
- [ ] The paper actually exists (not a hallucination)

## DOI Parsing Rules

Extract DOI from common formats:
- Full URL: `https://doi.org/10.1007/978-3-030-58595-7_1` → `10.1007/978-3-030-58595-7_1`
- Bare: `10.1109/CVPR.2021.00045`
- arXiv paper may not have a DOI; check if later published at a venue

## BibTeX Field Completeness

Required fields per entry type:

**@article:**
- author, title, journal, year (required)
- volume, number, pages, doi (strongly recommended)
- eprint, archivePrefix (for arXiv preprints)

**@inproceedings:**
- author, title, booktitle, year (required)
- pages, doi, address (strongly recommended)

**@misc (arXiv preprint):**
- author, title, year, eprint, archivePrefix (required)
- note (optional: "arXiv preprint")

## Safe Citation Wording

When a paper is relevant but not fully verified, write:
> "A related line of work appears to address ..., but citation metadata still needs verification. [CITATION NEEDED]"

When metadata is partially verified (single source):
> "Preliminary verification suggests that [brief_description], pending cross-reference confirmation."

Never output final BibTeX when:
- Author order is uncertain
- Title is uncertain
- Year/venue is uncertain
- DOI/arXiv/proceedings page is missing
- The paper's existence cannot be confirmed

## Common Citation Format Issues

1. **Author name normalization**: "J. Smith", "John Smith", "Smith, J." → Choose one format and stick to it. First-name-last-name is preferred for readability.

2. **Venue abbreviation**: "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition" vs "CVPR" → Use standard abbreviations consistently. DBLP provides canonical venue abbreviations.

3. **Year verification**: ArXiv submission year ≠ publication year. If a preprint was later published at a venue, use the venue year.

4. **Page numbers**: Some publishers use article numbers instead of page ranges (e.g., IEEE Access: "pp. 1-10" → "Art. no. 1234567"). Check the actual publication format.

5. **BibTeX special characters**: Escape `& % $ # _ { } ~ ^ \` in BibTeX fields. Author names with accented characters need LaTeX encoding (e.g., `{\"o}` for ö).
