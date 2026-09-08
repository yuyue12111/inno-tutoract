"""Compare v0 trial labels against Bridge labels mapped into v0 (naive and why-aware)."""
import json, collections, sys
path = sys.argv[1] if len(sys.argv) > 1 else "data/annotation/bridge_trial20.annotated.jsonl"
recs = [json.loads(l) for l in open(path)]

NAIVE = {"provide_hint":"HINT","ask_question":"PROBE","provide_strategy":"EXPLAIN",
         "explain_concept":"EXPLAIN","provide_correction":"CORRECT",
         "provide_similar_problem":"PRACTICE","simplify_question":"HINT",
         "affirm_correct_answer":"AFFIRM","encourage_student":"MANAGE","provide_example":"EXAMPLE"}

def why_aware(b):
    w, y = b["strategy"], b["intent"]
    if w == "ask_question":
        if y in ("diagnose_mistake", "elaborate_answer"): return "PROBE"
        if y in ("hint_mistake", "support_thinking", "clarify_misunderstanding"): return "HINT"
        return "PROBE"
    if w == "provide_strategy" and y == "hint_mistake": return "HINT"
    return NAIVE[w]

for name, fn in [("naive", lambda b: NAIVE[b["strategy"]]), ("why-aware", why_aware)]:
    agree = sum(fn(r["bridge"]) == r["v0_action"] for r in recs)
    print(f"{name:10s} agreement: {agree}/{len(recs)} = {agree/len(recs):.0%}")
print("\nv0 action distribution (expert):", collections.Counter(r["v0_action"] for r in recs).most_common())
print("v0 action distribution (orig tutor):", collections.Counter(r["v0_action_for_orig_tutor"] for r in recs).most_common())
print("\nmismatches (why-aware):")
for r in recs:
    m = why_aware(r["bridge"])
    if m != r["v0_action"]:
        print(f"  {r['c_id']}: bridge={r['bridge']['strategy']}/{r['bridge']['intent']} -> {m} | v0={r['v0_action']}")
