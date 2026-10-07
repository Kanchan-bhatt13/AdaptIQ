"""Shared feature definitions and the rule-based labelling function.

The rule-based label is used to create the initial training labels (see section 8
of the project plan) and as a safe fallback if the trained model is unavailable.
"""

DIFFICULTIES = ["Easy", "Medium", "Hard"]
DIFF_TO_INT = {d: i for i, d in enumerate(DIFFICULTIES)}

# Expected seconds a student needs per difficulty level.
EXPECTED_TIME = {0: 20.0, 1: 35.0, 2: 55.0}

FEATURES = [
    "correct",             # 1 if the last answer was right
    "response_time",       # seconds taken
    "attempts",            # attempts used on the question
    "overall_accuracy",    # 0-100, before this question
    "topic_accuracy",      # 0-100, before this question, in this topic
    "recent_streak",       # consecutive correct answers just before this question
    "difficulty",          # 0/1/2 - difficulty of the question just answered
]


def performance_score(correct, response_time, attempts, overall_accuracy,
                      topic_accuracy, difficulty):
    speed_ratio = min(response_time / EXPECTED_TIME[difficulty], 2.0)
    score = (
        0.30 * topic_accuracy / 100.0
        + 0.15 * overall_accuracy / 100.0
        + 0.25 * correct
        + 0.15 * (1.0 - speed_ratio / 2.0)
        + 0.15 * (1.0 / max(attempts, 1))
    )
    # Answering a harder question correctly is stronger evidence of skill.
    score += 0.04 * difficulty * correct
    if not correct:
        score -= 0.10
    return score


def rule_based_next_difficulty(correct, response_time, attempts, overall_accuracy,
                               topic_accuracy, difficulty, **_ignored):
    """Return 0 (Easy), 1 (Medium) or 2 (Hard)."""
    s = performance_score(correct, response_time, attempts, overall_accuracy,
                          topic_accuracy, difficulty)
    if s >= 0.72:
        return 2
    if s >= 0.40:
        return 1
    return 0
