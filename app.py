from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_url = "https://nphaeger-api-salary-2-hfgwbabahadraqdh.westus2-01.azurewebsites.net/predict"


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", prediction=None, error=None, form_data={})


@app.route("/predict", methods=["POST"])
def predict():
    form_data = {
        "age": request.form.get("age"),
        "gender": request.form.get("gender"),
        "country": request.form.get("country"),
        "highest_deg": request.form.get("highest_deg"),
        "code_experience": request.form.get("code_experience"),
        "current_title": request.form.get("current_title"),
        "company_size": request.form.get("company_size")
    }

    try:
        response = requests.post(api_url, json=form_data, timeout=60)

        if response.status_code != 200:
            return render_template(
                "index.html",
                prediction=None,
                error=f"Failed to get prediction, server responded with status code: {response.status_code}",
                form_data=form_data
            )

        result = response.json()
        prediction = result.get("predicted_salary")

        return render_template(
            "index.html",
            prediction=prediction,
            error=None,
            form_data=form_data
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction=None,
            error=f"Error calling API: {str(e)}",
            form_data=form_data
        )


if __name__ == "__main__":
    app.run(debug=True)