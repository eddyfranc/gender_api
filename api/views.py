from django.shortcuts import render
import requests
from django.http import JsonResponse
from datetime import datetime, timezone

GENDERIZE_URL = "https://api.genderize.io"

def classify_name(request):
    try:
        # Only allow GET
        if request.method != "GET":
            return JsonResponse(
                {"status": "error", "message": "Method not allowed"},
                status=405
            )

        name = request.GET.get("name")

        # Validation: missing or empty
        if name is None or name.strip() == "":
            return JsonResponse(
                {"status": "error", "message": "Name is required"},
                status=400
            )

        # Validation: must be string
        if not isinstance(name, str):
            return JsonResponse(
                {"status": "error", "message": "Name must be a string"},
                status=422
            )

        # Call Genderize API
        response = requests.get(GENDERIZE_URL, params={"name": name})

        if response.status_code != 200:
            return JsonResponse(
                {"status": "error", "message": "External API error"},
                status=502
            )

        data = response.json()

        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")

        # Edge Case Handling
        if gender is None or count == 0:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No prediction available for the provided name"
                },
                status=404
            )

        # Confidence Logic
        is_confident = probability >= 0.7 and count >= 100

        # UTC ISO 8601 timestamp
        processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        return JsonResponse(
            {
                "status": "success",
                "data": {
                    "name": name,
                    "gender": gender,
                    "probability": probability,
                    "sample_size": count,
                    "is_confident": is_confident,
                    "processed_at": processed_at
                }
            },
            status=200
        )

    except Exception:
        return JsonResponse(
            {"status": "error", "message": "Internal server error"},
            status=500
        )