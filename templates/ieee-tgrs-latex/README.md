# IEEE TGRS (Transactions on Geoscience and Remote Sensing) LaTeX Template

## About IEEE TGRS

- **Full Name:** IEEE Transactions on Geoscience and Remote Sensing
- **Publisher:** IEEE Geoscience and Remote Sensing Society (GRSS)
- **ISSN:** 0196-2892 (print), 1558-0644 (online)
- **Impact Factor:** ~8.2 (2024 JCR)
- **Frequency:** Monthly
- **Scope:** Remote sensing of land, oceans, atmosphere, and space; processing, interpretation, and analysis of remotely sensed data

## Setup

1. Place `IEEEtran.cls` and `IEEEtran.bst` from your TeX distribution in this directory  
   (or copy from `templates/ieee-latex/` if already present in this project)
2. Compile:
   ```bash
   pdflatex template.tex
   bibtex template
   pdflatex template.tex
   pdflatex template.tex
   ```

## TGRS vs IEEE Conference Template

The existing `templates/ieee-latex/` is in **conference mode** (`\documentclass[conference]{IEEEtran}`).  
This TGRS template uses **journal mode** (`\documentclass[journal]{IEEEtran}`).

| Feature | Conference (IEEE) | Journal (TGRS) |
|---------|------------------|-----------------|
| Document class | `[conference]` | `[journal]` |
| Page limit | 6-8 pages | No strict limit (typically 12-18) |
| Abstract length | ~200 words | ~200-300 words |
| Related Work | 1-2 pages, brief | 3-5 pages, comprehensive |
| Discussion section | Not required | Strongly recommended |
| References | 20-40 | 40-80 |
| Appendices | Not typical | Common (derivations, extra experiments) |
| Submission | Anonymous for review | Not anonymous (TGRS is single-blind) |

## TGRS-Specific Requirements

### Geoscience Context
- Always specify the **sensor/platform** (Sentinel-2, Landsat-8, Gaofen-2, WorldView-3, etc.) and its key parameters (spatial resolution, spectral bands, revisit time).
- Include a **study area description** with geographic coordinates and rationale for site selection.
- Use proper terminology: GSD (Ground Sampling Distance), IFOV, radiance vs reflectance, atmospheric correction, etc.

### Data Statement
- State the source of satellite/airborne data (ESA Copernicus, NASA EarthData, USGS EarthExplorer, etc.)
- Mention data access policies (open access or restricted)
- Cite dataset DOIs where available

### Mathematical Notation
- Use `\mathbf` for matrices, `\mathcal` for loss functions
- Clearly distinguish between spectral bands (typically B), spatial dimensions (H×W), and temporal dimension (T)
- For multi/hyperspectral data: specify the number of bands as N_λ (or B for multispectral)

### Reproducibility
- TGRS strongly encourages code release (GitHub repository)
- Specify training/validation/test split methodology (spatial split vs random split — spatial is preferred to avoid spatial autocorrelation)
- Report hardware specifications (GPU model, CUDA version)

## Key TGRS Conferences & Journals to Reference

| Abbreviation | Full Name | Type |
|-------------|-----------|------|
| TGRS | IEEE Trans. Geosci. Remote Sens. | Journal (this template) |
| GRSL | IEEE Geosci. Remote Sens. Lett. | Letters journal |
| JSTARS | IEEE J. Sel. Topics Appl. Earth Observ. Remote Sens. | Journal |
| RSE | Remote Sensing of Environment (Elsevier) | Journal |
| ISPRS J. | ISPRS J. Photogramm. Remote Sens. (Elsevier) | Journal |
| IGARSS | IEEE Int. Geosci. Remote Sens. Symp. | Conference |
| WHISPERS | Workshop on Hyperspectral Image and Signal Processing | Workshop |

## Documentclass Options

During writing, use `draftcls` for faster compilation:
```latex
\documentclass[journal,onecolumn,draftcls]{IEEEtran}
```

For final submission, switch to:
```latex
\documentclass[journal]{IEEEtran}
```

Remove the `draftcls,onecolumn` options — TGRS uses two-column format in final version.
