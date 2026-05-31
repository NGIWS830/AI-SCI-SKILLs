#!/usr/bin/env python3
"""Automated quality checks on generated paper artifacts.

Usage:
    python check_quality.py <output_dir> --checks claims,citations,language
    python check_quality.py <output_dir> --all --output quality_report.md
"""

import argparse
import os
import re
import sys
from collections import Counter


# ── Check Functions ─────────────────────────────────────────────────────────────

def check_claims(text, state_text=""):
    """Check that claims are backed by evidence."""
    issues = []

    # Count claim-like statements
    claim_patterns = [
        (r'\b(significantly|substantially|dramatically)\s+improves?\b',
         "Strong claim word used: '{}'. Verify evidence strength supports this wording."),
        (r'\b(state-of-the-art|state of the art|SOTA)\b',
         "SOTA claim detected: '{}'. Must be supported by explicit SOTA comparison with statistical test."),
        (r'\bproves?\b',
         "'Prove' claim: '{}'. Use 'demonstrates', 'suggests', or 'provides evidence that' unless formal proof exists."),
        (r'\bfirst\b.*\b(propos|introduc|present)\b',
         "'First to propose' claim: '{}'. Nearly impossible to verify objectively."),
        (r'\bnovel\b',
         "'Novel': '{}'. Consider removing — let the contribution speak for itself."),
        (r'\buniversally\b',
         "'Universally': '{}'. Unless tested on a representative sample of all possible scenarios, avoid."),
        (r'\boptimal\b',
         "'Optimal': '{}'. Requires formal optimality proof or exhaustive search."),
        (r'\brobust across all\b',
         "'Robust across all': '{}'. Specify which conditions were tested."),
    ]

    found_claims = []
    for pattern, msg_template in claim_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            word = match.group(1) if match.lastindex else match.group(0)
            found_claims.append({
                "type": "overclaim_risk",
                "word": word,
                "message": msg_template.format(word),
            })

    # Check for evidence anchoring
    numbers_in_prose = re.findall(r'\b(\d+\.?\d*)\s*(%|percent|points|ms|seconds)\b', text)
    section_refs = re.findall(r'(Table|Figure|Fig\.?|Section)\s+[IVX\d]+', text)

    if numbers_in_prose and not section_refs:
        issues.append({
            "type": "weak_anchoring",
            "message": f"Found {len(numbers_in_prose)} numerical claims but no table/figure/section references.",
        })

    issues.extend(found_claims)
    return issues


def check_citations(text, state_text=""):
    """Check citation completeness and markers."""
    issues = []

    # Count [CITATION NEEDED] markers
    citation_needed = list(re.finditer(r'\[CITATION\s+NEEDED\]', text))
    if citation_needed:
        issues.append({
            "type": "citation_gap",
            "severity": "high",
            "message": f"Found {len(citation_needed)} [CITATION NEEDED] markers. Sections: " +
                       ", ".join(sorted(set(
                           _find_section(text, m.start()) for m in citation_needed
                       ))),
        })

    if len(citation_needed) > 3:
        issues.append({
            "type": "citation_gap",
            "severity": "critical",
            "message": f"Too many [CITATION NEEDED] markers ({len(citation_needed)}). Manuscript not ready.",
        })

    # Count AUTHOR_INPUT_NEEDED markers
    author_needed = list(re.finditer(r'AUTHOR_INPUT_NEEDED', text))
    if author_needed:
        issues.append({
            "type": "missing_input",
            "severity": "medium",
            "message": f"Found {len(author_needed)} AUTHOR_INPUT_NEEDED markers.",
        })

    # Check citation density per section
    sections = _split_sections(text)
    for section_name, section_text in sections.items():
        cites = len(re.findall(r'\[(\d+|[A-Z][a-z]+ et al\.)\]', section_text))
        if section_name in ["Introduction", "Related Work"] and cites < 3:
            issues.append({
                "type": "sparse_citations",
                "message": f"Section '{section_name}' has only {cites} citations. Consider adding more literature context.",
            })

    return issues


