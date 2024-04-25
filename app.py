from flask import Flask, render_template, request
import urllib.request
import html2text

app = Flask(__name__)
h = html2text.HTML2Text()
h.ignore_links = True

# index will show an input for user to enter a url
@app.route('/')
def index():
    return render_template('home.html')


# that will lead to a page that will summarize the url given by the user, with appropriate guardrail
@app.route("/summary")
def summary():
    url = request.args.get('url')

    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    html_content = mybytes.decode("utf8")
    fp.close()
    
    content = h.handle(html_content)

    print(content)

    return render_template('summary.html', url=url)