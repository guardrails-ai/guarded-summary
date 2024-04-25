from flask import Flask, render_template, request
app = Flask(__name__)

# index will show an input for user to enter a url
@app.route('/')
def index():
    return render_template('home.html')


# that will lead to a page that will summarize the url given by the user, with appropriate guardrail
@app.route("/summary")
def summary():
    url = request.args.get('url')
    return render_template('summary.html', url=url)