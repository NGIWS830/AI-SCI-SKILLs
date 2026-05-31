# Template Filling Guide — Stage 4g

## Purpose

Guide for filling the three output templates with polished manuscript content from the pipeline. This stage is invoked after Stage 4e (English Polish) and 4f (Self-Critique) have passed quality threshold (score >= 80).

## Output Formats

| Format | Template | Output File | Required |
|--------|----------|-------------|----------|
| Chinese LaTeX | `templates/chinese/template.tex` | `<output_dir>/chinese_manuscript/` | Yes (reference) |
| English LaTeX | `templates/ieee-latex/template.tex` | `<output_dir>/english_manuscript/` | Yes (submission) |
| English Word | `templates/ieee-word/template.docx` | `<output_dir>/english_manuscript.docx` | Yes (submission) |
| Cover Letter LaTeX | `templates/cover-letter/template.tex` | `<output_dir>/cover_letter/` | Yes (submission) |
| Cover Letter Word | `templates/ieee-word/template.docx` | `<output_dir>/cover_letter.docx` | Yes (submission) |

## Content Source Mapping

Each template section draws from specific pipeline outputs:

| Template Section | Chinese LaTeX Source | IEEE LaTeX Source |
|-----------------|---------------------|-------------------|
| Title | Stage 1: 论文标题 (from project brief) | Stage 4e: English title (from `08_english_polished.md`) |
| Authors | Stage 0: Author-provided info | Stage 0: Author-provided info (English) |
| Affiliations | Stage 0: Author-provided info | Stage 0: Author-provided info (English) |
| Abstract | Stage 4c: `06_chinese_polished.md` 摘要 | Stage 4e: `08_english_polished.md` Abstract |
| Keywords | Stage 1: Task keywords + Stage 2: literature keywords | Stage 4e: Keywords |
| Introduction | Stage 4c: 引言 section | Stage 4e: Introduction section |
| Related Work | Stage 4c: 相关工作 section | Stage 4e: Related Work section |
| Method | Stage 4c: 方法 section (translated to match Stage 4e) | Stage 4e: Proposed Method section |
| Experiments | Stage 4c: 实验 section (translated to match Stage 4e) | Stage 4e: Experiments section |
| Conclusion | Stage 4c: 结论 section | Stage 4e: Conclusion section |
| References | Stage 2: Literature matrix (verified entries) | Stage 2: Literature matrix (verified entries) |

## Chinese LaTeX Filling Rules (cjc template)

### Metadata (`\classsetup{}`)

- `title` / `title*`: Chinese and English titles. Use the final title from Stage 4c.
- `authors`: Map each author with exact `name`, `name*`, `affiliations` reference, `email`.
- `affiliations`: Each `affN` with bilingual `name` / `name*`.
- `abstract` / `abstract*`: Bilingual abstracts. Chinese from `06_chinese_polished.md`, English from `08_english_polished.md`.
- `keywords` / `keywords*`: 5-7 keywords for each language. Consistent between Chinese and English — check against `ai-terminology-glossary.md`.
- `grants`: Funding information if provided. Format: "基金完整名称(No.项目号)".
- Leave `received-date`, `revised-date`, `publish-date`, `doi`, `clc`, `page` commented out for draft.

### Section Filling

- **引言** (Introduction): Use the standard 5-paragraph structure from `introduction-patterns.md`. Ensure contribution bullets have evidence pointers.
- **相关工作** (Related Work): Theme-based structure from Stage 2's "Related Work Structure". Each theme as `\subsection{}`.
- **方法** (Proposed Method): Keep `\subsection{}` per module. Every formula must have prose explanation. No orphan equations.
- **实验** (Experiments): Sub-sections: 数据集与实验设置, 与基线方法的对比, 消融实验, 效率分析, 定性分析.
- **结论** (Conclusion): Restate + future work. No new claims, no new citations.
- **致谢**: Fill from author-provided acknowledgments.
- **参考文献**: Generate `.bib` file from Stage 2's verified literature. Use `\cite{}` by BibTeX key.
- **附录** (Appendix): Only if there are detailed proofs or data tables that would disrupt main text flow.
- **作者简介** (`\makebiographies`): Fill author `biography`/`biography*` fields. Format: "性别，出生年，学位，职称，(CCF会员号)，主要研究领域."

### Chinese-Specific Formatting

- Figures: `\includegraphics[width=\linewidth]{filename}`. Figure captions in Chinese. Labels on axes in Chinese or quantity symbols.
- Tables: Use `booktabs` style (`\toprule`, `\midrule`, `\bottomrule`). Table headers in Chinese.
- Algorithms: Use `algorithm` + `algorithmic` packages. Pseudocode keywords in ALL CAPS. Variable names in italics.
- Theorem/Definition/Proof: Use `theorem` environment. Place lengthy proofs in appendix.
- Citations: `\cite{key}`. References numbered in order of first appearance.

