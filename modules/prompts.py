
def scenario_prompt(scenario, difficulty, personality, opening=False):
    personalities = {
        "Friendly": "warm, supportive and encouraging",
        "Professional": "professional and realistic",
        "Challenging": "challenging and probing"
    }

    difficulties = {
        "Beginner": "ask simple questions",
        "Intermediate": "ask realistic questions and follow-ups",
        "Advanced": "ask complex questions and challenge weak answers"
    }

    roles = {
        "HR Interview": "You are an HR interviewer.",
        "Technical Interview": "You are a technical interviewer assessing CS knowledge.",
        "Customer Support": "You are a customer with a realistic issue.",
        "English Conversation": "You are an English conversation practice partner."
    }

    start = (
        "Start with a greeting and your first question."
        if opening
        else "Continue naturally and ask only one question at a time."
    )

    return f"""
You are an educational AI roleplay simulator.

Role: {roles[scenario]}
Personality: {personalities[personality]}
Difficulty: {difficulties[difficulty]}

Stay in character.
Keep responses concise.
Ask relevant follow-up questions based on the learner's answers.
Do not answer on behalf of the learner.

{start}
"""
