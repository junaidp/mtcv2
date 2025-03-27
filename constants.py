output_format = {
    "data": [
        {
            "familyName": "Doe",
            "members":
            [
                {
                 "name": "name of the person",
                 "hypothesis":{
                         "extracted_data": "Output Format (Strict JSON no extra statements):\n"
                                           "{\n"
                                           '  "Passions": [ { "label": "<passion_name>", "weight": 3 } ],\n'
                                           '  "Interests": [ { "label": "<interest_name>", "weight": 1 } ],\n'
                                           '  "Lifestyle": [ { "label": "<lifestyle_name>", "weight": 0.5 } ]\n'
                                           "}",
                         "correlations": "Output Format (Strict JSON no extra statements):\n"
                                         "[\n"
                                         '    { "Data Pair": ["label_1", "label_2"], "Relation": "Yes/No", "Reasoning": "Factual explanation" }\n'
                                         " ]\n"
                                         "}",
                         "updated_weights": "Output Format (Strict JSON Ordered by Weight no extra sentences nothing else except json):\n"
                                            "[\n"
                                            '    { "Data Point": "label", "Updated Weight": value, "Details": "Detailed Explanation of calculations with exact points from the data along with explanations on how they added up to the updated weight, Make sure to mention the score additions and also make sure that what is being mentioned here is also making sense with updated weight score, they should go hand in hand" }\n'
                                            " ]\n",
                         "final_hypotheses": "Output Format (Strict JSON Ordered by Confidence no extra statements):\n"
                                             "[\n"
                                             '    { "Hypothesis": "Statement", "Confidence Score": "0%-100%", "Explanation": "Factual reasoning" }\n'
                                             "]\n"
                     }
                },
                {
                    "name": "name of the person",
                    "hypothesis": {
                        "extracted_data": "Output Format (Strict JSON no extra statements):\n"
                                          "{\n"
                                          '  "Passions": [ { "label": "<passion_name>", "weight": 3 } ],\n'
                                          '  "Interests": [ { "label": "<interest_name>", "weight": 1 } ],\n'
                                          '  "Lifestyle": [ { "label": "<lifestyle_name>", "weight": 0.5 } ]\n'
                                          "}",
                        "correlations": "Output Format (Strict JSON no extra statements):\n"
                                        "[\n"
                                        '    { "Data Pair": ["label_1", "label_2"], "Relation": "Yes/No", "Reasoning": "Factual explanation" }\n'
                                        " ]\n"
                                        "}",
                        "updated_weights": "Output Format (Strict JSON Ordered by Weight no extra sentences nothing else except json):\n"
                                           "[\n"
                                            '    { "Data Point": "label", "Updated Weight": value, "Details": "Detailed Explanation of calculations with exact points from the data along with explanations on how they added up to the updated weight, Make sure to mention the score additions and also make sure that what is being mentioned here is also making sense with updated weight score, they should go hand in hand" }\n'
                                           " ]\n",
                        "final_hypotheses": "Output Format (Strict JSON Ordered by Confidence no extra statements):\n"
                                            "[\n"
                                            '    { "Hypothesis": "Statement", "Confidence Score": "0%-100%", "Explanation": "Factual reasoning" }\n'
                                            "]\n"
                    }
                }
            ]
        },
        {
            "familyName": "Doe",
            "members": [
                {
                 "name": "name of the person",
                 "hypothesis":{
                         "extracted_data": "Output Format (Strict JSON no extra statements):\n"
                                           "{\n"
                                           '  "Passions": [ { "label": "<passion_name>", "weight": 3 } ],\n'
                                           '  "Interests": [ { "label": "<interest_name>", "weight": 1 } ],\n'
                                           '  "Lifestyle": [ { "label": "<lifestyle_name>", "weight": 0.5 } ]\n'
                                           "}",
                         "correlations": "Output Format (Strict JSON no extra statements):\n"
                                         "[\n"
                                         '    { "Data Pair": ["label_1", "label_2"], "Relation": "Yes/No", "Reasoning": "Factual explanation" }\n'
                                         " ]\n"
                                         "}",
                         "updated_weights": "Output Format (Strict JSON Ordered by Weight no extra sentences nothing else except json):\n"
                                            "[\n"
                                            '    { "Data Point": "label", "Updated Weight": value, "Details": "Detailed Explanation of calculations with exact points from the data along with explanations on how they added up to the updated weight, Make sure to mention the score additions and also make sure that what is being mentioned here is also making sense with updated weight score, they should go hand in hand" }\n'
                                            " ]\n",
                         "final_hypotheses": "Output Format (Strict JSON Ordered by Confidence no extra statements):\n"
                                             "[\n"
                                             '    { "Hypothesis": "Statement", "Confidence Score": "0%-100%", "Explanation": "Factual reasoning" }\n'
                                             "]\n"
                     }
                },
                {
                    "name": "name of the person",
                    "hypothesis": {
                        "extracted_data": "Output Format (Strict JSON no extra statements):\n"
                                          "{\n"
                                          '  "Passions": [ { "label": "<passion_name>", "weight": 3 } ],\n'
                                          '  "Interests": [ { "label": "<interest_name>", "weight": 1 } ],\n'
                                          '  "Lifestyle": [ { "label": "<lifestyle_name>", "weight": 0.5 } ]\n'
                                          "}",
                        "correlations": "Output Format (Strict JSON no extra statements):\n"
                                        "[\n"
                                        '    { "Data Pair": ["label_1", "label_2"], "Relation": "Yes/No", "Reasoning": "Factual explanation" }\n'
                                        " ]\n"
                                        "}",
                        "updated_weights": "Output Format (Strict JSON Ordered by Weight no extra sentences nothing else except json):\n"
                                           "[\n"
                                            '    { "Data Point": "label", "Updated Weight": value, "Details": "Detailed Explanation of calculations with exact points from the data along with explanations on how they added up to the updated weight, Make sure to mention the score additions and also make sure that what is being mentioned here is also making sense with updated weight score, they should go hand in hand" }\n'
                                           " ]\n",
                        "final_hypotheses": "Output Format (Strict JSON Ordered by Confidence no extra statements):\n"
                                            "[\n"
                                            '    { "Hypothesis": "Statement", "Confidence Score": "0%-100%", "Explanation": "Factual reasoning" }\n'
                                            "]\n"
                    }
                }
            ]
        },
        "similarly for each family",
    ]
}