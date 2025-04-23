import spacy

nlp = spacy.load("en_core_web_sm")

DESIRED_SKILLS = {"Python", "Java", "SQL", "Excel", "Machine Learning", "Data Analysis"}

def analyze_resume(text):
    doc = nlp(text)
    found_skills = set()

    for token in doc:
        if token.text in DESIRED_SKILLS:
            found_skills.add(token.text)

    score = len(found_skills)

    return {
        "skills_found": list(found_skills),
        "entities": [(ent.text, ent.label_) for ent in doc.ents],
        "score": score
    }
