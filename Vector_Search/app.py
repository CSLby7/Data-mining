from flask import Flask, request, url_for, render_template, flash
from VectorSpaceTool import VectorSpaceTool

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def search():
    result = ""
    content = ""
    query = ""
    if request.method == "POST":
        print('111111')
        query = request.form['query']
        vectorspacetool = VectorSpaceTool()
        result, content = vectorspacetool.Search(query)
        return render_template('index.html', result=result, content=content, query= query)
    result = ""
    content = ""
    return render_template('index.html', query = query)


if __name__ == "__main__":
    app.run()