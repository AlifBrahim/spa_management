from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import mysql.connector

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'SECRET_KEY'

# MySQL database details
db_host = 'cctmcagenda2.mysql.database.azure.com'
db_port = 3306
db_user = 'alif'
db_password = 'alep1234!'
db_name = 'spa'

class TreatmentForm(FlaskForm):
    name = StringField('Name of Treatment', validators=[DataRequired()])
    category = SelectField('Category of Treatment', choices=[('Category 1', 'Category 1'), ('Category 2', 'Category 2')])
    description = TextAreaField('Treatment Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Add New')

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/manage-treatment-records')
def manage_treatment_records():
    return render_template('manage_treatment_records.html')

@app.route('/add-treatment', methods=['GET', 'POST'])
def add_treatment():
    form = TreatmentForm()
    if form.validate_on_submit():
        # Save treatment details to database
        name = form.name.data
        category = form.category.data
        description = form.description.data
        price = form.price.data

        # Connect to the MySQL database
        cnx = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = cnx.cursor()

        # Execute the SQL query to insert treatment details
        query = "INSERT INTO treatment_record (name, category, description, price) VALUES (%s, %s, %s, %s)"
        values = (name, category, description, price)
        cursor.execute(query, values)

        # Commit the changes and close the database connection
        cnx.commit()
        cursor.close()
        cnx.close()

        return redirect(url_for('treatment_added'))
    return render_template('add-treatment.html', form=form)

@app.route('/treatment_added')
def treatment_added():
    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = cnx.cursor()

    # Execute the SQL query to fetch treatment records
    query = "SELECT * FROM treatment_record"
    cursor.execute(query)

    # Fetch all treatment records from the cursor
    treatments = []
    for row in cursor.fetchall():
        treatment = {
            'id': row[0],
            'name': row[1],
            'category': row[2],
            'description': row[3],
            'price': row[4]
        }
        treatments.append(treatment)

    # Close the database connection and cursor
    cursor.close()
    cnx.close()

    return render_template('treatment_added.html', treatments=treatments)


if __name__ == '__main__':
    app.run()
