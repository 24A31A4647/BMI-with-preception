from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BMI Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-image: url('/static/BMI.PNG');
            background-size: cover;
            background-position: center;
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .overlay {
            background: rgba(0, 0, 0, 0.6);
            position: absolute;
            width: 100%;
            height: 100%;
        }

        .container {
            position: relative;
            background: white;
            padding: 30px;
            width: 400px;
            border-radius: 15px;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.3);
            z-index: 1;
        }

        h1 {
            text-align: center;
        }

        input, select {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 8px;
            border: 1px solid #ccc;
        }

        button {
            width: 100%;
            padding: 12px;
            background: #4CAF50;
            border: none;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
        }

        button:hover {
            background: #45a049;
        }

        .result {
            margin-top: 15px;
            background: #f4f4f4;
            padding: 10px;
            border-radius: 8px;
        }
    </style>

    <script>
        function toggleHeight() {
            let type = document.getElementById("height_type").value;
            document.getElementById("feet").disabled = type !== "feet";
            document.getElementById("inches").disabled = type !== "inches";
        }
    </script>
</head>
<body>
    <div class="overlay"></div>

    <div class="container">
        <h1>BMI Calculator</h1>
        <form method="post">
            <input type="number" name="weight" placeholder="Weight (kg)" required>

            <select id="height_type" name="height_type" onchange="toggleHeight()" required>
                <option value="">Select Height Type</option>
                <option value="feet">Feet</option>
                <option value="inches">Inches</option>
            </select>

            <input type="number" id="feet" name="feet" placeholder="Height in feet" disabled>
            <input type="number" id="inches" name="inches" placeholder="Height in inches" disabled>

            <button type="submit">Calculate</button>
        </form>

        {% if bmi %}
        <div class="result">
            <p><b>BMI:</b> {{ bmi }}</p>
            <p><b>Status:</b> {{ status }}</p>
            <p>{{ tips }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def bmi():
    bmi = None
    status = ""
    tips = ""

    if request.method == "POST":
        weight = float(request.form["weight"])
        height_type = request.form["height_type"]

        if height_type == "feet":
            height_m = float(request.form["feet"]) * 0.3048
        else:
            height_m = float(request.form["inches"]) * 0.0254

        bmi = round(weight / (height_m ** 2), 2)

        if bmi < 18.5:
            status = "Underweight"
            tips = "Eat healthy, increase calorie intake."
        elif bmi < 25:
            status = "Normal weight"
            tips = "Maintain healthy lifestyle."
        elif bmi < 30:
            status = "Overweight"
            tips = "Exercise daily and avoid junk food."
        else:
            status = "Obese"
            tips = "Consult a healthcare professional."

    return render_template_string(
        HTML_TEMPLATE, bmi=bmi, status=status, tips=tips
    )

if __name__ == "__main__":
    app.run(debug=True)
