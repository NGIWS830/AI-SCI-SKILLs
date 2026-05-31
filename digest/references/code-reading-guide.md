# Code and Material Reading Guide

## Priority files

Inspect these first when available:

- `README.md`, `requirements.txt`, `environment.yml`, `pyproject.toml`
- `train.py`, `main.py`, `test.py`, `eval.py`, `inference.py`
- `configs/`, `experiments/`, `scripts/`
- `models/`, `networks/`, `modules/`, `losses/`, `datasets/`
- result logs, checkpoints metadata, and experiment tables

## Extract

- Task: classification, detection, segmentation, retrieval, generation, QA, summarization, NER, RAG, multimodal reasoning, etc.
- Inputs and outputs.
- Backbone and key modules.
- Training objective and loss terms.
- Datasets and preprocessing.
- Baselines and evaluation metrics.
- Claims that can be supported by the implementation.

## Red flags

- Method described in notes but absent from code.
- Results table without dataset split or metric direction.
- Baselines without implementation source.
- Hyperparameters missing from config.
- Claims of SOTA without verified comparison.
