import traceback

from fastapi import FastAPI, HTTPException
from app.models import GroupInput
from app.utils import (
    generate_member_hypotheses,
    generate_family_hypotheses,
    generate_group_hypotheses,
)
import sys
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import nest_asyncio
import asyncio
from fastapi.responses import JSONResponse
from tqdm import tqdm

app = FastAPI()

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins as needed for your use case
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate_hypotheses/")
async def generate_trip_hypotheses(group_input: GroupInput):
    try:
        families = []
        all_members = []

        for customer in group_input.customers:
            member = {key: value for key, value in customer.model_dump().items() if key != "dependents"}
            all_members.append(member)

            family_name = f"{customer.lastName}"
            member_hypotheses = []

            all_members.extend(customer.model_dump()['dependents'])

            # Generate hypotheses for each dependent
            for dependent in tqdm(all_members):
                curr_member_hypo = generate_member_hypotheses(dependent)
                member_hypotheses.append({
                    "name": dependent['firstName'],
                    "hypotheses": curr_member_hypo
                })
                print(f"Hypothesis generated for {dependent['firstName']}: \n {curr_member_hypo}")


            # Generate family-level hypotheses
            family_hypotheses = generate_family_hypotheses(family_name, member_hypotheses)
            families.append({
                "familyName": family_name,
                "familyHypotheses": family_hypotheses,
                "members": member_hypotheses
            })

        # Step 2: Generate group-level hypotheses
        group_hypotheses = generate_group_hypotheses(group_input.groupName, [f["familyHypotheses"] for f in families])

        # Step 3: Construct final output
        return JSONResponse({
            "groupHypotheses": group_hypotheses,
            "familyHypotheses": families
        })
    except Exception as e:
        print(f"Error generating hypotheses: {str(e)} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error generating hypotheses: {str(e)}")


# Define a custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Trip Planning API",
        version="1.0.0",
        description="API for generating hypotheses for group, family, and individual travel planning.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Add the __main__ block
if __name__ == "__main__":
    import uvicorn

    # Apply `nest_asyncio` for running the FastAPI app in the same thread as the event loop
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()

    # Run the application with a local host and port
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    loop.run_until_complete(server.serve())
