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
    prompt = (f"You are building a detailed personality and preference profile of an individual based on their data. Avoid making assumptions. "
            f"Focus on deriving meaningful insights and probabilities about their personality, taste, and interests. "
            f"Based on the provided data, generate nuanced hypotheses that are testable and open to further data collection:\n\n"
            f"1. Calculate the individual's exact age from the provided date of birth and use it to infer significant milestones (e.g., school, college, retirement).\n"
            f"2. Determine upcoming significant events (e.g., birthdays, anniversaries) based on their data and suggest how these might influence their priorities.\n"
            f"3. Combine their passions, interests, and lifestyle to deduce potential preferences. Avoid recommendations and instead focus on testable ideas.\n"
            f"4. Evaluate their nationality and cultural background to hypothesize unique influences on their personality and preferences.\n"
            f"5. Calculate a probability score for each new deduction based on the provided data.\n\n"
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
        f"Using the member-level hypotheses provided, build a detailed profile of the family '{family_name}' by synthesizing the insights. "
        f"Focus on relationships, shared traits, and potential conflicts or synergies. Avoid recommendations and instead create testable, data-driven hypotheses:\n\n"
        f"1. Analyze the age gap between the youngest and oldest family members and infer its impact on shared activities or preferences.\n"
        f"2. Identify shared or complementary interests across family members and hypothesize their influence on group decision-making.\n"
        f"3. Determine upcoming family-wide events (e.g., anniversaries, shared birthdays) that might require specific planning.\n"
        f"4. Highlight potential conflicts in preferences or lifestyle within the family and propose areas for further inquiry.\n"
        f"5. Provide a ranked list of hypotheses based on their importance to family dynamics.\n"
        f"6. Assign a probability score to each hypothesis to indicate its likelihood based on the data.\n\n"
        
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
