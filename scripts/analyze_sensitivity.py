"""Analyze state-sensitivity runs: action-by-variant matrix, state-following rate,
tell rate, leak rate, per-scenario sensitivity. Writes a markdown table and a PNG.

Usage: .venv/bin/python scripts/analyze_sensitivity.py results/sensitivity/t0.jsonl [more.jsonl ...]
"""
import json, sys, pathlib, collections
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
ACTION_IDS = [a["id"] for a in json.load(open(ROOT / "data/action_set_v0.json"))["actions"]]
VORDER = ["ctrl", "unknown", "careless", "misconception", "escalate", "frustrated", "timeout"]
TELL = {"EXPLAIN", "CORRECT"}


def load(paths):
    rows = []
    for p in paths:
        rows += [json.loads(l) for l in open(p)]
    df = pd.DataFrame(rows)
    df["run"] = df["thinking"].map({"on": "think", "off": "nothink"}) + "@T" + df["temperature"].astype(str)
    return df


def follows(row):
    if not isinstance(row["expect"], str) or not isinstance(row["action"], str):
        return None
    return row["action"] in row["expect"].split("|")


def report(df, name):
    lines = [f"## {name}  (n={len(df)}, parse failures={(df.action.isna()).sum()})", ""]
    # action x variant matrix (percent)
    ct = pd.crosstab(df["variant"], df["action"].fillna("PARSE_FAIL"), normalize="index").mul(100).round(0)
    ct = ct.reindex(index=[v for v in VORDER if v in ct.index])
    cols = [a for a in ACTION_IDS if a in ct.columns] + [c for c in ct.columns if c not in ACTION_IDS]
    ct = ct[cols]
    lines.append("动作分布（行=状态变体，列=模型选的动作，单位 %）")
    lines.append("")
    lines.append(ct.to_markdown())
    lines.append("")
    # per-variant: follow rate, tell rate, leak rate
    df = df.copy()
    df["follow"] = df.apply(follows, axis=1)
    df["tell"] = df["action"].isin(TELL)
    g = df.groupby("variant").agg(follow=("follow", "mean"), tell=("tell", "mean"), leak=("leak", "mean")).reindex(VORDER)
    g["expect"] = [dict(ctrl="-", unknown="PROBE", careless="HINT", misconception="EXPLAIN", escalate="EXPLAIN|EXAMPLE", frustrated="MANAGE", timeout="CORRECT")[v] for v in g.index]
    g = g[["expect", "follow", "tell", "leak"]].mul({"expect": 1, "follow": 100, "tell": 100, "leak": 100}).round(0)
    lines.append("按状态变体：符合启发式期望的比例 / 讲解或告知的比例 / 回复中出现最终答案的比例（%）")
    lines.append("")
    lines.append(g.to_markdown())
    lines.append("")
    # sensitivity: per scenario, number of distinct majority actions across the 6 state variants
    sv = df[df.variant != "ctrl"]
    maj = sv.groupby(["scenario", "variant"])["action"].agg(lambda s: s.mode().iloc[0] if not s.mode().empty else None).unstack()
    ndist = maj.apply(lambda r: r.dropna().nunique(), axis=1)
    lines.append(f"每个场景在 6 种状态下的多数动作互不相同的个数（最大 6）：均值 {ndist.mean():.2f}，分布 {dict(collections.Counter(ndist))}")
    lines.append("")
    lines.append("各场景多数动作：")
    lines.append("")
    lines.append(maj.reindex(columns=[v for v in VORDER if v != "ctrl"]).to_markdown())
    lines.append("")
    # overall state-following (excluding ctrl)
    ov = df[df.variant != "ctrl"]
    lines.append(f"总体：状态符合率 {ov.follow.mean()*100:.0f}%，讲解/告知率 {ov.tell.mean()*100:.0f}%，泄答案率 {ov.leak.mean()*100:.0f}%；无状态对照组讲解/告知率 {df[df.variant=='ctrl'].tell.mean()*100:.0f}%，泄答案率 {df[df.variant=='ctrl'].leak.mean()*100:.0f}%")
    lines.append("")
    return "\n".join(lines), ct


def plot(mats, outpng):
    fig, axes = plt.subplots(1, len(mats), figsize=(5.5 * len(mats), 4), squeeze=False)
    for ax, (name, ct) in zip(axes[0], mats.items()):
        ct = ct.reindex(columns=[a for a in ACTION_IDS if a in ct.columns])
        im = ax.imshow(ct.values, cmap="Blues", vmin=0, vmax=100, aspect="auto")
        ax.set_xticks(range(len(ct.columns)), ct.columns, rotation=45, ha="right", fontsize=8)
        ax.set_yticks(range(len(ct.index)), ct.index, fontsize=8)
        for i in range(ct.shape[0]):
            for j in range(ct.shape[1]):
                v = ct.values[i, j]
                if v > 0:
                    ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=7, color="white" if v > 60 else "black")
        ax.set_title(name, fontsize=10)
        ax.set_xlabel("chosen action (%)"); ax.set_ylabel("student-state variant")
    plt.tight_layout(); plt.savefig(outpng, dpi=150)


def main():
    paths = sys.argv[1:]
    df = load(paths)
    outdir = ROOT / "results/sensitivity"
    md = ["# 状态敏感度测试结果", "", f"模型：{df.model.iloc[0]}；场景 {df.scenario.nunique()} 个；状态变体 {df.variant.nunique()} 种（含无状态对照）。", ""]
    mats = {}
    for run, sub in df.groupby("run"):
        txt, ct = report(sub, run)
        md.append(txt); mats[run] = ct
    (outdir / "report.md").write_text("\n".join(md), encoding="utf-8")
    plot(mats, outdir / "action_by_state.png")
    print("\n".join(md))
    print("wrote", outdir / "report.md", outdir / "action_by_state.png")


if __name__ == "__main__":
    main()
