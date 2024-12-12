from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# HTML Template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>M3U8 Link Finder</title>
</head>
<body>
    <h1>Find M3U8 Links on a Webpage</h1>
    <form method="post">
        <label for="url">Enter a URL:</label><br><br>
        <input type="text" id="url" name="url" placeholder="https://example.com" required>
        <button type="submit">Find Links</button>
    </form>
    <hr>
    {% if result %}
        <h2>Results:</h2>
        {% if result.m3u8_links %}
            <p>Found the following .m3u8 links:</p>
            <ul>
                {% for link in result.m3u8_links %}
                    <li><a href="{{ link }}" target="_blank">{{ link }}</a></li>
                {% endfor %}
            </ul>
        {% else %}
            <p>No .m3u8 links found.</p>
        {% endif %}
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form.get("url")
        result = find_m3u8_links(url)
    return render_template_string(html_template, result=result)

def find_m3u8_links(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        # Find all links in the webpage
        links = [link.get("href") for link in soup.find_all("a", href=True)]
        m3u8_links = [link for link in links if link.endswith(".m3u8")]
        
        return {"m3u8_links": m3u8_links}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(debug=True)
