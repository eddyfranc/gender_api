# Gender Classification API
A simple Django-based REST API that predicts the gender of a given name using the Genderize API and returns clean, processed results.

This project is built to demonstrate API integration, data processing, and clean backend design.

---
## 🚀 Live API

https://web-production-43f7f.up.railway.app

---
## 🎯 What this project does

This API takes a name as input and returns:

- Predicted gender
- Confidence level (probability)
- Sample size used for prediction
- A computed confidence flag
- A timestamp of when the request was processed

It acts as a clean wrapper around the Genderize API with additional business logic and validation.

---
## 📍 Endpoint

```
GET /api/classify?name=<name>

```
### Example Request

```
https://web-production-43f7f.up.railway.app/api/classify?name=john

```
---
## ⚙️ How it works

The API integrates with Genderize and processes the response:

- Extracts:
  - gender
  - probability
  - count → renamed to sample_size

- Adds business logic:

```
is_confident = probability >= 0.7 AND sample_size >= 100

```
- Adds metadata:

```
processed_at = current UTC timestamp (ISO 8601)

````
## 📦 Example Response

```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-13T12:00:00Z"
  }
}
````
## ❌ Error Handling

The API handles errors consistently:

### Missing name
```json
{ "status": "error", "message": "Name is required" }
```
### No prediction available

```json
{ "status": "error", "message": "No prediction available for the provided name" }
```
### External API failure

```json
{ "status": "error", "message": "External API request failed" }
```
### Method not allowed

```json
{ "status": "error", "message": "Method not allowed" }
```

## 🧪 How to run locally

Clone and set up the project in seconds:

```
git clone <repo-url>
cd project

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Then visit:

```
http://127.0.0.1:8000/api/classify?name=john
```
## 🧩 Features

* External API integration (Genderize)
* Input validation
* Clean JSON responses
* Confidence scoring logic
* Timestamp tracking
* Error handling for all edge cases

---

## 🛠 Tech Stack

* Python
* Django
* Requests library
* Genderize API

---
## 🌍 Deployment

Live and hosted on Railway:

https://web-production-43f7f.up.railway.app

## 🏁 Try it out

Test the API in your browser or Postman:

```
/api/classify?name=John
