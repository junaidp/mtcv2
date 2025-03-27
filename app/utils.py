from openai import AsyncOpenAI
from typing import List, Dict

# Load OpenAI API key from environment variables
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def generate_hypotheses(prompt: str, model="gpt-4o-mini") -> str:
    """
    Function to generate hypotheses using OpenAI's GPT model.
    """
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=10000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")


async def generate_member_hypotheses(member_data):
    """
    Generate hypotheses for an individual member.
    """
    ### **Step 1: Extract and Assign Weights to Data Points**
    step_1_prompt = (
        "Step 1: Extract data points from the JSON input under the categories: Passions, Interests, and Lifestyle. "
        "Make sure that all the passions, interests or lifestyle data points are within the given inputs."
        "Make sure that there is no external data points that are not given in the input, no such data points should make it to the output."
        "Assign weights as follows: Passions = 3, Interests = 1, Lifestyle = 0.5. "
        "Ensure the extraction is accurate and only based on the given data.\n\n"
        "Output Format (Strict JSON no extra statements):\n"
        "{\n"
        '  "Passions": [ { "label": "<passion_name>", "weight": 3 } ],\n'
        '  "Interests": [ { "label": "<interest_name>", "weight": 1 } ],\n'
        '  "Lifestyle": [ { "label": "<lifestyle_name>", "weight": 0.5 } ]\n'
        "}"
    )
    extracted_data = await generate_hypotheses(f"{step_1_prompt}\n\nData Provided:\n{member_data}")
    print(extracted_data)

    ### **Step 2: Perform Correlation Analysis**
    step_2_prompt = (
        "Step 2: Perform correlation analysis on all possible combinations of extracted data points, "
        "make sure each combination of passions and lifestyle, lifestyle and interests as well as interests and passions. "
        "like if the counts are 4 and 3 for passions and lifestyle there should 4*3=12 correlations tested."
        "Each correlation should be tested against every other data point, and the result should be 'Yes' or 'No' "
        "with a factual reasoning if 'Yes'.\n\n"
        "Output Format (Strict JSON no extra statements):\n"
        "{\n"
        '  "Correlations": [\n'
        '    { "Data Pair": ["label_1", "label_2"], "Relation": "Yes/No", "Reasoning": "Factual explanation" }\n'
        "  ]\n"
        "}"
    )
    correlations = await generate_hypotheses(f"{step_2_prompt}\n\nExtracted Data:\n{extracted_data}")
    print(correlations)

    ### **Step 3: Assign Percentage Correlations and Update Weights**
    step_3_prompt = (
        "Step 3: Assign percentage-based correlations and dynamically update weights. "
        "Use the following scale:\n"
        "- 100% = Direct match (inherits full weight value)\n"
        "- 50% = Partial match (inherits half weight value)\n"
        "- 25% = Weak match (inherits one-quarter weight value)\n"
        "- If Lifestyle factors influence another category, add +0.5\n\n"
        "Output Format (Strict JSON Ordered by Weight no extra sentences nothing else except json):\n"
        "{\n"
        '  "Updated Weights": [\n'
        '    { "Data Point": "label", "Updated Weight": value, "Details": "Explanation of calculations" }\n'
        "  ]\n"
        "}"
    )
    updated_weights = await generate_hypotheses(
        f"{step_3_prompt}\n\nCorrelations:\n{correlations} Initial weights: {extracted_data}")
    print(updated_weights)

    ### **Step 4: Generate Final Hypotheses**
    step_4_prompt = (
        "Step 4: Using the updated weighted data, generate logical and testable hypotheses. "
        "Each hypothesis must be based on factual reasoning and assigned a confidence score (0%-100%).\n\n"
        "Output Format (Strict JSON Ordered by Confidence no extra statements):\n"
        "{\n"
        '  "Hypotheses": [\n'
        '    { "Hypothesis": "Statement", "Confidence Score": "0%-100%", "Explanation": "Factual reasoning" }\n'
        "  ]\n"
        "}"
    )
    final_hypotheses = await generate_hypotheses(f"{step_4_prompt}\n\nUpdated Weights:\n{updated_weights}")
    return {
        "name": member_data['firstName'],
        "hypothesis":
            {
                "extracted_data": json.loads(extracted_data.replace("```", "").replace("json", "")),
                "correlations": json.loads(correlations.replace("```", "").replace("json", "")),
                "updated_weights": json.loads(updated_weights.replace("```", "").replace("json", "")),
                "final_hypotheses": json.loads(final_hypotheses.replace("```", "").replace("json", ""))
            }}


async def generate_family_hypotheses(family_name: str, member_hypotheses):
    """
    Combine member-level hypotheses to generate family-level hypotheses.
    """
    step_4_prompt = (
        f"Using the correlations, updated weighted data and hypothesis for each member generate logical and testable hypotheses for the whole family. "
        "Each hypothesis must be based on factual reasoning and assigned a confidence score (0%-100%).\n\n"
        "Output Format (Strict JSON Ordered by Confidence no extra statements):\n"
        "{\n"
        '  "Hypotheses": [\n'
        '    { "Hypothesis": "Statement", "Confidence Score": "0%-100%", "Explanation": "Factual reasoning" }\n'
        "  ]\n"
        "} \n\n"
        f"\nAll members hypothesis combined: {[member['hypothesis']['final_hypotheses'] for member in member_hypotheses]}"
        f"\nAll members correlations extracted: {[member['hypothesis']['correlations'] for member in member_hypotheses]}"
        f"\nAll members updated weights combined: {[member['hypothesis']['updated_weights'] for member in member_hypotheses]}"
    )
    final_hypotheses = await generate_hypotheses(f"{step_4_prompt}")
    return {
        "final_hypotheses": json.loads(final_hypotheses.replace("```", "").replace("json", ""))
    }


async def generate_group_hypotheses(group_name: str, family_hypotheses):
    """
    Combine family-level hypotheses to generate group-level hypotheses.
    """

    step_4_prompt = (
        f"Using the correlations, updated weighted data and hypothesis for each member as well as family, generate logical and testable hypotheses for the whole group {group_name}. "
        "Each hypothesis must be based on factual reasoning and assigned a confidence score (0%-100%).\n\n"
        "Output Format (Strict JSON Ordered by Confidence no extra statements):\n"
        "{\n"
        '  "Hypotheses": [\n'
        '    { "Hypothesis": "Statement", "Confidence Score": "0%-100%", "Explanation": "Factual reasoning" }\n'
        "  ]\n"
        "} \n\n"
        f"\nFamily hypothesis: {family_hypotheses}"
    )

    final_hypotheses = await generate_hypotheses(f"{step_4_prompt}")
    return {
        "final_hypotheses": json.loads(final_hypotheses.replace("```", "").replace("json", ""))
    }