### Compilation Check

```bash
cd <output_dir>/chinese_manuscript/
latexmk -xelatex chinese_manuscript.tex
```

---

## IEEE LaTeX Filling Rules (IEEEtran template)

### Title & Authors

- `\title{...}`: Final English title. Do NOT include line breaks, subtitles, footnotes, or special characters in title.
- Author block: Use `\IEEEauthorblockN{}` for name, `\IEEEauthorblockA{}` for affiliation. Maximum 6 authors per the standard template. If more, consolidate or ask author.
- Funding footnote: If applicable, add `\thanks{}` to the title.

### Abstract & Keywords

- Abstract: ~210 words (range 180-250). From `08_english_polished.md` Abstract section. Follow the 2-6-2 structure: 2 sentences background/gap, 6 sentences method (First/Second/Finally), 2 sentences results/implication. Include specific numbers (metric, dataset, value) in sentence 9.
- Keywords: 4-6 keywords. No abbreviations unless standard (e.g., CNN, NLP). Use `IEEEkeywords` environment.

### Section Filling

- **Introduction**: 5 paragraphs per `introduction-patterns.md`. Use `\section{Introduction}`.
- **Related Work**: `\section{Related Work}` with `\subsection{}` per theme. Avoid "Author et al. [X] proposed..." pattern.
- **Proposed Method**: `\section{Proposed Method}`. `\subsection{}` per module. Active voice for design rationale; passive acceptable for process description.
- **Experiments**: `\section{Experiments}`. Subsections: Datasets and Implementation Details, Comparison with State-of-the-Art, Ablation Study, Efficiency Analysis, Qualitative Analysis.
- **Conclusion**: `\section{Conclusion}`. Restate + future work.

### IEEE-Specific Formatting

- **Figures**: `\begin{figure}[htbp]` → `\centering` → `\includegraphics{filename}` → `\caption{...}` → `\label{fig:...}`. Refer as "Fig.~\ref{fig:...}". Figure labels: 8pt Times New Roman. Axis labels use words, not just symbols (e.g., "Accuracy (\%)" not "Acc").
- **Tables**: `\begin{table}[htbp]` → `\caption{...}` → `\label{tab:...}`. Use `booktabs` rules. Table footnotes with `$^{\mathrm{a}}$`.
- **Equations**: Number with `\begin{equation}`. Use `\eqref{eq:...}` for references. Punctuate equations as part of the sentence. No `{eqnarray}` — use `{align}` or `{IEEEeqnarray}`.
- **Algorithms**: Use `{algorithmic}`. Pseudocode keywords in CAPS.
- **Citations**: `\cite{b1}` — numbered in square brackets. Sentence punctuation follows bracket: "as shown in \cite{b2}." Six or more authors: use "et al." Format unpublished/in-press papers correctly (see `citation-verification.md`).
- **Tense conventions**:
  - Abstract: present (past for "We evaluated...")
  - Introduction: present (past for specific historical results)
  - Related Work: present perfect / present
  - Method: present
  - Experiments: past (present for "Table I reports...")
  - Conclusion: present

### Bibliography Generation (`.bib` file)

Generate `references.bib` from Stage 2's verified literature matrix. Requirements:
1. Only include VERIFIED entries (verification status: "✓ confirmed").
2. If verification is "~ single source" or "✗ unverified", mark as `[CITATION NEEDED]` in the text and do NOT add to .bib.
3. BibTeX entry format:
   ```bibtex
   @article{key2024,
     author    = {Author, First and Author, Second},
     title     = {Paper Title},
     journal   = {Journal Name},
     volume    = {XX},
     number    = {X},
     pages     = {XXX--XXX},
     year      = {YYYY},
     publisher = {Publisher},
     doi       = {10.XXXX/XXXXX},
   }
   ```
4. Use consistent BibTeX keys: `firstauthorYYYYkeyword` (e.g., `he2016deep`).
5. Every paper in the .bib file must be cited in the text, and every citation in the text must have a corresponding .bib entry.

### Compilation Check

```bash
cd <output_dir>/english_manuscript/
pdflatex english_manuscript.tex
bibtex english_manuscript
pdflatex english_manuscript.tex
pdflatex english_manuscript.tex
```

Or use the compile script:

```bash
python scripts/compile_latex.py <output_dir>/english_manuscript/english_manuscript.tex --output-dir <output_dir>/english_manuscript/
```