def check_reproducibility(text, state_text=""):
    """Check that experiments are reproducible."""
    issues = []

    # Implementation details checklist
    impl_checks = [
        (r'optimizer|Adam|SGD|AdamW', "Optimizer specified"),
        (r'learning rate|lr\s*=', "Learning rate specified"),
        (r'batch\s*size', "Batch size specified"),
        (r'epochs?', "Number of epochs specified"),
        (r'GPU|A100|V100|RTX|TPU', "Hardware specified"),
        (r'seed', "Random seed specified"),
    ]

    found = []
    missing = []
    for pattern, label in impl_checks:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(label)
        else:
            missing.append(label)

    if missing:
        issues.append({
            "type": "reproducibility",
            "severity": "medium",
            "message": f"Missing implementation details: {', '.join(missing)}",
        })

    issues.append({
        "type": "reproducibility",
        "severity": "info",
        "message": f"Found details: {', '.join(found)}. Missing: {', '.join(missing) if missing else 'none'}",
    })

    # Check for standard deviations
    if not re.search(r'(\d+\.\d+\s*[±+-]\s*\d+\.\d+)', text):
        issues.append({
            "type": "reproducibility",
            "severity": "medium",
            "message": "No standard deviations detected in results. Consider reporting variance across runs.",
        })

    return issues


def check_language(text, state_text=""):
    """Check language quality heuristics."""
    issues = []

    # Sentence starter variety
    we_starts = re.findall(r'^(We\s)', text, re.MULTILINE)
    consecutive_we = 0
    max_consecutive = 0
    for line in text.split('\n'):
        if re.match(r'^\s*We\s', line):
            consecutive_we += 1
            max_consecutive = max(max_consecutive, consecutive_we)
        else:
            consecutive_we = 0

    if max_consecutive > 3:
        issues.append({
            "type": "style",
            "severity": "low",
            "message": f"Found {max_consecutive} consecutive sentences starting with 'We'. Vary sentence openers.",
        })

    # Check for informal words
    informal_checks = [
        (r'\ba lot of\b', "Replace with 'many', 'substantial', or a specific number"),
        (r'\bkind of\b', "Remove or replace with 'type of'"),
        (r'\b(a )?big\b', "Replace with 'large', 'substantial', or 'considerable'"),
        (r'\bget\b', "Consider 'obtain' or 'achieve'"),
        (r'\blook(ing|s|ed)? at\b', "Consider 'examine', 'investigate', or 'analyze'"),
    ]
    for pattern, suggestion in informal_checks:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            issues.append({
                "type": "informal_language",
                "severity": "low",
                "message": f"'{matches[0].group(0)}' — {suggestion} (found {len(matches)} occurrences)",
            })

    return issues


def check_structure(text, state_text=""):
    """Check manuscript structure."""
    issues = []

    # Check required sections
    required_sections = ["Abstract", "Introduction", "Related Work", "Proposed Method", "Experiments", "Conclusion"]
    for section in required_sections:
        if not re.search(rf'#+\s+.*{section}', text, re.IGNORECASE):
            # Also check Chinese section names
            cn_map = {
                "Abstract": "摘要",
                "Introduction": "引言|绪论",
                "Related Work": "相关工作",
                "Proposed Method": ".*方法|本文方法",
                "Experiments": "实验",
                "Conclusion": "结论|总结",
            }
            cn_pattern = cn_map.get(section, "")
            if not cn_pattern or not re.search(cn_pattern, text):
                issues.append({
                    "type": "structure",
                    "severity": "high",
                    "message": f"Required section '{section}' not found.",
                })

    # Check figure/table references are sequential
    fig_refs = [int(m.group(1)) for m in re.finditer(r'Fig(?:ure)?\.?\s*(\d+)', text)]
    if fig_refs and fig_refs != sorted(set(fig_refs)):
        issues.append({
            "type": "structure",
            "severity": "low",
            "message": "Figure references may not be sequential or have gaps.",
        })

    return issues


