"""Stratified sample of Bridge dialogues for action-set v0 trial annotation.

Outputs a JSONL annotation template: one record per sampled conversation,
with the history, the expert response, Bridge's original labels, and empty
slots for v0 labels (student state + action).
"""
import json, random, collections, argparse, pathlib

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=20)
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--out", default="data/annotation/bridge_trial20.template.jsonl")
args = ap.parse_args()

root = pathlib.Path("data/raw/bridge/dataset")
rows = []
for split in ["train", "validation", "test"]:
    for r in json.load(open(root / f"{split}.json")):
        r["split"] = split
        rows.append(r)

# keep only the 10 canonical strategy labels; free-text ones are edge cases
canon = {"ask_question","explain_concept","provide_hint","provide_strategy",
         "provide_correction","provide_similar_problem","simplify_question",
         "affirm_correct_answer","encourage_student","provide_example"}
rows = [r for r in rows if r["z_what"] in canon]
random.seed(args.seed)
random.shuffle(rows)

# stratify: at least 1 per strategy, remaining proportional to frequency
by = collections.defaultdict(list)
for r in rows: by[r["z_what"]].append(r)
picked = [by[k].pop() for k in canon]
rest = [r for k in canon for r in by[k]]
random.shuffle(rest)
picked += rest[: args.n - len(picked)]
random.shuffle(picked)

out = pathlib.Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "w") as f:
    for r in picked:
        rec = {
            "c_id": r["c_id"], "split": r["split"], "topic": r["lesson_topic"],
            "history": [f'{t["user"]}: {t["text"]}' for t in r["c_h"]],
            "expert_response": " ".join(t["text"] for t in r["c_r_"]),
            "orig_tutor_response": " ".join(t["text"] for t in r["c_r"]),
            "bridge": {"error": r["e"], "strategy": r["z_what"], "intent": r["z_why"]},
            "v0_state": {"last_response": None, "error_type": None,
                          "mastery": None, "affect": None},
            "v0_action": None, "v0_secondary": None,
            "v0_action_for_orig_tutor": None,
            "notes": ""
        }
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
print(f"wrote {len(picked)} -> {out}")
print(collections.Counter(r["z_what"] for r in picked))