---

## IEEE Word Filling Instructions

The Word template (`templates/ieee-word/template.docx`) is filled programmatically via `scripts/render_word.py`. The script requires a structured JSON input.

### JSON Input Structure

Create `<output_dir>/word_content.json` with this structure:

```json
{
  "title": "Paper Title",
  "authors": [
    {"name": "Author One", "affiliation": "Dept., University, City, Country", "email": "a@example.com"},
    {"name": "Author Two", "affiliation": "Dept., University, City, Country", "email": "b@example.com"}
  ],
  "abstract": "Abstract text...",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "sections": [
    {"heading": "Introduction", "level": 1, "content": "Paragraph text..."},
    {"heading": "Related Work", "level": 1, "content": ""},
    {"heading": "Theme A", "level": 2, "content": "Paragraph text..."},
    {"heading": "Proposed Method", "level": 1, "content": ""},
    {"heading": "Overview", "level": 2, "content": "Paragraph text..."},
    {"heading": "Module A", "level": 2, "content": "Paragraph text with equation: $E = mc^2$..."},
    {"heading": "Experiments", "level": 1, "content": ""},
    {"heading": "Conclusion", "level": 1, "content": "Paragraph text..."},
    {"heading": "Acknowledgment", "level": 1, "content": "Acknowledgment text..."}
  ],
  "references": [
    "[1] Author et al., \"Title,\" Journal, vol. X, pp. X-Y, YYYY.",
    "[2] ..."
  ],
  "figures": [
    {"caption": "Fig. 1. Figure caption.", "image_path": "fig1.png", "width_inches": 3.5}
  ],
  "tables": [
    {
      "caption": "TABLE I. Table caption.",
      "header": ["Method", "Metric1", "Metric2"],
      "rows": [
        ["Method A", "0.95", "0.87"],
        ["Ours", "0.98", "0.92"]
      ]
    }
  ]
}
```

### Running the Script

```bash
python scripts/render_word.py <output_dir>/word_content.json \
    --template templates/ieee-word/template.docx \
    --output <output_dir>/english_manuscript.docx
```

### Content Preprocessing for Word

Before feeding to the script:
1. Extract section content from `08_english_polished.md`.
2. Convert Markdown formatting to Word-compatible structures:
   - `**bold**` → bold style
   - `*italic*` → italic style
   - Lists → Word bullet/numbered lists
   - `$...$` inline math → leave as-is (rendered by Word equation editor or plain text)
3. Resolve all `AUTHOR_INPUT_NEEDED` and `[CITATION NEEDED]` markers before rendering.
4. Tables: Convert Markdown tables to the JSON table structure.
5. Figures: Reference image files by path (copy to output directory first).

---

---

## Cover Letter Filling Rules

### Purpose

A cover letter accompanies the manuscript submission. It is addressed to the Editor-in-Chief and concisely explains why the paper merits publication in the target journal. The cover letter must use formal academic register and avoid overclaims.

### Content Structure

| Para | Content | Source |
|------|---------|--------|
| 1 | Submission statement: manuscript title, journal name, statement of exclusive submission | Stage 0: Target venue; Stage 4e: Final title |
| 2 | Background (2-3 sentences) + Main contributions (3-4 bullets) | Stage 1: Project brief; Stage 4e: Contribution bullets |
| 3 | Key findings (2-3 sentences with specific numbers) | Stage 4e: Abstract; Stage 3: Improvement summary |
| 4 | Why this journal (2-3 reasons: topic fit, audience, recent related papers) | Stage 2: Literature matrix; author's journal knowledge |
| 5 | Declarations: all authors approved, no conflicts, funding, data/code availability | Stage 0: Author-provided info |

### Writing Rules

**Tone & Register:**
- Formal but not obsequious. Do not use "we are honored", "we humbly submit", or "esteemed journal".
- Confident but not grandiose. Do not use "groundbreaking", "revolutionary", or "paradigm-shifting".
- Specific: every claim about the paper's contribution must be traceable to evidence in the manuscript.

**Length:** Maximum 1 page (400-500 words).

**Overclaim Prevention (critical for cover letters):**
- Never claim "this is the first" — the editor may know of earlier work.
- Never claim the paper "solves" a problem — use "addresses", "advances", "makes progress on".
- Never guarantee impact — state what was done and found, not its historical significance.
- All overclaim rules from `forbidden-overclaims.md` apply doubly to cover letters.

**Content Boundaries:**
- DO write: short, specific statements about the paper's contribution and findings.
- Do NOT write: a mini-abstract, a full literature review, or long method descriptions.
- Do NOT copy-paste from the manuscript abstract — the cover letter should use fresh phrasing.

