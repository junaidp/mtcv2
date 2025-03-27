import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.utils import (
    generate_member_hypotheses,
    generate_family_hypotheses,
    generate_group_hypotheses,
    generate_hypotheses
)
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import nest_asyncio
import asyncio
from fastapi.responses import JSONResponse
import json
from constants import output_format

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input model for custom testing
class CustomPromptInput(BaseModel):
    input_data: dict

@app.post("/generate_hypotheses/")
async def generate_trip_hypotheses(group_input: dict):
    """
    Generates hypotheses for a group, analyzing each family and individual within it.
    """
    try:
        families = []
        all_members = []

        for customer in group_input["customers"]:
            member = {key: value for key, value in customer.items() if key != "dependents"}
            all_members.append(member)

            family_name = f"{customer['lastName']}"
            member_hypotheses = []

            all_members.extend(customer.get("dependents", []))

            # Generate hypotheses for each dependent
            for dependent in all_members:
                curr_member_hypo = generate_member_hypotheses(dependent)
                member_hypotheses.append({
                    "name": dependent['firstName'],
                    "hypotheses": curr_member_hypo
                })

            # Generate family-level hypotheses
            family_hypotheses = generate_family_hypotheses(family_name, member_hypotheses)
            families.append({
                "familyName": family_name,
                "familyHypotheses": family_hypotheses,
                "members": member_hypotheses
            })

        # Generate group-level hypotheses
        group_hypotheses = generate_group_hypotheses(group_input["groupName"], [f["familyHypotheses"] for f in families])

        # Construct final output
        return JSONResponse({
            "groupHypotheses": group_hypotheses,
            "familyHypotheses": families
        })
    except Exception as e:
        print(f"Error generating hypotheses: {str(e)} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error generating hypotheses: {str(e)}")


