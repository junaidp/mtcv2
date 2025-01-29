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
    prompt = (
            f"You are analyzing an individual's data to build a multi-dimensional profile that maps their personality, interests, and potential preferences. "
            f"Focus on logical deductions and avoid assumptions:\n\n"
            f"1. Use their age, passions, and lifestyle to hypothesize current priorities and likely preferences.\n"
            f"2. Cross-analyze their cultural and social background with their interests to identify unique or unexpected influences.\n"
            f"3. Suggest areas where additional data could improve the profile (e.g., hobbies, recent activities, specific milestones).\n"
            f"4. Assign a probability score to each hypothesis based on how strongly it is supported by the data.\n\n"
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
        f"Using the family-level hypotheses provided, create a detailed profile of the group '{family_name}' with a focus on identifying shared "
        f"characteristics and group-wide dynamics:\n\n"
        f"1. Combine overlapping interests, cultural influences, and milestones across families to deduce group themes.\n"
        f"2. Highlight potential synergies or divergences within the group and propose testable ways to address them.\n"
        f"3. Rank hypotheses based on their significance to group cohesion and assign probability scores to each.\n\n"
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
        f"Using the family-level hypotheses provided, build a comprehensive profile of the group '{group_name}' by synthesizing shared traits and dynamics. "
        f"Focus on group-wide synergies, potential conflicts, and testable hypotheses:\n\n"
        f"1. Identify overlapping interests or themes across families and hypothesize their potential impact on group preferences.\n"
        f"2. Highlight possible conflicts between family dynamics and suggest ways to test or resolve them.\n"
        f"3. Propose testable ideas for group-wide events or activities that align with shared preferences.\n"
        f"4. Explore less obvious, creative connections between family-level data points to hypothesize unique opportunities.\n"
        f"5. Assign a probability score to each hypothesis to indicate its confidence level based on the data.\n\n"
        
        f"Give it form of points separated by '\n' and should be of format:"
        f"Group Hypothesis: \n (then followed by points in each new line)"
        f"\n{family_hypotheses}"
    )
    hypotheses = generate_hypotheses(prompt)
    return hypotheses.split("\n")[1:]
