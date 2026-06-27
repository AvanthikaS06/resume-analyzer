import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_suggestions(resume_text, jd_text):
    prompt = f"""
You are a professional resume coach and recruiter.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{jd_text[:1500]}

Give a structured analysis:
1. **Strengths** - What this resume does well for this role
2. **Weaknesses** - What is lacking or weak
3. **Missing Skills** - Key skills from JD not in resume
4. **Improvement Tips** - 3 to 5 specific actionable suggestions
5. **One-Line Verdict** - Hire / Maybe / Pass and why
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content