@app.post("/generate_response/")
async def generate_response(request: CustomPromptInput):
    """
    Multi-Step Breakdown to process JSON Input and generate more accurate structured hypotheses.
    """
    try:
        input_data = request.input_data
        prompt = ("You need to perform the below instructed steps for each member in the input data as well as whole family and then the group, the input data is a structured json which lists various details of a family by"
                  "member and then the dependents and has separate attributes for each of those. You need to extract details for each member separately. Below are step by step instructions:"
                  "Step 1: Extract data points from the JSON input under the categories: Passions, Interests, and Lifestyle. Stick to passions, interests and lifestyle given only, dont make assumptions or bring anything out of the box."
                  "Assign weights as follows: Passions = 3, Interests = 1, Lifestyle = 0.5. "
                  "Ensure the extraction is accurate and only based on the given data.\n\n"
                  "Step 2: Perform correlation analysis on all possible combinations of extracted data points, "
                  "make sure each combination of datapoints from passions, lifestyle and interests itself gets comapred as well as data points across passions and lifestyle, lifestyle and interests as well as interests and passions is compared and none of them is missed. "
                  "So for example, if there are total 15 data points like: Passions: [A,B,C], Lifestyle:[D,E] and interest: [F,G,H,I], the comparisons should be of each data point with the other data point, for example: "
                  "[A,B],[A,C],[A,D],[A,E],[A,H],[A,G],[A,H] and similarly for other data points like this (considering B has already been compared with A) so: [B,C], [B,D], [B,E], [B,F], [B,G], [B,H]"
                  "a data point in passions must be compared with other data points in passion as well as also with each data point from interests as well as lifestyle so in the example explained total data points are n(n-1)/2 which should result into 9*8/2=36 correlations tested"
                  "this must be followed for each data point in passions, interests and lifestyle making sure that later ones are compared as previous would already have been compared, make sure none of the correlations are missed out."
                  "Each correlation should be tested against every other data point, and the result should be 'Yes' or 'No' and make sure the correlations list has (n* (n-1))/2 number of items mapped in output where n being the sum of data points out of Passions, Interests, and Lifestyle. Dont leave out any or omit any for brevity as they are required and important"
                  "with a factual reasoning if 'Yes'.\n\n"
                  "Step 3: Assign percentage-based correlations and dynamically update weights based on correlations, look for all direct, partial and weak matches. Make sure to update weights and add weights as per below rules, "
                  "so just for an example, if the main label weight is 3 and there is a direct match with two other labels with weight 3 and 1 respectively, updated weight should be 3(default) + 3 + 1 = 7, it should sum upto 7 and add influence if any"
                  "Use the following scale:\n"
                  "- 100% = Direct match (inherits full weight value)\n"
                  "- 50% = Partial match (inherits half weight value)\n"
                  "- 25% = Weak match (inherits one-quarter weight value)\n"
                  "- If Lifestyle factors influence another category, add +0.5\n\n"
                  "Make no mistakes with weight addition calculations, it is just basic addition of base weight with weights of data points it matched with and make sure all the correlations found are considered while updating weights, missing out on any might cause huge problems and weights should all be collected accurately from data points."
                  " as it is very important to determine hypothesis it should logically make sense when explaining details format in the output."
                  "Step 4: Using the updated weighted data, generate logical and testable hypotheses. "
                  "Each hypothesis must be based on factual reasoning and assigned a confidence score (0%-100%).\n\n"
                  "Output Format (Strict JSON nothing else no extra sentences or explanation, "
                  "Ensure that all correlation pairs, weight calculations, and hypotheses are fully listed in JSON format without any omissions, truncation, or placeholder comments."
                  "The output must be fully expanded JSON, ensuring all data points, correlations, updated weights, and hypotheses are explicitly included. There should be no omissions or abbreviations. Try to get back with everything within 30-40 seconds"
                  f"{output_format}"
                  )
        77416370220
        extracted_data = await generate_hypotheses(f"{prompt}\n\nData Provided:\n{input_data}")
        print(extracted_data)
        ### **Step 1: Extract and Assign Weights to Data Points**
        # step_1_prompt = (
        #     "Step 1: Extract data points from the JSON input under the categories: Passions, Interests, and Lifestyle. Stick to passions, interests and lifestyle given only, dont make assumptions or bring anything out of the box."
        #     "Assign weights as follows: Passions = 3, Interests = 1, Lifestyle = 0.5. "
        #     "Ensure the extraction is accurate and only based on the given data.\n\n"
        #     "Output Format (Strict JSON nothing else):\n"
        #     "{\n"
        #     '  "Passions": [ { "label": "<passion_name>", "weight": 3 } ],\n'
        #     '  "Interests": [ { "label": "<interest_name>", "weight": 1 } ],\n
        #     '  "Lifestyle": [ { "label": "<lifestyle_name>", "weight": 0.5 } ]\n'
        #     "}"
        # )
        # extracted_data = generate_hypotheses(f"{step_1_prompt}\n\nData Provided:\n{input_data}")
        # print(extracted_data)
        #
        # ### **Step 2: Perform Correlation Analysis**
        # step_2_prompt = (
        #     "Step 2: Perform correlation analysis on all possible combinations of extracted data points, "
        #     "make sure each combination of passions and lifestyle, lifestyle and interests as well as interests and passions. "
        #     "like if the counts are 4 and 3 for passions and lifestyle there should 4*3=12 correlations tested."
        #     "Each correlation should be tested against every other data point, and the result should be 'Yes' or 'No' "
        #     "with a factual reasoning if 'Yes'.\n\n"
        #     "Output Format (Strict JSON nothing else):\n"
        #     "{\n"
        #     '  "Correlations": [\n'
        #     '    { "Data Pair": ["label_1", "label_2"], "Relation": "Yes/No", "Reasoning": "Factual explanation" }\n'
        #     "  ]\n"
        #     "}"
        # )
        # correlations = generate_hypotheses(f"{step_2_prompt}\n\nExtracted Data:\n{extracted_data}")
        # print(correlations)
        #
        # ### **Step 3: Assign Percentage Correlations and Update Weights**
        # step_3_prompt = (
        #     "Step 3: Assign percentage-based correlations and dynamically update weights. "
        #     "Use the following scale:\n"
        #     "- 100% = Direct match (inherits full weight value)\n"
        #     "- 50% = Partial match (inherits half weight value)\n"
        #     "- 25% = Weak match (inherits one-quarter weight value)\n"
        #     "- If Lifestyle factors influence another category, add +0.5\n\n"
        #     "Output Format (Strict JSON Ordered by Weight nothign else):\n"
        #     "{\n"
        #     '  "Updated Weights": [\n'
        #     '    { "Data Point": "label", "Updated Weight": value, "Details": "Explanation of calculations" }\n'
        #     "  ]\n"
        #     "}"
        # )
        # updated_weights = generate_hypotheses(f"{step_3_prompt}\n\nCorrelations:\n{correlations}")
        # print(updated_weights)
        #
        # ### **Step 4: Generate Final Hypotheses**
        # step_4_prompt = (
        #     "Step 4: Using the updated weighted data, generate logical and testable hypotheses. "
        #     "Each hypothesis must be based on factual reasoning and assigned a confidence score (0%-100%).\n\n"
        #     "Output Format (Strict JSON Ordered by Confidence nothign else):\n"
        #     "{\n"
        #     '  "Hypotheses": [\n'
        #     '    { "Hypothesis": "Statement", "Confidence Score": "0%-100%", "Explanation": "Factual reasoning" }\n'
        #     "  ]\n"
        #     "}"
        # )
        # final_hypotheses = generate_hypotheses(f"{step_4_prompt}\n\nUpdated Weights:\n{updated_weights}")
        # print(final_hypotheses)

        return JSONResponse(
            json.loads(extracted_data.replace("```", "").replace("json", ""))
        )
    except Exception as e:
        print(f"Error processing structured response: {str(e)} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing structured response: {str(e)}")


# OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Multi-Step Data Analysis API",
        version="1.0.0",
        description="API to perform structured analysis on input JSON data through a step-by-step process.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Run FastAPI server
if __name__ == "__main__":
    import uvicorn
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())
