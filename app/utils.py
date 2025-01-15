from openai import OpenAI
from typing import List, Dict

# Load OpenAI API key from environment variables
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_hypotheses(prompt: str, model="gpt-4-turbo") -> str:
    """
    Function to generate hypotheses using OpenAI's GPT model.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")


def generate_member_hypotheses(member_data) -> List[str]:
    """
    Generate hypotheses for an individual member.
    """
    prompt = (f"You are assisting with a trip planning system. Based on the data provided, generate nuanced hypotheses about this individual's preferences, avoiding assumptions. Focus on:"
                "1. How their passions, interests, and lifestyle interact to suggest diverse and novel possibilities."
                "2. What characteristics from the data (e.g., age, nationality, interests) could inform meaningful experiences to test or explore."
                "3. Hypotheses should be framed as testable ideas, highlighting gaps in the data or areas needing further input."
                f"Give it form of points separated by '\n' and should be of format:"
                f"Hypothesis: \n (then followed by points in each new line)"
                 f"{member_data}")
    hypotheses = generate_hypotheses(prompt)
    return hypotheses.split("\n")[1:]


def generate_family_hypotheses(family_name: str, member_hypotheses) -> List[str]:
    """
    Combine member-level hypotheses to generate family-level hypotheses.
    """
    prompt = (
        f"Using the member-level hypotheses provided, synthesize insights to generate testable family-level hypotheses. Focus on:"

        "1. Shared or complementary passions, interests, and lifestyle factors among family members."
        "2. Potential conflicts or divergences in preferences and how they could be addressed."
        "3. Opportunities for combined experiences that enrich the family as a unit."
        "Provide suggestions that go beyond conventional activities, ensuring hypotheses are exploratory and data-driven."
        
        f"Give it form of points separated by '\n' and should be of format:"
        f"Family Hypothesis: \n (then followed by points in each new line)"
        f"\n{member_hypotheses}"
    )
    hypotheses = generate_hypotheses(prompt)
    return hypotheses.split("\n")[1:]


def generate_group_hypotheses(group_name: str, family_hypotheses: List[List[str]]) -> List[str]:
    """
    Combine family-level hypotheses to generate group-level hypotheses.
    """
    prompt = (
        f"Based on the family-level hypotheses provided, generate hypotheses for the group. Focus on:"

        "1. Identifying overarching themes or shared interests across families."
        "2. Highlighting potential synergies or conflicts between family preferences."
        "3. Suggesting novel group experiences that align with shared themes or bridge differences."
        "4. Avoid assuming obvious solutions and instead explore creative, less conventional possibilities. Frame hypotheses as testable ideas."
        
        f"Give it form of points separated by '\n' and should be of format:"
        f"Group Hypothesis: \n (then followed by points in each new line)"
        f"\n{family_hypotheses}"
    )
    hypotheses = generate_hypotheses(prompt)
    return hypotheses.split("\n")[1:]
