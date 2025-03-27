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
        group_input = request.input_data
        families = []
        all_members = []

        async def process_family(customer):
            """
            Process a single family's members concurrently.
            """
            family_name = customer["lastName"]
            members = [customer] + customer.get("dependents", [])

            # Step 1: Run ALL member hypotheses in parallel
            member_hypotheses_results = await asyncio.gather(
                *[generate_member_hypotheses(member) for member in members]
            )

            # Step 2: Run family hypothesis generation **AFTER** members are processed
            family_hypotheses = await generate_family_hypotheses(family_name, member_hypotheses_results)

            return {
                "familyName": family_name,
                "familyHypotheses": family_hypotheses,
                "members": member_hypotheses_results
            }

        families = await asyncio.gather(*[process_family(customer) for customer in group_input["customers"]])

        # Generate group-level hypotheses
        group_hypotheses = await generate_group_hypotheses(group_input["groupName"], families)
        return {
            "groupHypotheses": group_hypotheses,
            "familyHypotheses": families
        }

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
