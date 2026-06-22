import json
from pathlib import Path

p = Path(r'D:\HACKATHONS AND BUILDATHONS\KAGGLE MASTERCLASS\answers_preview.json')
answers = json.loads(p.read_text())

patches = {
    "Q10": (
        "According to the HR policy, the following employees are eligible for Work From Home (WFH) arrangements:\n\n"
        "- L3 and above: Hybrid WFH and Ad-hoc WFH\n"
        "- L5 and above: Full Remote (case-by-case, formal approval required)\n"
        "- All employees: Emergency WFH\n\n"
        "The four types of WFH arrangements are:\n"
        "1. Hybrid WFH: Fixed WFH days agreed with reporting manager (max 3 days/week)\n"
        "2. Full Remote: Works entirely from remote location with formal approval (max 5 days/week)\n"
        "3. Ad-hoc WFH: Unplanned single-day WFH for personal or minor health reasons (max 2 days)\n"
        "4. Emergency WFH: Activated during declared emergencies, natural disasters, or health advisories (as directed by HR)"
    ),
    "Q12": (
        "According to the HR policy, Employee Stock Options (ESOP) have a 4-year vesting schedule on a 1-year cliff basis. "
        "This benefit is offered to employees at grade L5 and above. "
        "The specific number of stock options granted to a new joiner is determined individually and is not specified in the HR policy documents."
    ),
}

for item in answers:
    qid = item["question_id"]
    if qid in patches:
        item["answer"] = patches[qid]
        print(f"Patched {qid}")

p.write_text(json.dumps(answers, indent=2))
print("Done — answers_preview.json updated")
