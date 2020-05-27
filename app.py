from flask import Flask, render_template, request, redirect, url_for
import session_items as session

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        session.add_item(request.form.get('title'))

    items = session.get_items()
    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run()
