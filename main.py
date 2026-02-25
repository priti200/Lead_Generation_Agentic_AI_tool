import json
import os
import subprocess
from preprocess import clean_text
from groq_analysis import analyze_with_groq
from scoring import calculate_final_score
from decision import decide_crm_category

Input_folder = "mock_inputs"

def read_input(filename):
    file_path = os.path.join(Input_folder,filename)

    with open (file_path,'r') as file:
        data = json.load(file)
    return data


if __name__=="__main__":
    # Run bolna.py first
    print("Running bolna.py...")
    subprocess.run(["python", "bolna/bolna.py"], check=True)
    print("bolna.py executed successfully.")

    # Process files in the mock_inputs folder
    files = os.listdir(Input_folder)
    for file in files:
        data = read_input(file)

        analysis_result = analyze_with_groq(data)

        final_score = calculate_final_score(analysis_result)

        crm_category = decide_crm_category(final_score)

        output_data = {
            "event_type": "lead_analyzed",
            "lead_id": data["lead_id"],
            "name": data["lead"]["name"],
            "phone": data["lead"]["phone"],
            "email": data["lead"]["email"],
            # "responses": data["responses"],
            "analysis": analysis_result,
            "ai_score": final_score,
            "crm_category": crm_category
        }

        OUTPUT_FOLDER = "mock_outputs"
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        output_file_path = os.path.join(
            OUTPUT_FOLDER,
            f"analysis_{data['lead_id']}.json"
        )

        with open(output_file_path, "w") as f:
            json.dump(output_data, f, indent=4)

        print("Final JSON saved at:", output_file_path)
        try:
            # Send the JSON directly to CRM via crm.crm_push.send_payload
            from crm import crm_push

            resp = crm_push.send_payload(output_data)
            print("Lead created successfully.")
            print("Lead ID:", resp.get("id"))
        except Exception as e:
            print("Error sending to CRM:", e)