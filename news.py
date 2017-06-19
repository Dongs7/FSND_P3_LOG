
from newsdb import result_to_view, print_output
from flask import Flask, Markup, url_for, render_template

app = Flask(__name__)

#  Create Output file
print_output()


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html',
                           article=Markup(result_to_view(1)),
                           author=Markup(result_to_view(2)),
                           error_rate=Markup(result_to_view(3)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
