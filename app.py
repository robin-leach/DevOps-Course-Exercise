from flask import Flask, render_template, request, redirect, url_for, jsonify
import session_items as session
from exceptions import Error

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.errorhandler(Error)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        form_type = request.form.get('form_id')

        if form_type == 'add-item':
            title = request.form.get('title')
            if title:
                session.add_item(title)
            else:
                raise Error('Item title is required')

        elif form_type == 'update-item':
            id = request.form.get('item_id')
            if id:
                item = session.get_item(id)
                if item:
                    updated_status = 'Not Started' if item['status'] == 'Done' else 'Done'
                    updated_item = { 'id': item['id'], 'status': updated_status, 'title': item['title'] }
                    session.save_item(updated_item)
                else:
                    raise Error('No item found with id ' + id)
        
        else:
            raise Error('Invalid request')

    items = session.get_items()
    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run()
