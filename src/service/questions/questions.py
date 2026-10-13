from typesafe_sdk import Choice, Noul, Score

PERSON_QUESTIONS = {
    "seniority_level": Choice(
        instructions="What is the professional seniority level of the person?",
        criteria={
            "junior": "Entry-level, junior, or associate roles",
            "mid": "Mid-level practitioner with independent execution",
            "senior": "Senior, lead, principal, or staff-level roles",
            "executive": "Director, VP, C-level, or founder",
        },
    ),
    "is_in_leadership": Noul(
        instructions="The person currently manages a team, leads an organization, or holds a leadership title",
    ),
    "experience_depth": Score(
        instructions="How extensive is their professional track record?",
        criteria=[
            "0 to 2 years (Early career)",
            "3 to 6 years (Mid-career)",
            "7+ years (Highly experienced)",
        ],
    ),
}