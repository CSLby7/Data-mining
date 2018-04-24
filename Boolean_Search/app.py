from flask import Flask, request, url_for, render_template, flash
from BooleanSearch import BooleanSearch

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def search():
    query = ""
    if request.method == "POST":
        print('111111')
        query = request.form['query']
        booleansearch = BooleanSearch()
        result, content = booleansearch.Search(query)
        return render_template('index.html', result=result, content=content, query= query)

    return render_template('index.html', query = query)


if __name__ == "__main__":
    app.run()