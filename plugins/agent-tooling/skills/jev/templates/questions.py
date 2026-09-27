# questions.py: every Jev question and threshold for <DECISION>, in one file for review.
#
# Copied from the jev skill template. Replace every <ANGLE> placeholder, delete the
# example question you do not need, and keep the contract:
#   - evidence: <WHAT THE STATE HOLDS, AND WHERE CODE GETS EACH FIELD>
#   - Jev decides: <THE NARROW JUDGMENT>. It does not decide: <WHAT STAYS WITH CODE OR A PERSON>
#   - thresholds are PROVISIONAL until a held-out run supports them:
#     <DATE, ITEM COUNT, RESULTS FILE>
from typesafe_sdk import Choice, Noul, NoulCriteria

# Pinned so thresholds keep meaning. Before changing it: client.models.list(), read the
# changelog, and re-run evaluate.py on the held-out set.
MODEL = "jev-1.13.0"

QUESTIONS = {
    # Example Noul: one property the state can answer, phrased so a high value means yes.
    "<noul_id>": Noul(
        instructions={
            "question": "Is `candidate` the same <THING> as `reference`?",
            "focus": "<WHAT TO COMPARE, AND WHAT TO IGNORE>",
        },
        criteria=NoulCriteria(
            true="<WHAT COUNTS AS YES, CONCRETELY>",
            false="<WHAT COUNTS AS NO, INCLUDING THE NEAR MISS THAT IS STILL NO>",
        ),
    ),
    # Example Choice: every option defined, including where it stops, plus a way out.
    "<choice_id>": Choice(
        instructions={"question": "<WHICH OPTION FITS `candidate`?>", "focus": "<WHAT TO JUDGE>"},
        criteria={
            "<option_a>": {"what": "<COVERS>", "not_for": "<BELONGS ELSEWHERE>", "examples": ["<REAL CASE>"]},
            "<option_b>": {"what": "<COVERS>", "not_for": "<BELONGS ELSEWHERE>", "examples": ["<REAL CASE>"]},
            "other": "None of the above fit",
        },
    ),
}

# Thresholds: the middle band is never guessed; it goes to review.
YES_FROM = 0.80          # Noul at or above: act on yes
NO_BELOW = 0.20          # Noul below: act on no
CHOICE_CONFIDENCE = 0.60 # Choice confidence below this: review


def build_state(candidate, reference):
    """The evidence packet. Full text, not summaries; records as they stood when judged."""
    return {"candidate": candidate, "reference": reference}


def route(answers):
    """Map answers to an action. Replace with the project's own branches."""
    noul = answers["<noul_id>"].noul
    choice = answers["<choice_id>"]
    if NO_BELOW <= noul < YES_FROM or choice.confidence < CHOICE_CONFIDENCE:
        return "review"
    return f"{'yes' if noul >= YES_FROM else 'no'}:{choice.choice}"


def judge(client, candidate, reference):
    """One call per item. Raises on a missing answer or an unexpected model, never defaults."""
    r = client.system_one(model=MODEL, state=build_state(candidate, reference), questions=QUESTIONS)
    if r.model != MODEL:
        raise RuntimeError(f"answered by {r.model}, thresholds were set on {MODEL}")
    missing = set(QUESTIONS) - set(r.answers)
    if missing:
        raise RuntimeError(f"missing answers: {sorted(missing)}")
    for qid, q in QUESTIONS.items():
        if isinstance(q, Choice) and r.answers[qid].choice not in q.criteria:
            raise RuntimeError(f"{qid}: answer {r.answers[qid].choice!r} is not an option")
    return {"route": route(r.answers), "answers": r.answers, "model": r.model,
            "input_tokens": r.usage.input_tokens}
