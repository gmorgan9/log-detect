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
#         account_type = "admin" if row[6] == 1 else "standard"
#         capitalized_f_name = row[4].capitalize()
#         capitalized_l_name = row[5].capitalize()
#         full_name = capitalized_f_name + ' ' + capitalized_l_name
#         result.append({
#             'id': row[1],
#             'name': full_name,
#             'username': row[2],
#             'account_type': account_type,
#             'status': row[9]
#         })

#     # Return the data as JSON
#     return jsonify(result)

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
        capitalized_f_name = row[4].capitalize()
        capitalized_l_name = row[5].capitalize()
        full_name = capitalized_f_name + ' ' + capitalized_l_name
        result.append({
            'id': row[1],
            'name': full_name,
            'username': row[2],
            'account_type': account_type,
            'status': row[9]
        })

    # Generate HTML table markup
    table_html = '<table class="table table-striped mx-auto" style="width: 98%;">'
    table_html += '<thead>'
    table_html += '<tr>'
    table_html += '<th class="text-center" style="width: 1px !important;" scope="col"></th>'
    table_html += '<th class=" col-sm-1" scope="col">ID</th>'
    table_html += '<th class="" scope="col">Name</th>'
    table_html += '<th class="" scope="col">Username</th>'
    table_html += '<th class="" scope="col">Account Type</th>'
    table_html += '<th class="" scope="col">Status</th>'
    table_html += '</tr>'
    table_html += '</thead>'
    table_html += '<tbody>'
    for row in result:
        table_html += '<tr>'
        table_html += '<td class="text-center">'
        table_html += '<a class="text-decoration-none text-secondary" href=""><i class="bi bi-eye"></i></a>'
        table_html += '</td>'
        table_html += f'<td class=""><a class="text-decoration-none" href="">#{row["id"]}</a></td>'
        table_html += f'<td>{row["name"]}</td>'
        table_html += f'<td>{row["username"]}</td>'
        table_html += f'<td>{row["account_type"]}</td>'
        table_html += f'<td><span class="badge text-bg-primary">{row["status"]}</span></td>'
        table_html += '</tr>'
    table_html += '</tbody>'
    table_html += '</table>'

    # return table_html
    # Return the index.html template with the table HTML
    return render_template('index.html', table_html=table_html)


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
