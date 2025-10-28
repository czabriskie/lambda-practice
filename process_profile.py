import json
from datetime import datetime

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        # Extract multiple user inputs
        name = body.get("name", "")
        email = body.get("email", "")
        age = int(body.get("age", 0))
        interests = body.get("interests", [])

        # Process the data
        profile = {
            "full_name": name.title(),
            "email_domain": email.split("@")[1] if "@" in email else "unknown",
            "age_group": get_age_group(age),
            "interest_count": len(interests),
            "profile_score": calculate_profile_score(name, email, age, interests),
            "created_at": datetime.now().isoformat()
        }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Profile processed successfully",
                "original_input": body,
                "processed_profile": profile
            })
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }

def get_age_group(age):
    if age < 18:
        return "minor"
    elif age < 65:
        return "adult"
    else:
        return "senior"

def calculate_profile_score(name, email, age, interests):
    score = 0
    if name: score += 25
    if "@" in email: score += 25
    if 18 <= age <= 100: score += 25
    if interests: score += 25
    return score
