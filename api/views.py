import requests
from django.http import JsonResponse
from datetime import datetime, timezone

GENDERIZE_URL = "https://api.genderize.io"


def classify_name(request):
    try:
        # Allow only GET
        if request.method != "GET":
            response = JsonResponse(
                {"status": "error", "message": "Method not allowed"},
                status=405
            )
            response["Access-Control-Allow-Origin"] = "*"
            return response

        name = request.GET.get("name")

        # Missing or empty
        if name is None or name.strip() == "":
            response = JsonResponse(
                {"status": "error", "message": "Name parameter is required"},
                status=400
            )
            response["Access-Control-Allow-Origin"] = "*"
            return response

        # Safe string handling 
        if not isinstance(name, str):
            response = JsonResponse(
                {"status": "error", "message": "Name must be a string"},
                status=422
            )
            response["Access-Control-Allow-Origin"] = "*"
            return response

        # External API call
        try:
            r = requests.get(
                GENDERIZE_URL,
                params={"name": name},
                timeout=2
            )
        except requests.exceptions.RequestException:
            response = JsonResponse(
                {"status": "error", "message": "External API request failed"},
                status=502
            )
            response["Access-Control-Allow-Origin"] = "*"
            return response

        if r.status_code != 200:
            response = JsonResponse(
                {"status": "error", "message": "External API error"},
                status=502
            )
            response["Access-Control-Allow-Origin"] = "*"
            return response

        data = r.json()

        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")

        # type safety 
        probability = float(probability or 0)
        count = int(count or 0)

        # Edge case rule
        if gender is None or count == 0:
            response = JsonResponse(
                {
                    "status": "error",
                    "message": "No prediction available for the provided name"
                },
                status=400
            )
            response["Access-Control-Allow-Origin"] = "*"
            return response

        # Confidence logic
        is_confident = probability >= 0.7 and count >= 100

        processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        response = JsonResponse({
            "status": "success",
            "data": {
                "name": name,
                "gender": gender,
                "probability": probability,
                "sample_size": count,
                "is_confident": is_confident,
                "processed_at": processed_at
            }
        })

        response["Access-Control-Allow-Origin"] = "*"
        return response

    except Exception:
        response = JsonResponse(
            {"status": "error", "message": "Internal server error"},
            status=500
        )
        response["Access-Control-Allow-Origin"] = "*"
        return response