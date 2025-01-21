from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)



@app.get('/')
def default_path_func():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM student")
    results = cursor.fetchall()
    return render_template("index.html",students=results)

@app.post("/submit-data")
def post_data_func():
    data = request.get_json()
    firstname = data.get('firstName')
    lastname = data.get('secondName')
    country = data.get('countryName')

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO student(first_name, second_name, country_name) VALUES(%s, %s, %s)", (firstname, lastname, country))
    mysql.connection.commit()
    cursor.close()
    return 'Success'

@app.delete('/delete-record/<int:id>')
def delete_table_data(id):
    try:
        cursor = mysql.connection.cursor()
        # Execute delete query
        cursor.execute("DELETE FROM student WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": f"Record with ID {id} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.put('/edit-record/<int:id>')
def edit_record(id):
    try:
        # Get updated data from the request
        data = request.get_json()
        print("data",data)
        first_name = data.get('firstName')
        last_name = data.get('secondName')
        country_name = data.get('countryName')
       
        # Update the record in the database
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE student
            SET first_name = %s, second_name = %s, country_name = %s
            WHERE id = %s
        """, (first_name, last_name, country_name, id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": f"Record with ID {id} updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get('/get-data')
def get_record():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student")
        results = cursor.fetchall()

        # Initialize an empty list to hold the formatted results
        res = []

        for row in results:
            # Each 'row' is a tuple, so access elements by index
            student = {
                'id': row[0],  # assuming 'id' is the first column
                'firstName': row[1],  # assuming 'first_name' is the second column
                'secondName': row[2],  # assuming 'last_name' is the third column
                'countryName': row[3]  # assuming 'country_name' is the fourth column
            }
            res.append(student)

        return jsonify(res), 200  # Use jsonify to return the data as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)