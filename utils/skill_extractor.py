import pandas as pd
import re

def load_skills(path="utils/skills.csv"):
    df = pd.read_csv(path)
    return [s.lower().strip() for s in df["skill"].tolist()]

def extract_skills(text, skills_list):
    text_lower = text.lower()
    found = []
    for skill in skills_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return list(set(found))