def check_overclaims_cn(text, state_text=""):
    """Check Chinese text for overclaim/夸大 words."""
    issues = []

    # Absolute claims in Chinese
    cn_absolute = [
        (r'完美(?!匹配|对齐)', "禁止使用'完美'。替代：有效 / 可行 / 取得了良好效果。"),
        (r'完全解决|彻底解决|根本解决', "禁止使用'解决'类绝对词。替代：缓解 / 改善 / 在一定程度上处理了。"),
        (r'彻底消除|根本消除', "禁止使用'彻底消除'。替代：有效抑制 / 显著降低。"),
        (r'最优|最佳(?!化)', "限定比较范围。替代：在[数据集]上取得了最佳性能 / 在所列方法中表现最好。"),
        (r'首次提出|首次实现|第一次', "禁止使用'首次'。虽然可能是事实，但几乎无法客观验证。替换：提出了 / 实现了。"),
        (r'颠覆性|革命性', "禁止使用'颠覆性'/'革命性'。让历史评判。替代：提出了一种新思路 / 从[视角]探索了。"),
        (r'史无前例', "禁止使用'史无前例'。替代：与现有方法不同，该方法..."),
        (r'证明了(?!.*定理|.*引理)', "禁止使用'证明了'（非数学语境）。替代：表明 / 实验结果表明 / 为...提供了证据。"),
        (r'普遍适用|通用(?!.*近似|.*函数)', "禁止使用'普遍适用'/'通用'。替代：在[N]个数据集上得到了验证。"),
        (r'鲁棒性极强|鲁棒性非常好|非常鲁棒', "量化为具体数值。替代：在[条件下]性能波动小于[X]%。"),
    ]

    for pattern, message in cn_absolute:
        for match in re.finditer(pattern, text):
            issues.append({
                "type": "overclaim_cn",
                "severity": "high",
                "word": match.group(0),
                "message": f"'{match.group(0)}' — {message}",
            })

    # Exaggerated magnitude in Chinese
    cn_magnitude = [
        (r'大幅提升|大幅度提高|大幅降低', "用具体数值替代：提升了[X]个百分点 / 从[A]降至[B]。"),
        (r'显著改善|显著提高|显著增强|显著降低', "用具体数值替代：在[数据集]上从[X]变为[Y]。"),
        (r'极大地|极大改善|极大提升', "删除'极大'或替换为具体数值。"),
        (r'性能远超|远远超过|远超', "替换为具体比较：性能优于[基线名称]（+[X]个百分点）。"),
        (r'(实现了|取得)(了)?惊人的|令人印象深刻的', "删除形容词，直接报告数值。"),
        (r'极低(的)?计算开销|极低(的)?成本', "量化：仅增加[X]%参数量 / [Y]ms延迟。"),
    ]

    for pattern, message in cn_magnitude:
        for match in re.finditer(pattern, text):
            issues.append({
                "type": "overclaim_cn",
                "severity": "medium",
                "word": match.group(0),
                "message": f"'{match.group(0)}' — {message}",
            })

    # Vague generalizations in Chinese
    cn_vague = [
        (r'在所有数据集上均优于', "限定具体范围：在[列出的N个数据集]上均优于。"),
        (r'具有(良好的|很强的)?泛化能力', "具体化：在[域外数据集X]上达到了[Y]（域内为[Z]）。"),
        (r'可以广泛应用(于)?', "说明已测试的具体场景。"),
        (r'具有重要的理论意义和实际应用价值', "删除空话，或用具体应用场景替代。"),
        (r'达到了国际先进水平', "具体化：在[基准]上与[SOTA方法]性能相当（[具体值]）。"),
    ]

    for pattern, message in cn_vague:
        for match in re.finditer(pattern, text):
            issues.append({
                "type": "overclaim_cn",
                "severity": "medium",
                "word": match.group(0),
                "message": f"'{match.group(0)}' — {message}",
            })

    # Redundant emphasis words in Chinese
    cn_redundant = [
        (r'非常(?!重要)', "冗余强调词。删除或用具体数值替代。"),
        (r'十分|极其|极为', "冗余强调词。删除。"),
        (r'毫无(疑问|疑义)', "如确无疑，说明原因；否则是夸大。"),
        (r'显而易见|显然(?!，)', "如果真显然，不需要说。删除。"),
        (r'众所周知', "如果真众所周知，引用文献；否则是撒谎。"),
        (r'毋庸置疑|不容置疑', "科学中一切都可质疑。删除。"),
        (r'必须指出|特别强调|值得一提的是|值得注意的是', "删除引导语，直接陈述。"),
    ]

    for pattern, message in cn_redundant:
        for match in re.finditer(pattern, text):
            issues.append({
                "type": "overclaim_cn",
                "severity": "low",
                "word": match.group(0),
                "message": f"'{match.group(0)}' — {message}",
            })

    return issues


