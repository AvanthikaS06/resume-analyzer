import re

def check_ats_score(text):
    checks = {
        "Email Address":      bool(re.search(r'[\w.-]+@[\w.-]+\.\w+', text)),
        "Phone Number":       bool(re.search(r'\+?\d[\d\s\-().]{7,}\d', text)),
        "LinkedIn URL":       bool(re.search(r'linkedin\.com', text, re.I)),
        "Education Section":  bool(re.search(r'\b(education|degree|university|college|b\.?tech|m\.?tech)\b', text, re.I)),
        "Experience Section": bool(re.search(r'\b(experience|work history|employment)\b', text, re.I)),
        "Skills Section":     bool(re.search(r'\b(skills|technical skills|core competencies)\b', text, re.I)),
        "Projects Section":   bool(re.search(r'\b(projects|personal projects|academic projects)\b', text, re.I)),
        "Certifications":     bool(re.search(r'\b(certification|certified|certificate)\b', text, re.I)),
    }
    passed = sum(checks.values())
    ats_score = int((passed / len(checks)) * 100)
    feedback = [{"check": k, "passed": v} for k, v in checks.items()]
    return ats_score, feedback