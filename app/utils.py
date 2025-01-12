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
    prompt = (f"This is supposed to be for a Trip planning app and you need to derive hypothesis based on details mentioned below. "
              f"Focus on each small detail as this help suggest best experiences to them on what they love or as per occasion that is near. "
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
        f"Based on the following member hypotheses for the family '{family_name}', "
        f"combine and suggest hypotheses for the entire family:"
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
        f"Based on the following family hypotheses for the group '{group_name}', "
        f"combine and suggest hypotheses for the entire group:"
        f"Give it form of points separated by '\n' and should be of format:"
        f"Group Hypothesis: \n (then followed by points in each new line)"
        f"\n{family_hypotheses}"
    )
    hypotheses = generate_hypotheses(prompt)
    return hypotheses.split("\n")[1:]
