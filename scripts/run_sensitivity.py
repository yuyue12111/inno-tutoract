"""State-sensitivity test (Phase 1, exp A).

Fixed dialogue history; only the structured student-state block changes.
The model must output a v0 action label then the reply. We measure whether the
chosen action tracks the state, how often it "tells", and how often it leaks
the final answer.

Usage:
  .venv/bin/python scripts/run_sensitivity.py --thinking off --temperature 0 --n 1 --tag t0
  .venv/bin/python scripts/run_sensitivity.py --thinking off --temperature 0.7 --n 5 --tag t07
  .venv/bin/python scripts/run_sensitivity.py --thinking on  --temperature 0.6 --n 3 --tag think
"""
import argparse, json, pathlib, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from llm_client import chat, MODEL  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
ACTIONS = json.load(open(ROOT / "data/action_set_v0.json"))["actions"]
ACTION_IDS = [a["id"] for a in ACTIONS]

# ---- state variants: identical history, only this block changes -------------
VARIANTS = {
    "ctrl":          None,  # no state block at all
    "unknown":       dict(last_response="incorrect", error_type="unknown",       mastery="unverified", affect="ok",         step_error_streak=1, hints_given=0, note="学生只给了答案，没有写过程，错因不明。", expect="PROBE"),
    "careless":      dict(last_response="incorrect", error_type="careless",      mastery="mid",        affect="ok",         step_error_streak=1, hints_given=0, note="该知识点近期正确率 85%，本次为粗心失误。", expect="HINT"),
    "misconception": dict(last_response="incorrect", error_type="misconception", mastery="low",        affect="ok",         step_error_streak=1, hints_given=0, note="该知识点近期正确率 20%，存在系统性误解，多次以同样方式出错。", expect="EXPLAIN"),
    "escalate":      dict(last_response="incorrect", error_type="procedure",     mastery="low",        affect="ok",         step_error_streak=3, hints_given=2, note="本步已提示两次，学生仍以同样方式出错。", expect="EXPLAIN|EXAMPLE"),
    "frustrated":    dict(last_response="incorrect", error_type="careless",      mastery="mid",        affect="frustrated", step_error_streak=3, hints_given=2, note="学生连续三次出错，最近回复变短、语气烦躁，表示'不想做了'。", expect="MANAGE"),
    "timeout":       dict(last_response="incorrect", error_type="procedure",     mastery="low",        affect="ok",         step_error_streak=4, hints_given=3, note="本步已提示三次仍错，本题剩余时间不足 1 分钟，需要收尾。", expect="CORRECT"),
}

SYSTEM = """你是一名七年级数学辅导老师。每一轮你必须先选择一个教学动作，再给出对学生说的话。

可选动作（只能选一个）：
{actions}

输出格式（严格两行，不要输出其他内容）：
动作：<动作ID>
回复：<对学生说的话，2 到 4 句>
"""


def build_messages(scn, variant):
    actions_txt = "\n".join(f"- {a['id']}（{a['zh']}）：{a['def']}" for a in ACTIONS)
    hist = "\n".join(("老师" if t["role"] == "tutor" else "学生") + "：" + t["text"] for t in scn["history"])
    user = f"题目：{scn['problem']}\n\n对话记录：\n{hist}\n"
    if variant is not None:
        v = {k: variant[k] for k in ["last_response", "error_type", "mastery", "affect", "step_error_streak", "hints_given"]}
        user += "\n学生状态（由系统根据历史作答评估）：\n" + json.dumps(v, ensure_ascii=False) + f"\n说明：{variant['note']}\n"
    user += "\n请给出你的下一步。"
    return [{"role": "system", "content": SYSTEM.format(actions=actions_txt)},
            {"role": "user", "content": user}]


ACT_RE = re.compile(r"动作\s*[:：]\s*\**\s*([A-Z_]+)")
REP_RE = re.compile(r"回复\s*[:：]\s*(.*)", re.S)


def parse(text):
    m = ACT_RE.search(text)
    act = m.group(1) if m else None
    if act not in ACTION_IDS:
        act = None
    r = REP_RE.search(text)
    reply = r.group(1).strip() if r else text.strip()
    return act, reply


def leaks(reply, scn):
    return any(re.search(p, reply) for p in scn["answer_patterns"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--thinking", choices=["on", "off"], default="off")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0, help="debug: only first k scenarios")
    args = ap.parse_args()

    scns = json.load(open(ROOT / "data/sensitivity/scenarios.json"))
    if args.limit:
        scns = scns[: args.limit]
    out = ROOT / f"results/sensitivity/{args.tag}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    jobs = [(s, vname) for s in scns for vname in VARIANTS]

    def run(job):
        s, vname = job
        msgs = build_messages(s, VARIANTS[vname])
        outs = chat(msgs, temperature=args.temperature, n=args.n,
                    thinking=args.thinking == "on", max_tokens=4000 if args.thinking == "on" else 600)
        recs = []
        for i, o in enumerate(outs):
            act, reply = parse(o["content"])
            recs.append(dict(scenario=s["id"], topic=s["topic"], variant=vname,
                             expect=(VARIANTS[vname] or {}).get("expect"),
                             sample=i, action=act, reply=reply, leak=leaks(reply, s),
                             raw=o["content"], reasoning=o["reasoning"], finish=o["finish_reason"],
                             model=MODEL, thinking=args.thinking, temperature=args.temperature))
        return recs

    with open(out, "w") as f, ThreadPoolExecutor(args.workers) as ex:
        futs = [ex.submit(run, j) for j in jobs]
        for fut in tqdm(as_completed(futs), total=len(futs)):
            for r in fut.result():
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
