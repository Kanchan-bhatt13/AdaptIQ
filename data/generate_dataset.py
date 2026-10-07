import math
import os
import random
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ml.rules import EXPECTED_TIME, rule_based_next_difficulty  # noqa: E402

TOPICS = ["Variables", "Loops", "Functions", "OOP", "Data Structures"]
THRESH = {0: 0.25, 1: 0.50, 2: 0.75}   # skill needed to find a level comfortable
N_STUDENTS = 500
QUESTIONS_PER_STUDENT = 40
NOISE = 0.05


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def simulate(seed=7):
    rng = random.Random(seed)
    rows = []
    for sid in range(1, N_STUDENTS + 1):
        base = rng.betavariate(2.2, 2.2)
        skill = {t: min(max(base + rng.gauss(0, 0.12), 0.02), 0.98) for t in TOPICS}
        seen = {t: [0, 0] for t in TOPICS}   # topic -> [correct, total]
        total_c = total_n = streak = 0
        diff = 1
        for _ in range(QUESTIONS_PER_STUDENT):
            topic = rng.choice(TOPICS)
            p = sigmoid(9 * (skill[topic] - THRESH[diff]))
            correct = 1 if rng.random() < p else 0
            expected = EXPECTED_TIME[diff]
            t = expected * (1.45 - skill[topic]) * rng.lognormvariate(0, 0.28)
            if not correct:
                t *= rng.uniform(1.1, 1.6)
            t = round(min(max(t, 3), 180), 1)
            attempts = 1 if correct and rng.random() < 0.9 else rng.choice([1, 2, 2, 3])
            if not correct:
                attempts = max(attempts, rng.choice([1, 2, 2, 3]))

            overall = round(100 * total_c / total_n, 1) if total_n else 60.0
            tc, tn = seen[topic]
            topic_acc = round(100 * tc / tn, 1) if tn else overall

            label = rule_based_next_difficulty(correct, t, attempts, overall, topic_acc, diff)
            if rng.random() < NOISE:
                label = min(2, max(0, label + rng.choice([-1, 1])))

            rows.append(dict(
                student_id=f"S{sid:03d}", topic=topic, difficulty=diff, correct=correct,
                response_time=t, attempts=attempts, overall_accuracy=overall,
                topic_accuracy=topic_acc, recent_streak=streak, next_difficulty=label,
            ))

            # update history
            total_n += 1
            total_c += correct
            seen[topic][0] += correct
            seen[topic][1] += 1
            streak = streak + 1 if correct else 0
            # follow the label most of the time, explore otherwise (covers the feature space)
            diff = label if rng.random() < 0.75 else rng.randint(0, 2)
    return pd.DataFrame(rows)


def main():
    df = simulate()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "student_interactions.csv")
    df.to_csv(out, index=False)
    print(f"Wrote {len(df)} rows to {out}")
    print(df["next_difficulty"].value_counts(normalize=True).sort_index().round(3).to_string())


if __name__ == "__main__":
    main()
