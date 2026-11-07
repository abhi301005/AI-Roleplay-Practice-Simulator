
from .roleplay import generate_reply


def evaluate_session(messages, scenario, difficulty, model):

    transcript = "\n".join(
        f'{m["role"].upper()}: {m["content"]}'
        for m in messages
    )

    prompt = f"""
You are an educational communication coach.

Evaluate the learner's {scenario} practice session.
Difficulty: {difficulty}

Analyze only the learner's answers.

Provide:

1. Overall performance summary
2. Strengths
3. Areas for improvement
4. Relevance score (1-5)
5. Clarity score (1-5)
6. Structure score (1-5)
7. One improved sample answer
8. Three improvement suggestions

Be constructive and supportive.
Do not invent learner information.

Conversation:
{transcript}
"""

    return generate_reply([], prompt, model)