def check_dedup(text, state_text=""):
    """Check for duplicated content across sections."""
    issues = []

    sections = _split_sections(text)
    if len(sections) < 2:
        return issues

    # Check for near-identical sentences across sections
    section_sentences = {}
    for section_name, section_text in sections.items():
        if section_name == "Preamble":
            continue
        sentences = [s.strip() for s in re.split(r'[.。]', section_text) if len(s.strip()) > 20]
        section_sentences[section_name] = sentences

    seen_sentences = {}  # normalized_sentence -> (section, original)
    for section_name, sentences in section_sentences.items():
        for sent in sentences:
            normalized = re.sub(r'\s+', '', sent.lower())[:60]
            if normalized in seen_sentences:
                prev_section, prev_sent = seen_sentences[normalized]
                issues.append({
                    "type": "dedup",
                    "severity": "medium",
                    "message": f"Near-duplicate sentence: '{prev_sent[:60]}...' in [{prev_section}] and [{section_name}]",
                })
            else:
                seen_sentences[normalized] = (section_name, sent)

    # Check for method-description leaking into Introduction
    method_keywords = [r'具体而言.*模块', r'由.*个.*组成', r'结构如图\s*\d', r'如图\s*\d\s*所示.*架构']
    intro_text = sections.get("Introduction", "") + sections.get("引言", "")
    method_text = sections.get("Proposed Method", "") + sections.get("方法", "")

    for kw_pattern in method_keywords:
        intro_matches = list(re.finditer(kw_pattern, intro_text))
        method_matches = list(re.finditer(kw_pattern, method_text))
        if intro_matches and method_matches:
            issues.append({
                "type": "dedup",
                "severity": "medium",
                "message": f"Possible method detail in Introduction: '{kw_pattern}' found in both Introduction and Method.",
            })

    # Check for result numbers appearing in too many sections
    result_pattern = re.compile(r'(\d+\.?\d*)\s*%')
    results_by_section = {}
    for section_name, section_text in sections.items():
        numbers = result_pattern.findall(section_text)
        if numbers:
            results_by_section[section_name] = len(numbers)

    for section_name, count in results_by_section.items():
        if count > 15 and section_name not in ["Experiments", "实验"]:
            issues.append({
                "type": "dedup",
                "severity": "low",
                "message": f"Section '{section_name}' contains {count} numerical percentages — possible result duplication from Experiments.",
            })

    return issues


