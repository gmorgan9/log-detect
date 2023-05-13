from flask import Flask, request, jsonify, redirect, session, render_template
import psycopg2
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '6d5b6348fad22778e627f12fe5084bab06a4b830804814d1'  # Replace with your secret key
Session(app)


conn = psycopg2.connect(database="logdetect", user="DBadmin", password="DBadmin123!", host="192.168.1.183", port="5432")

# @app.route('/api/data', methods=['GET'])
# def get_data():
#     # Fetch data from the database
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM users;")
#     data = cur.fetchall()
#     cur.close()

#     # Return the data as JSON
#     return jsonify(data)

# @app.route('/api/data', methods=['GET'])
# def get_data():
#     # Fetch data from the database
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM users;")
#     data = cur.fetchall()
#     cur.close()

#     # Convert the data to a list of dictionaries
#     result = []
#     for row in data:
#         result.append({
#             'id': row[0],
#             'name': row[1],
#             'username': row[2],
#             'account_type': row[3],
#             'status': row[4]
#         })

#     # Return the data as JSON
#     return jsonify(result)

# format: [[1,"63724","garrett","test","garrett","morgan",0,1,"Fri, 12 May 2023 04:29:27 GMT","pending",1]]
@app.route('/api/data', methods=['GET'])
def get_data():
    # Fetch data from the database
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    data = cur.fetchall()
    cur.close()

    # Convert the data to a list of dictionaries
    result = []
    for row in data:
        account_type = "admin" if row[6] == 1 else "standard"
        full_name = row[4] + ' ' + row[5]
        capitalized_full_name = full_name.capitalize()
        result.append({
            'id': row[1],
            'name': capitalized_full_name,
            'username': row[2],
            'account_type': account_type,
            'status': row[9]
        })

    # Return the data as JSON
    return jsonify(result)

@app.route('/api/login', methods=['POST'])
def login():
    # Get the form data
    username = request.form.get('username')
    password = request.form.get('password')

    # Perform authentication
    authenticated = False

    # Query the database to check the username and password combination
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE username = %s AND password = %s", (username, password))
    count = cur.fetchone()[0]

    if count == 1:
        authenticated = True
        session['username'] = username
        session['loggedin'] = True
        cur.execute("UPDATE users SET loggedin = 1 WHERE username = %s", (username,))
        conn.commit()

    cur.close()

    # Return a response based on the authentication result
    if authenticated:
        session['logged_in'] = True
        return redirect('https://logdetect.morganserver.com/core/home/')
    else:
        session['logged_in'] = False
        return redirect('https://logdetect.morganserver.com/core/entry/login/')

@app.route('/api/logout', methods=['POST'])
def logout():
    # Check if the user is logged in
    if 'username' in session:
        # Update the 'loggedin' status to 0 in the database
        username = session['username']
        cur = conn.cursor()
        cur.execute("UPDATE users SET loggedin = 0 WHERE username = %s", (username,))
        conn.commit()
        cur.close()

        # Clear the session data
        session.clear()

    # Redirect the user to the login page
    return redirect('https://logdetect.morganserver.com/core/entry/login')

if __name__ == '__main__':
    app.run(host="192.168.1.183")
