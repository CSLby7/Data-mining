from flask import Flask, request, url_for, render_template, flash
from inverted_file import SearchEngine

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def search():
    result = ""
    content = ""
    query = ""
    if request.method == "POST":
        query = request.form['query']
        searchengine = SearchEngine()
        searchengine.Page_Load()
        result, content = searchengine.Match(query)
        return render_template('index.html', result=result, content=content, query= query)
    result = ""
    content = ""
    return render_template('index.html', query = query)


if __name__ == "__main__":
    app.run()