def check_aiflavor(text, state_text=""):
    """Check for AI-generated language patterns (both CN and EN)."""
    issues = []

    # ── English AI-flavor patterns ──

    # Generic openers
    en_openers = [
        (r'In recent years,?\s+there has been (growing|increasing) interest in',
         "AI-flavor opener. Replace with concrete problem statement."),
        (r'With the rapid development of\b',
         "AI-flavor opener. Name the specific development relevant to this work."),
        (r'The field of\s+\w+\s+has witnessed (remarkable|significant) progress',
         "AI-flavor opener. Cite specific breakthroughs instead."),
        (r'In the era of\b',
         "AI-flavor cliché. Delete; start with problem."),
        (r'It is widely recognized that\b',
         "AI-flavor hedge. Cite evidence or delete."),
        (r'To the best of our knowledge,?\s+',
         "Overused hedge. Use at most once; delete other occurrences."),
    ]

    for pattern, message in en_openers:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            issues.append({
                "type": "aiflavor",
                "severity": "medium",
                "message": f"'{match.group(0)[:60]}' — {message}",
            })

    # Overused connectors (count-based, not just presence)
    en_connectors = {
        "Moreover": r'\bMoreover\b',
        "Furthermore": r'\bFurthermore\b',
        "In addition": r'\bIn addition\b',
        "It is worth noting": r'\bIt is worth noting\b',
        "Notably": r'\bNotably\b',
        "Importantly": r'\bImportantly\b',
    }
    for word, pattern in en_connectors.items():
        count = len(re.findall(pattern, text, re.IGNORECASE))
        if count > 3:
            issues.append({
                "type": "aiflavor",
                "severity": "low",
                "message": f"'{word}' used {count} times — overused connector. Reduce to <=2 or restructure.",
            })

    # Hollow adjectives
    en_hollow = [
        (r'a powerful framework\b', "Hollow adjective. Replace with specific capability or metric."),
        (r'an effective approach\b', "Hollow adjective. State what makes it effective with evidence."),
        (r'a promising direction\b', "Hollow adjective. Describe the specific potential."),
        (r'comprehensive experiments?\b', "State the scope concretely: N datasets, M baselines."),
        (r'extensive evaluation\b', "Use concrete description instead: 'evaluation across [conditions]'."),
        (r'a novel architecture\b', "Let the architecture speak for itself. Drop 'novel'."),
    ]

    for pattern, message in en_hollow:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            issues.append({
                "type": "aiflavor",
                "severity": "low",
                "message": f"'{match.group(0)}' — {message}",
            })

    # Formulaic concluding sentences
    en_concluding = [
        (r'These results demonstrate the effectiveness of our (proposed )?(approach|method)\.?\s*$',
         "Formulaic concluding sentence. Delete — let results speak for themselves."),
        (r'This highlights the importance of\b',
         "Delete or be specific about what was learned."),
        (r'These findings provide valuable insights into\b',
         "Be specific or delete."),
        (r'Our work opens up several (new )?avenues for (future )?research\.?\s*$',
         "List the specific future directions, or delete."),
    ]

    for pattern, message in en_concluding:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            issues.append({
                "type": "aiflavor",
                "severity": "low",
                "message": f"'{match.group(0)[:70]}' — {message}",
            })

    # ── Chinese AI-flavor patterns ──

    cn_openers = [
        (r'近年来，?随着.*?(的)?(飞速|快速|迅速|不断)发展',
         "AI套话开头。删除，直接描述具体问题和应用场景。"),
        (r'随着人工智能技术的不断进步',
         "AI套话开头。空洞无信息。引用与本工作直接相关的具体进展。"),
        (r'在当今.*?时代',
         "AI陈词滥调。删除，直接切入问题。"),
        (r'近年来，?\w+领域取得了长足的进步',
         "AI套话开头。引用2-3个里程碑工作并说明具体进展。"),
    ]

    for pattern, message in cn_openers:
        for match in re.finditer(pattern, text):
            issues.append({
                "type": "aiflavor",
                "severity": "medium",
                "message": f"'{match.group(0)[:60]}' — {message}",
            })

    # Chinese overused connectors
    cn_connectors = {
        "值得注意的是": r'值得注意的是',
        "值得一提的是": r'值得一提的是',
        "此外": r'\b此外\b',
    }
    for word, pattern in cn_connectors.items():
        count = len(re.findall(pattern, text))
        if count > 3:
            issues.append({
                "type": "aiflavor",
                "severity": "low",
                "message": f"'{word}' 使用了 {count} 次 — 过度使用连接词。减少至≤2次或重组结构。",
            })

    # Chinese formulaic conclusions
    cn_concluding = [
        (r'综上所述，本文提出的方法有效(地)?(解决|处理)了',
         "公式化总结。具体重述方法做了什么，实验证明了什么。"),
        (r'实验结果表明，我们的方法具有(良好的|优秀的)?性能',
         "空洞总结。报告具体指标：在[数据集]上达到[值]，优于[基线]。"),
        (r'未来的工作将围绕以下.*?展开',
         "泛泛的未来工作。列出1-2个具体可执行的方向，或不写。"),
        (r'本文的研究为相关领域提供了新的思路',
         "空话。删除或用具体贡献替代。"),
    ]

    for pattern, message in cn_concluding:
        for match in re.finditer(pattern, text):
            issues.append({
                "type": "aiflavor",
                "severity": "low",
                "message": f"'{match.group(0)[:60]}' — {message}",
            })

    # Chinese hollow modifiers
    cn_hollow = [
        (r'强大的性能', "空洞修饰。替换为：在[数据集]上达到了[X]（具体数值）。"),
        (r'有效的方法', "空洞修饰。替换为：使[指标]提升了[Y]的方法。"),
        (r'充分的实验', "空洞修饰。替换为：在[N]个数据集上与[M]个基线进行了对比实验。"),
        (r'良好的效果', "空洞修饰。替换为：[指标]从[A]提升至[B]。"),
        (r'较为优秀', "空洞修饰。替换为：在所列方法中排名第[K]。"),
        (r'令人满意的结果', "空洞修饰。删除，直接报告结果。"),
        (r'达到(了)?国际先进水平', "空洞修饰。替换为：在[基准]上的性能[具体值]，与[SOTA方法]相当。"),
    ]

    for pattern, message in cn_hollow:
        for match in re.finditer(pattern, text):
            issues.append({
                "type": "aiflavor",
                "severity": "low",
                "message": f"'{match.group(0)}' — {message}",
            })

    return issues


