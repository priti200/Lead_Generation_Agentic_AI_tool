import json

def extract_summary_and_transcript(input_file, output_file):
    """
    Extracts the summary and transcript from the input JSON file and writes them to a new JSON file.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output JSON file.
    """
    try:
        # Read the input JSON file
        with open(input_file, 'r') as infile:
            data = json.load(infile)

        # Extract the required fields
        result = {
            "lead_id": 1,
              "lead": {
            "name": "Ajay",
            "phone": "+918590351989",
            "email": "abc@mail.com"
            },
            "summary": data.get("summary"),
            "transcript": data.get("transcript")
        }

        # Write the extracted fields to the output JSON file
        with open(output_file, 'w') as outfile:
            json.dump(result, outfile, indent=4)

        print(f"Summary and transcript successfully extracted to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Define file paths
input_file = "bolna/bolna_response.json"
output_file = "mock_inputs/lead1.json"

# Run the extraction
extract_summary_and_transcript(input_file, output_file)