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
                "1. Calculate the age of the person by their given date of birth, which can help advise what travel experiences are more suitable as per their age."
                "2. Get details regarding if any latest event coming up from the details given like birthday, anniversary, etc."
                "3. Get important timeframes like their school pass out year, graduation or any significant date events to take care of."
                "4. Grab an idea about their interests and likings from the details given."
                "5. Also take into account where the person belongs from, passions and lifestyles to see how they can be blended together to "
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
        "1. Map out if the family is planning to celebrate any significant events in nearby future to simulate travelling experiences."
        "2. Shared or complementary passions, interests, and lifestyle factors among family members."
        "3. Calculate age gaps between the oldest and youngest members of the family."
        "4. Potential conflicts or divergences in preferences and how they could be addressed."
        "5. Opportunities for combined experiences that enrich the family as a unit."
        "6. Any combined family events coming up like two people's birthdays coming together or husband-wife anniversary date, etc. make observations like that."
        "7. After getting everything above, rank the information in descending order of importance of what the family travelling experiences can be suggested from."
        "Provide suggestions that go beyond conventional activities, ensuring hypotheses are exploratory and obtained data-driven."
        
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
        "1. Identifying similar traits between different family's members or any shared interests across families."
        "2. Highlighting potential synergies or conflicts between family preferences and ways to address that"
        "3. Suggesting novel group experiences that align with shared interests, ranked importance or bridge differences."
        "4. Avoid assuming obvious solutions and instead explore creative, less conventional possibilities. Frame hypotheses as real life testable   ideas."
        
        f"Give it form of points separated by '\n' and should be of format:"
        f"Group Hypothesis: \n (then followed by points in each new line)"
        f"\n{family_hypotheses}"
    )
    hypotheses = generate_hypotheses(prompt)
    return hypotheses.split("\n")[1:]