def check_terminology(text, state_text=""):
    """Check terminology consistency."""
    issues = []

    # Common inconsistent pairs (Chinese)
    cn_pairs = [
        (r'注意力机制|Attention机制|attention机制', "注意力机制"),
        (r'骨干网络|主干网络|backbone网络', "骨干网络"),
        (r'特征提取器|特征提取网络', "特征提取器"),
        (r'消融实验|消融研究|ablation study', "消融实验"),
    ]
    for pattern, expected in cn_pairs:
        variants = set()
        for m in re.finditer(pattern, text, re.IGNORECASE):
            variants.add(m.group(0))
        if len(variants) > 1:
            issues.append({
                "type": "terminology",
                "severity": "medium",
                "message": f"Inconsistent terms: {variants}. Use '{expected}' consistently.",
            })

    return issues


# ── Helpers ─────────────────────────────────────────────────────────────────────

def _find_section(text, pos):
    """Find the section name containing position pos."""
    sections = list(re.finditer(r'^(#{1,4})\s+(.+)$', text[:pos], re.MULTILINE))
    if sections:
        return sections[-1].group(2).strip()[:40]
    return "(unknown)"


def _split_sections(text):
    """Split text into sections."""
    sections = {}
    current_section = "Preamble"
    current_text = []

    for line in text.split('\n'):
        if re.match(r'^#{1,4}\s+', line):
            if current_text:
                sections[current_section] = '\n'.join(current_text)
            current_section = re.sub(r'^#+\s+', '', line).strip()[:50]
            current_text = []
        else:
            current_text.append(line)

    if current_text:
        sections[current_section] = '\n'.join(current_text)

    return sections