### LaTeX Output

1. Copy `templates/cover-letter/` to `<output_dir>/cover_letter/`.
2. Fill `cover_letter.tex`:
   - Sender block: corresponding author name, affiliation, address, email, phone.
   - Recipient: Editor-in-Chief, journal name.
   - Date: `\today` or specific date.
   - Title: exact manuscript title (must match main manuscript).
   - Para 1: submission statement.
   - Para 2: background + contributions (bulleted list).
   - Para 3: key findings with specific numbers.
   - Para 4: why this journal.
   - Para 5: declarations (authorship, conflicts, funding, data/code).
   - Closing: "Sincerely," + corresponding author name.
3. Optional: Suggested/opposed reviewers (comment in/out as needed).
4. Compile check: `pdflatex cover_letter.tex`

### Word Output (via JSON)

Create `<output_dir>/cover_letter_content.json`:

```json
{
  "title": "Submission of manuscript: Paper Title",
  "output_type": "cover_letter",
  "authors": [
    {"name": "Corresponding Author", "affiliation": "Dept., University, City, Country", "email": "author@university.edu", "phone": "+X-XXX-XXX-XXXX"}
  ],
  "recipient": {
    "role": "Editor-in-Chief",
    "journal": "Journal Name"
  },
  "sections": [
    {"heading": "", "level": 1, "content": "We wish to submit our manuscript entitled \"Paper Title\" for consideration for publication in Journal Name. This manuscript has not been published elsewhere and is not under consideration by any other journal."},
    {"heading": "Background and Contributions", "level": 2, "content": "Background paragraph text...\\n\\nMain Contributions:\\n\\u2022 Contribution 1\\n\\u2022 Contribution 2\\n\\u2022 Contribution 3"},
    {"heading": "Key Findings", "level": 2, "content": "Key findings paragraph with specific numbers..."},
    {"heading": "Fit for Journal Name", "level": 2, "content": "Why this journal paragraph..."},
    {"heading": "Declarations", "level": 2, "content": "\\u2022 All authors have read and approved the final manuscript.\\n\\u2022 The authors declare no conflicts of interest.\\n\\u2022 Funding: ..."}
  ],
  "references": []
}
```

Run:
```bash
python scripts/render_word.py <output_dir>/cover_letter_content.json \
    --template templates/ieee-word/template.docx \
    --output <output_dir>/cover_letter.docx
```

### Cover Letter Output Files

```
<output_dir>/
├── cover_letter/
│   └── cover_letter.tex
├── cover_letter_content.json
└── cover_letter.docx
```

---

## Output Directory Structure (After Stage 4g)

```
<output_dir>/
├── project-state.md
├── 05_chinese_draft.md
├── 06_chinese_polished.md
├── 07_english_draft.md
├── 08_english_polished.md
├── 09_revision_notes.md
├── 10_critique_report.md
├── 10a_auto_check.md
├── word_content.json                    (intermediate JSON for Word)
├── english_manuscript.docx              (final Word output)
├── cover_letter_content.json            (intermediate JSON for cover letter)
├── cover_letter.docx                    (cover letter Word output)
├── cover_letter/
│   └── cover_letter.tex                 (cover letter LaTeX output)
├── chinese_manuscript/
│   ├── chinese_manuscript.tex
│   ├── cjc.cls
│   ├── cjc.bst
│   ├── references.bib
│   └── figures/                         (copied figure files)
└── english_manuscript/
    ├── english_manuscript.tex
    ├── IEEEtran.cls
    ├── IEEEtran.bst
    ├── references.bib
    └── figures/                         (copied figure files)
```

---

## Cross-Template Consistency Checks

Before finalizing, verify across all output files:

1. **Title matches**: Chinese LaTeX `title*` == IEEE LaTeX `\title{}` == Word title == cover letter title.
2. **Author list matches**: Same authors, same order, same affiliations. Cover letter uses corresponding author.
3. **Abstract matches**: Chinese LaTeX `abstract*` == IEEE LaTeX abstract == Word abstract. Cover letter should NOT copy-paste the abstract.
4. **Numbers match**: Every metric value in Chinese LaTeX == IEEE LaTeX == Word. Cover letter key findings must use the same numbers.
5. **Citation count matches**: Same number of references in all three manuscript outputs.
6. **Claim consistency**: Cover letter claims must not exceed claims in the manuscript. The manuscript is the authoritative source.
7. **No `AUTHOR_INPUT_NEEDED` or `[CITATION NEEDED]`** in final outputs — these should be resolved before rendering.

If discrepancies are found, document them in `09_revision_notes.md` and fix before declaring the pipeline complete.
