from flask import Flask, render_template, request
from demo_search import searcher

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_value = request.form['input_value']
        result = searcher(input_value)
        return render_template('results.html', input_value=input_value, result=result)
    else:
        return '''<html>
                    <head>
                        <title>Поисковик</title>
                    </head>
                    <body>
                        <h1>Введите запрос:</h1>
                        <form action="/" method="POST">
                            <input type="text" name="input_value">
                            <br><br>
                            <input type="submit" value="Поиск">
                        </form>
                    </body>
                </html>'''


if __name__ == '__main__':
    app.run()