def _read_artifacts(output_dir):
    """Read all generated manuscript files from output directory."""
    text = ""
    state_text = ""

    files_to_check = [
        "08_english_polished.md",
        "07_english_draft.md",
        "05_chinese_draft.md",
        "06_chinese_polished.md",
    ]

    for fname in files_to_check:
        fpath = os.path.join(output_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                text += f.read() + "\n"

    state_path = os.path.join(output_dir, "project-state.md")
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            state_text = f.read()

    return text, state_text


# ── CLI ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Automated quality checks on paper artifacts")
    parser.add_argument("output_dir", help="Directory containing generated paper files")
    parser.add_argument("--checks", default="all",
                        help="Comma-separated checks: claims,citations,reproducibility,language,structure,terminology,all")
    parser.add_argument("--output", "-o", help="Output report path")
    args = parser.parse_args()

    # Read artifacts
    text, state_text = _read_artifacts(args.output_dir)

    if not text.strip():
        print(f"Warning: No manuscript files found in {args.output_dir}", file=sys.stderr)
        # Still run checks — they'll report missing sections

    # Determine which checks to run
    if args.checks == "all":
        checks_to_run = ["claims", "citations", "reproducibility", "language", "structure", "terminology",
                         "overclaims_cn", "dedup", "aiflavor"]
    else:
        checks_to_run = [c.strip() for c in args.checks.split(",")]

    CHECK_MAP = {
        "claims": ("Claims-Evidence Alignment", check_claims),
        "citations": ("Citation Completeness", check_citations),
        "reproducibility": ("Reproducibility", check_reproducibility),
        "language": ("Language Quality", check_language),
        "structure": ("Structure", check_structure),
        "terminology": ("Terminology Consistency", check_terminology),
        "overclaims_cn": ("Chinese Overclaims", check_overclaims_cn),
        "dedup": ("Content Deduplication", check_dedup),
        "aiflavor": ("AI-Flavor Language", check_aiflavor),
    }

    all_issues = {}
    total_issues = 0
    critical_count = 0

    for check_name in checks_to_run:
        if check_name not in CHECK_MAP:
            continue
        label, fn = CHECK_MAP[check_name]
        issues = fn(text, state_text)
        all_issues[label] = issues
        total_issues += len(issues)
        for issue in issues:
            if issue.get("severity") == "critical":
                critical_count += 1

    # Build report
    report_lines = ["# Quality Check Report\n"]

    report_lines.append(f"**Artifacts directory:** `{args.output_dir}`\n")
    report_lines.append(f"**Checks run:** {', '.join(checks_to_run)}\n")
    report_lines.append(f"**Total issues found:** {total_issues}")
    if critical_count:
        report_lines.append(f"**Critical issues:** {critical_count} [!!!]\n")
    else:
        report_lines.append("")

    for label, issues in all_issues.items():
        report_lines.append(f"\n## {label}\n")
        if not issues:
            report_lines.append("✅ No issues found.\n")
        else:
            for issue in issues:
                severity = issue.get("severity", "info")
                icon = {"critical": "[!!]", "high": "[!]", "medium": "[-]", "low": "[.]", "info": "[i]"}.get(severity, "")
                report_lines.append(f"- {icon} [{severity}] {issue['message']}")

    # Summary
    report_lines.append(f"\n---\n")
    report_lines.append(f"### Summary\n")
    if critical_count > 0:
        report_lines.append(f"> [!!!] **{critical_count} critical issue(s)** must be resolved before submission.\n")
    elif total_issues > 5:
        report_lines.append(f"> **{total_issues} issues** found. Review and address as appropriate.\n")
    else:
        report_lines.append(f"> Only {total_issues} minor issue(s) found. The manuscript is in good shape.\n")

    report = "\n".join(report_lines)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        # Encode as ascii, replace unicode chars to avoid GBK errors on Windows
        try:
            print(report)
        except UnicodeEncodeError:
            print(report.encode('ascii', errors='replace').decode('ascii'))


if __name__ == "__main__":
    main()
