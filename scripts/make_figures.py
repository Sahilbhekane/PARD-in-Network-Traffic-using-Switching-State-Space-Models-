"""Regenerate the result figures used in the README and docs.

Every held-out number is read from ``artifacts/<dataset>/metrics.json`` (written by
``scripts/export_artifacts.py``), so the figures always match the exported models.

The only hard-coded values are the *repository-reported* F1-scores of the original
shuffled-split experiments, which cannot be regenerated (see README, "Limitations").

Usage (from the repository root):
    python scripts/make_figures.py
    python scripts/make_figures.py --out docs/figures
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATASETS = {"cicids2017": "CICIDS2017", "unswnb15": "UNSW-NB15"}

# Original repository-reported hybrid F1 (random 80/20 split of shuffled rows; NOT reproduced).
REPORTED_F1 = {"cicids2017": 0.9607, "unswnb15": 0.9438}

INDIGO, TEAL, AMBER, ROSE, SLATE, LIGHT = "#4F46E5", "#14B8A6", "#F59E0B", "#E11D48", "#334155", "#CBD5E1"
VARIANTS = [("rf_only", "RF only"), ("rf_diff", "RF + differences"), ("hybrid", "Hybrid (RF + SSSM)")]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#94A3B8",
    "axes.labelcolor": SLATE,
    "xtick.color": SLATE,
    "ytick.color": SLATE,
    "axes.titleweight": "bold",
    "axes.titlesize": 12,
    "figure.facecolor": "white",
})


def load_metrics() -> dict:
    out = {}
    for key in DATASETS:
        path = ROOT / "artifacts" / key / "metrics.json"
        out[key] = json.loads(path.read_text(encoding="utf-8"))
    return out


def _save(fig, out_dir: Path, name: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_dir / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out_dir / name}")


def fig_ablation(m: dict, out: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4), sharey=True)
    colors = {"precision": INDIGO, "recall": TEAL, "f1": AMBER}
    for ax, (key, title) in zip(axes, DATASETS.items()):
        x = np.arange(len(VARIANTS))
        w = 0.26
        for i, metric in enumerate(["precision", "recall", "f1"]):
            vals = [m[key]["variants"][v][metric] for v, _ in VARIANTS]
            bars = ax.bar(x + (i - 1) * w, vals, w, label=metric.upper() if metric == "f1" else metric.capitalize(),
                          color=colors[metric])
            for b, v in zip(bars, vals):
                ax.text(b.get_x() + b.get_width() / 2, v + 0.012, f"{v:.3f}", ha="center", va="bottom",
                        fontsize=7.5, color=SLATE)
        ax.set_xticks(x)
        ax.set_xticklabels([lbl for _, lbl in VARIANTS])
        ax.set_ylim(0, 1.12)
        ax.set_title(f"{title} — held-out test partition")
        ax.grid(axis="y", color="#E2E8F0", linewidth=0.8)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("Score")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.06), ncol=3, frameon=False)
    fig.suptitle("Ablation: what does each component add?", fontsize=14, fontweight="bold", y=1.02)
    _save(fig, out, "ablation_heldout.png")


def fig_protocol(m: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    labels = list(DATASETS.values())
    series = [
        ("Repository-reported hybrid\n(random shuffled split, not reproducible)", [REPORTED_F1[k] for k in DATASETS], LIGHT),
        ("Reproduced RF only\n(chronological split)", [m[k]["variants"]["rf_only"]["f1"] for k in DATASETS], TEAL),
        ("Reproduced hybrid\n(chronological split)", [m[k]["variants"]["hybrid"]["f1"] for k in DATASETS], INDIGO),
    ]
    x = np.arange(len(labels))
    w = 0.26
    for i, (name, vals, color) in enumerate(series):
        bars = ax.bar(x + (i - 1) * w, vals, w, label=name, color=color)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.01, f"{v:.3f}", ha="center", fontsize=9, color=SLATE)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("F1-score")
    ax.set_title("The evaluation protocol changes the conclusion")
    ax.grid(axis="y", color="#E2E8F0")
    ax.set_axisbelow(True)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.30), ncol=3, frameon=False, fontsize=8.5)
    _save(fig, out, "protocol_effect.png")


def fig_prevalence(m: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    splits = ["train", "val", "test"]
    x = np.arange(len(splits))
    w = 0.34
    for i, ((key, name), color) in enumerate(zip(DATASETS.items(), [INDIGO, TEAL])):
        vals = [m[key]["attack_rate"][s] * 100 for s in splits]
        bars = ax.bar(x + (i - 0.5) * w, vals, w, label=name, color=color)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.4, f"{v:.1f}%", ha="center", fontsize=9, color=SLATE)
    ax.set_xticks(x)
    ax.set_xticklabels(["Training (60%)", "Validation (20%)", "Test (20%)"])
    ax.set_ylabel("Attack share of rows (%)")
    ax.set_title("Attack prevalence shifts across chronological splits")
    ax.grid(axis="y", color="#E2E8F0")
    ax.set_axisbelow(True)
    ax.legend(frameon=False)
    _save(fig, out, "prevalence_shift.png")


def fig_classwise(m: dict, out: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6), gridspec_kw={"width_ratios": [1, 1.5]})
    for ax, (key, title) in zip(axes, DATASETS.items()):
        fam = m[key]["per_family_flagged_rate"]
        benign_key = "BENIGN" if "BENIGN" in fam else "Normal"
        attack_items = sorted(((k, v) for k, v in fam.items() if k != benign_key),
                              key=lambda kv: kv[1]["flagged_rate"])
        items = [(benign_key, fam[benign_key])] + attack_items
        names = [f"{k}  (n={v['n']:,})" for k, v in items]
        rates = [v["flagged_rate"] * 100 for _, v in items]
        colors = [AMBER] + [TEAL if r >= 80 else ROSE for r in rates[1:]]
        y = np.arange(len(items))[::-1]
        ax.barh(y, rates, color=colors, height=0.62)
        for yi, r in zip(y, rates):
            ax.text(min(r + 1.5, 101), yi, f"{r:.1f}%", va="center", fontsize=8.5, color=SLATE)
        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=9)
        ax.set_xlim(0, 118)
        ax.set_xlabel("Share of test rows flagged as attack (%)")
        ax.set_title(f"{title}")
        ax.grid(axis="x", color="#E2E8F0")
        ax.set_axisbelow(True)
    fig.suptitle("Class-wise detection (hybrid). Amber = benign false-alarm rate; others = recall. "
                 "Classes with n < 30 are statistically unreliable.", fontsize=10.5, color=SLATE, y=1.01)
    _save(fig, out, "classwise_detection.png")


def fig_confusion(m: dict, out: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    for ax, (key, title) in zip(axes, DATASETS.items()):
        c = m[key]["variants"]["hybrid"]["confusion"]
        mat = np.array([[c["tn"], c["fp"]], [c["fn"], c["tp"]]])
        norm = mat / mat.sum(axis=1, keepdims=True)
        ax.imshow(norm, cmap="Blues", vmin=0, vmax=1.15)
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{mat[i, j]:,}\n({norm[i, j] * 100:.1f}% of row)", ha="center", va="center",
                        fontsize=10.5, color="white" if norm[i, j] > 0.55 else SLATE, fontweight="bold")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Predicted benign", "Predicted attack"])
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["Actual benign", "Actual attack"])
        thr = m[key]["variants"]["hybrid"]["threshold"]
        ax.set_title(f"{title} (threshold {thr:.3f})")
        for s in ax.spines.values():
            s.set_visible(False)
        ax.tick_params(length=0)
    fig.suptitle("Hybrid model — confusion matrices on the held-out test partition", fontsize=13,
                 fontweight="bold", y=1.03)
    _save(fig, out, "confusion_matrices.png")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "docs" / "figures"), help="output directory")
    args = ap.parse_args()
    out = Path(args.out)
    m = load_metrics()
    fig_ablation(m, out)
    fig_protocol(m, out)
    fig_prevalence(m, out)
    fig_classwise(m, out)
    fig_confusion(m, out)


if __name__ == "__main__":
    main()
