import json
import os
import subprocess
from whatsapp_module.whatsapp import send_message
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
        # Skip any non-lead files (e.g., raw bolna responses)
        if not isinstance(data, dict) or "lead_id" not in data or "lead" not in data:
            print(f"Skipping {file}: missing lead_id or lead payload")
            continue

        analysis_result = analyze_with_groq(data)

        final_score = calculate_final_score(analysis_result)

        crm_category = decide_crm_category(final_score)

        output_data = {
            "event_type": "lead_analyzed",
            # "lead_id": data["lead_id"],
            "name": data["lead"]["name"],
            "phone": data["lead"]["phone"],
            "email": data["lead"]["email"],
            # "responses": data["responses"],
            "analysis": analysis_result,
            "aiScore": final_score,
            "crmCategory": crm_category,
            "summary": data["summary"]
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
        # Send a WhatsApp follow-up to the lead's phone number
        try:
            recipient_phone = data.get("lead", {}).get("phone")
            if recipient_phone:
                message = (
                    "You are a professional admissions associate calling on behalf of Amrita University interested in enrolling for a the PhD program enrolled twice an year\n\n"
                    "About the program in detail:\n"
                    "I understand you’re exploring doctoral studies. May I briefly share how our Ph.D. program at Amrita Vishwa Vidyapeetham is structured? "
                    "Our doctoral programs are designed to develop high-impact researchers with strong methodological foundations and deep domain expertise. "
                    "If you’re aiming for a research-driven career—whether in academia, industry, or policy—this program is structured to provide both intellectual depth and professional growth."
                )
                sms_resp = send_message(recipient_phone, message)
                print("WhatsApp send response:", sms_resp)
            else:
                print("No recipient phone found to send WhatsApp message.")
        except Exception as e:
            print("Error sending WhatsApp message:", e)
        try:
            # Send the JSON directly to CRM via crm.crm_push.send_payload
            from crm import crm_push

            resp = crm_push.send_payload(output_data)
            print("Lead created successfully.")
            print("Lead ID:", resp.get("id"))
        except Exception as e:
            print("Error sending to CRM:", e)