from flask import Flask, render_template, request
import litellm
import urllib.request
import html2text
from dotenv import load_dotenv
from guardrails import Guard
from guardrails.hub import (
    NSFWText,
    ProfanityFree, PolitenessCheck
)

load_dotenv()

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
    # use guardrails to prevent abuse
    guard = Guard().use_many(
        NSFWText(on_fail='exception'),
        PolitenessCheck(on_fail='exception'),
        ProfanityFree(on_fail='exception'),
    )

    validated_output, *rest = guard(
        llm_api=litellm.completion,
        model="groq/llama3-8b-8192",
        messages=[{"role": "user", "content": input}],
        prompt=f"Here is the text of an article. Please summarize it for me. {content}"
    )

    return render_template('summary.html', url=url, summary=validated_output)