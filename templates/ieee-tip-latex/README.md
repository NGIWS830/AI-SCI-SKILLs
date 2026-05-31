# IEEE TIP (Transactions on Image Processing) LaTeX Template

## About IEEE TIP

- **Full Name:** IEEE Transactions on Image Processing
- **Publisher:** IEEE Signal Processing Society
- **ISSN:** 1057-7149
- **Impact Factor:** ~10.6 (2024 JCR)
- **Frequency:** Monthly (continuous publication)
- **Scope:** Image and video processing, computer vision, image/video coding, restoration, enhancement, analysis, and understanding

## Setup

1. Copy `IEEEtran.cls` and `IEEEtran.bst` from `templates/ieee-latex/` into this directory
2. Compile:
   ```bash
   pdflatex template.tex
   bibtex template
   pdflatex template.tex
   pdflatex template.tex
   ```

## TIP Scope

### What TIP Publishes
- **Image/video restoration**: denoising, deblurring, super-resolution, inpainting, deraining, dehazing
- **Image/video compression**: learned compression, neural codecs, perceptual compression
- **Image/video enhancement**: HDR, color correction, exposure correction, low-light enhancement
- **Image/video analysis**: segmentation, detection, tracking, recognition
- **Image/video quality assessment**: full-reference, no-reference, perceptual metrics
- **Computational imaging**: inverse problems, compressed sensing, tomography
- **Medical/biomedical imaging**: CT, MRI, ultrasound, microscopy image processing
- **Theory**: sampling theory, sparse representation, variational methods, optimization for imaging

### TIP vs CVPR/ICCV vs TPAMI
| Venue | Type | Review | Length | Expectation |
|-------|------|--------|--------|-------------|
| **TIP** | Journal | Single-blind | 12-18 pages | Thorough, reproducible, well-validated |
| CVPR/ICCV | Conference | Double-blind | 8 pages | Novel, exciting, timely |
| TPAMI | Journal | Single-blind | 14-20+ pages | Major theoretical + empirical contribution |

TIP is the premier journal venue for image processing. It values depth over novelty — a TIP paper should be the definitive treatment of its topic.

## Key Requirements

### Image Processing Rigor
- **Mathematical formulation**: Every image processing operation should have a mathematical foundation. Use proper notation: $\mathbf{x}$ for clean image, $\mathbf{y}$ for degraded, $\hat{\mathbf{x}}$ for restored.
- **Degradation model**: For restoration tasks, clearly define the image formation / degradation model: $\mathbf{y} = \mathbf{H}\mathbf{x} + \mathbf{n}$.
- **Parameter justification**: Explain WHY each hyperparameter value was chosen. Grid search on validation set is acceptable.

### Standard Benchmarks
| Task | Standard Datasets |
|------|-------------------|
| Super-Resolution | DIV2K, Flickr2K, Set5, Set14, BSD100, Urban100, Manga109 |
| Denoising | BSD68, Set12, Kodak24, McMaster, DND, SIDD |
| Deblurring | GoPro, HIDE, RealBlur, REDS |
| Image Enhancement | LOL, MIT-Adobe FiveK, HDR+ |
| Quality Assessment | LIVE, TID2013, KADID-10k, PIPAL |

### Statistical Reporting
- Report **mean ± std** over multiple runs (minimum 3-5 seeds)
- For restoration tasks, report PSNR/SSIM on **standard test sets** with **standard evaluation protocols**
- Do NOT cherry-pick best results — report average across seeds
- Use proper image processing evaluation: convert to YCbCr and evaluate on Y channel (luminance) when standard in the field

### Visual Comparison
- Show zoomed-in **patches** (not full images) for fine-detail comparison
- Use consistent color mapping and scaling across all compared methods
- Include **error maps** (|prediction − ground truth|) to visualize reconstruction errors
- Show **both** best-case and worst-case examples

### Efficiency
- Report: #params (M), FLOPs (G), GPU memory (GB), inference time (ms)
- For video: report FPS
- TIP increasingly values efficient methods; state-of-the-art PSNR at any computational cost is no longer sufficient

## Common TIP Rejection Reasons
1. Insufficient comparison to classical (non-DL) image processing baselines (e.g., BM3D, WNNM)
2. Missing standard benchmarks for the task
3. No efficiency analysis (params, FLOPs, runtime)
4. Claims not supported by statistical evidence
5. Viewing image processing as pure deep learning without understanding the underlying signal processing
