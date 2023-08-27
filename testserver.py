from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# In a real application, this data would be stored in a database
data = {
    "value": "Hello, World!"
}

html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Change API Value</title>
</head>
<body>
    <h1>Current Value: {{ value }}</h1>
    <form method="post" action="/api">
        <label for="value">New Value:</label>
        <input type="text" id="value" name="value">
        <input type="submit" value="Update">
    </form>
</body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_value = request.form['value']
        data["value"] = new_value

    return render_template_string(html_template, value=data["value"])


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        return jsonify(data)

    if request.method == 'POST':
        new_value = request.form['value']
        data["value"] = new_value
        return jsonify({"message": "Value updated successfully!"}), 200


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)