from flask import Flask, request, jsonify, redirect, session, render_template
import psycopg2
from flask_session import Session
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '6d5b6348fad22778e627f12fe5084bab06a4b830804814d1'  # Replace with your secret key
Session(app)


conn = psycopg2.connect(database="logdetect", user="DBadmin", password="DBadmin123!", host="192.168.1.183", port="5432")

@app.route('/api/data', methods=['GET'])
@cross_origin()
def get_data():
    # Fetch data from the database
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    data = cur.fetchall()
    cur.close()

    # Convert the data to a list of dictionaries
    result = []
    for row in data:
        account_type = "Admin" if row[6] == 1 else "Standard"
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

# def insert_snort_alert(data):
#     # connection = create_db_connection()
#     cursor = conn.cursor()
#     # query = """
#     #     INSERT INTO snort_alerts (seconds, action, class, dir, dst_addr, dst_ap, dst_port, eth_dst,
#     #                               eth_len, eth_src, eth_type, gid, iface, ip_id, ip_len, msg, mpls,
#     #                               pkt_gen, pkt_len, pkt_num, priority, proto, rev, rule, service,
#     #                               sid, src_addr, src_ap, src_port, tcp_ack, tcp_flags, tcp_len,
#     #                               tcp_seq, tcp_win, tos, ttl, vlan, timestamp)
#     #     VALUES (%(seconds)s, %(action)s, %(class)s, %(dir)s, %(dst_addr)s, %(dst_ap)s, %(dst_port)s, %(eth_dst)s,
#     #             %(eth_len)s, %(eth_src)s, %(eth_type)s, %(gid)s, %(iface)s, %(ip_id)s, %(ip_len)s, %(msg)s, %(mpls)s,
#     #             %(pkt_gen)s, %(pkt_len)s, %(pkt_num)s, %(priority)s, %(proto)s, %(rev)s, %(rule)s, %(service)s,
#     #             %(sid)s, %(src_addr)s, %(src_ap)s, %(src_port)s, %(tcp_ack)s, %(tcp_flags)s, %(tcp_len)s,
#     #             %(tcp_seq)s, %(tcp_win)s, %(tos)s, %(ttl)s, %(vlan)s, %(timestamp)s)
#     # """

#     query = """
#         INSERT INTO alerts (seconds, action, class, timestamp)
#         VALUES (%(seconds)s, %(action)s, %(class)s, %(timestamp)s)
#     """
#     cursor.execute(query, data)
#     conn.commit()
#     cursor.close()
#     conn.close()

def insert_snort_alert(data, conn):
    cursor = conn.cursor()
    
    query = """
        INSERT INTO alerts (seconds, action, class, timestamp)
        VALUES (%(seconds)s, %(action)s, %(class)s, %(timestamp)s)
    """
    cursor.execute(query, data)
    conn.commit()
    cursor.close()


# SNORT ALERTS
import json

@app.route('/snort-alerts', methods=['POST'])
def process_snort_alerts():
    try:
        with open('/var/log/snort/alert_json.txt', 'r') as file:
            alerts = json.load(file)

        # connection = create_db_connection()  # Assuming you have a function to create the database connection

        for alert in alerts:
            insert_snort_alert(alert, conn)

        conn.close()

        return 'Snort alert data added to the database.', 200
    except Exception as e:
        return str(e), 400



if __name__ == '__main__':
    app.run(host="192.168.1.183")
