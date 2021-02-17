"""Flask application."""

import os
import sqlite3 as sql

from flask import Flask, render_template, request
from flask.helpers import flash, url_for
import pandas as pd
from werkzeug.utils import secure_filename
from werkzeug.utils import redirect

# from src.constant import ALLOWED_EXTENSIONS, COLUMNS, DATABASE, UPLOAD_FOLDER
# from src.query import query

from constant import ALLOWED_EXTENSIONS, COLUMNS, DATABASE, UPLOAD_FOLDER
from query import query


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """Only allow csv files to pass through."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def connect_to_db(db_file):
    """
    Connect to an SQlite database, if db file does not exist it will be created
    :param db_file: absolute or relative path of db file
    :return: sqlite3 connection
    """
    conn = None

    try:
        onn = sql.connect(db_file)
        return conn

    except conn.Error as err:
        print(err)

        if conn is not None:
            conn.close()


def get_column_names_from_db_table(sql_cursor, table_name):
    """
    Scrape the column names from a database table to a list
    :param sql_cursor: sqlite cursor
    :param table_name: table name to get the column names from
    :return: a list with table column names
    """

    table_column_names = 'PRAGMA table_info(' + table_name + ');'
    sql_cursor.execute(table_column_names)
    table_column_names = sql_cursor.fetchall()

    column_names = list()

    for name in table_column_names:
        column_names.append(name[1])

    return column_names
    

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    """Upload files.

    Stores the original file locally
    Applies columns to the files
    Pushes file object downstream to the database
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

        # Run the table creation query
        if file and os.path.exists(os.path.join(app['UPLOAD_FOLDER'], file.filename)):
            conn = connect_to_db(DATABASE)
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute(query)
    
                df = pd.read_csv(os.path.join(app['UPLOAD_FOLDER'], file.filename), names=COLUMNS)

                # data associated with customers
                customers_df = df[
                    [
                        "customer_id",
                        "customer_firstname",
                        "customer_lastname",
                        "customer_street_address",
                        "customer_state",
                        "customer_zip_code",
                        "purchase_status"
                    ]
                ]

                # data associated with products
                products_df = df[
                    [
                        "product_id",
                        "product_name",
                        "purchase_amount",
                        "date_time"
                    ]
                ]

                # get the columns from both tables
                customers_df.columns = get_column_names_from_db_table(cursor, 'customers')
                products_df.columns = get_column_names_from_db_table(cursor, 'products')

                # insert data into the tables
                customers_df.to_sql(name='customers', conn=conn, if_exists='append', index=False)
                products_df.to_sql(name='products', conn=conn, if_exists='append', index=False)

    
                conn.close()
                flash('Table created')
            else:
                flash('connection to database failed')

    return render_template('uploader.html')

if __name__ == "__main__":
    app.run(debug=True)
