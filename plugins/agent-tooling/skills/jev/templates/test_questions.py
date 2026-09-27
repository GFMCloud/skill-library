# test_questions.py: proves questions.judge fails closed, by deliberate failure, with a
# FAKE client (fixture data; no API call, no spend). Run before any real call:
#   python test_questions.py
# Every case must print PASS. A FAIL means the gate would accept a bad response.
from types import SimpleNamespace as NS

from typesafe_sdk import Choice

from questions import MODEL, QUESTIONS, judge


class FakeClient:
    """Fixture: returns canned answers. Never report its output as a finding."""

    def __init__(self, drop=None, model=MODEL, noul=0.9, choice=None, confidence=0.9):
        self.drop, self.model, self.noul, self.choice, self.confidence = drop, model, noul, choice, confidence

    def system_one(self, model, state, questions):
        answers = {}
        for i, (qid, q) in enumerate(questions.items()):
            if i == self.drop:
                continue
            if isinstance(q, Choice):
                pick = self.choice or next(iter(q.criteria))
                answers[qid] = NS(choice=pick, confidence=self.confidence)
            else:
                answers[qid] = NS(noul=self.noul)
        return NS(model=self.model, answers=answers, usage=NS(input_tokens=1))


def expect_raise(client, label):
    try:
        judge(client, "candidate", "reference")
    except RuntimeError as e:
        print(f"PASS {label}: raised ({e})")
        return
    except Exception as e:  # the gate missed it and later code tripped over it
        raise SystemExit(f"FAIL {label}: the gate did not catch it; crashed later with {e!r}")
    raise SystemExit(f"FAIL {label}: a bad response was accepted")


for i in range(len(QUESTIONS)):  # drop each answer in turn, not just the first
    expect_raise(FakeClient(drop=i), f"answer {i} missing")
expect_raise(FakeClient(model="some-other-model"), "different model answered")
if any(isinstance(q, Choice) for q in QUESTIONS.values()):
    expect_raise(FakeClient(choice="not-an-option"), "choice outside the options")
    out = judge(FakeClient(confidence=0.1), "candidate", "reference")
    assert out["route"] == "review", out
    print("PASS low-confidence choice routes to review")
out = judge(FakeClient(noul=0.5), "candidate", "reference")
assert out["route"] == "review", out
print("PASS middle-band noul routes to review")
