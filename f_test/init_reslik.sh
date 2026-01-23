#!/usr/bin/env bash

set -e

REPO_NAME="reslik"

echo "Creating repository structure: $REPO_NAME"

mkdir -p $REPO_NAME/{cpp,python,docs,examples,benchmarks,scripts}

# -------------------------
# C++ CORE STRUCTURE
# -------------------------
mkdir -p $REPO_NAME/cpp/{include/reslik,src,bindings,tests}

touch $REPO_NAME/cpp/include/reslik/{reslik_unit.hpp,normalization.hpp,gating.hpp,diagnostics.hpp}
touch $REPO_NAME/cpp/src/{reslik_unit.cpp,normalization.cpp,gating.cpp,diagnostics.cpp}
touch $REPO_NAME/cpp/bindings/pybind_module.cpp
touch $REPO_NAME/cpp/tests/test_reslik_unit.cpp

# -------------------------
# PYTHON STRUCTURE
# -------------------------
mkdir -p $REPO_NAME/python/reslik
touch $REPO_NAME/python/reslik/{__init__.py,wrapper.py,diagnostics.py,version.py}

# -------------------------
# EXAMPLES
# -------------------------
mkdir -p $REPO_NAME/examples/{synthetic,rna_seq,multi_modal}
touch $REPO_NAME/examples/synthetic/{generate_data.py,run_reslik.py}
touch $REPO_NAME/examples/rna_seq/{preprocess.py,apply_reslik.py}
touch $REPO_NAME/examples/multi_modal/cross_modal_test.py

# -------------------------
# BENCHMARKS
# -------------------------
touch $REPO_NAME/benchmarks/{stability_shift.py,calibration_eval.py,ablation.py}

# -------------------------
# DOCS
# -------------------------
touch $REPO_NAME/docs/{design_choices.md,failure_modes.md,api_reference.md,what_this_is_not.md}

# -------------------------
# ROOT FILES
# -------------------------
touch $REPO_NAME/{README.md,LICENSE,CITATION.cff,CMakeLists.txt,pyproject.toml}
touch $REPO_NAME/scripts/{build_cpp.sh,run_tests.sh}

# -------------------------
# THEORY.MD (CORE CONTENT)
# -------------------------
cat << 'EOF' > $REPO_NAME/docs/theory.md
# ResLik: Residual Likelihood–Gated Representation Unit

## 1. Motivation

Modern biological models learn high-capacity representations but suffer from:
- overconfidence under distribution shift,
- instability due to noisy features,
- lack of feature-level diagnostics.

ResLik introduces a **likelihood-consistency–gated residual unit** that operates on
feature embeddings *independently of modality*, encouraging representations to
respect empirical biological expectations without enforcing hard constraints.

This unit is **regularizing, not generative**, and **diagnostic, not causal**.

---

## 2. Input Assumptions

Let:
- \( z_i \in \mathbb{R}^d \) be the embedding of feature \( i \)
  (gene, CpG, protein, metabolite, etc.)
- \( \mu_i^{ref}, \sigma_i^{ref} \) be empirical reference statistics
  estimated from training data

No assumptions are made about:
- biological networks,
- pathways,
- omics modality,
- downstream likelihood.

---

## 3. Pre-Normalization

Each feature embedding is normalized independently:

\[
\tilde{z}_i = \frac{z_i - \mu(z_i)}{\sigma(z_i) + \epsilon}
\]

This stabilizes optimization and removes scale dependence from upstream encoders.

---

## 4. Feed-Forward Projection

A shared feed-forward transformation is applied:

\[
f_i = \phi(W \tilde{z}_i + b)
\]

Where:
- \( W \in \mathbb{R}^{d \times d} \)
- \( \phi \) is a smooth nonlinearity (e.g. GELU, SiLU)

Weights are **shared across features**, enforcing consistent behavior.

---

## 5. Learned Distribution Scale

Each feature learns a data-dependent scaling factor:

\[
s_i = \text{softplus}(u^\top \tilde{z}_i)
\]

\[
a_i = s_i \cdot f_i
\]

This allows features with higher uncertainty or variability to be adaptively dampened.

---

## 6. Likelihood-Consistency Discrepancy

We define a normalized discrepancy score:

\[
C_i =
\frac{|\hat{\mu}_i - \mu_i^{ref}|}
{\sigma_i^{ref} + \epsilon}
\]

Where:
- \( \hat{\mu}_i \) is a model-implied or observed statistic
- \( (\mu_i^{ref}, \sigma_i^{ref}) \) are empirical baselines

This score measures **deviation from expected biological behavior**, not error.

---

## 7. Multiplicative Consistency Gating

Instead of injecting discrepancy additively, ResLik applies **multiplicative gating**:

\[
z'_i = a_i \cdot \exp(-\lambda C_i)
\]

Where:
- \( \lambda \ge 0 \) controls the strength of consistency enforcement

This preserves representation geometry while softly suppressing implausible features.

---

## 8. Outputs

The unit outputs:
- gated embeddings \( z'_i \in \mathbb{R}^d \)
- diagnostic scores \( C_i \), gating strengths, and scaling factors

No biological interpretation is imposed at this stage.

---

## 9. Design Intent

ResLik is designed to:
- improve calibration under distribution shift,
- stabilize embeddings across noisy modalities,
- provide feature-level diagnostics.

It is **not** intended to:
- infer causality,
- discover new biological mechanisms,
- replace domain-specific models.

---

## 10. When ResLik May Fail

- Reference statistics are misestimated
- Strong covariate shift invalidates baselines
- Feature embeddings already collapse information

These failure modes are documented explicitly to prevent misuse.

---

## 11. Summary

ResLik is a **representation-level regularization primitive** that introduces
likelihood-awareness without enforcing a specific probabilistic model.

Its strength lies in:
- modularity,
- interpretability,
- and cross-modal applicability.

EOF

echo "Repository $REPO_NAME initialized successfully."
