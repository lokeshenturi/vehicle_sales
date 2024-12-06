from flask import Flask, render_template, request, redirect, jsonify
from utils.db import db
from models.vehicle import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle.db'


@app.route('/')
def index():
    vehicle = Vehicle.query.all()
    return render_template('index.html', content=vehicle)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add_data')
def add_data():
    return render_template('add_data.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    vehicle = Vehicle.query.all()  # ORM query to fetch data
    vehicle = [{
        'id': vehicle.id,
        'name': vehicle.name,
        'model': vehicle.model,
        'year': vehicle.year,
        'transmission': vehicle.transmission,
    } for vehicle in vehicle]
    return render_template('dashboard.html', content=vehicle)

@app.route('/help')
def help():
    return render_template('help.html')


db.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")

    id = form_data.get('id')
    name = form_data.get('name')
    model = form_data.get('model')
    year = form_data.get('year')
    transmission = form_data.get('transmission')

    vehicle= Vehicle.query.filter_by(id=id).first()
    if not vehicle:
        vehicle = Vehicle(id=id, name=name,model=model, year=year, transmission=transmission)
        db.session.add(vehicle)
        db.session.commit()
    print("submitted successfully")
    return redirect('/')

@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete(id):
    vehicle = Vehicle.query.get(id)
    print("task: {}".format(vehicle.id))

    if not vehicle:
        return jsonify({'message': 'vehicle not found'}), 404
    try:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({'message': 'vehicle deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the data {}'.format(e)}), 500

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
        vehicle = Vehicle.query.get_or_404(id)
        print(vehicle.id)
        if not vehicle:
            return jsonify({'message': 'vehicle not found'}), 404

        if request.method == 'POST':
            vehicle.id = request.form['id']
            vehicle.name = request.form['name']
            vehicle.model = request.form['model']
            vehicle.year = request.form['year']
            vehicle.transmission = request.form['transmission']

            try:
                db.session.commit()
                return redirect('/')

            except Exception as e:
                db.session.rollback()
                return "there is an issue while updating the record"
        return render_template('update.html', vehicle=vehicle)





if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=2000,
        debug=True
    )