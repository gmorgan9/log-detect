from flask import Flask, request, jsonify, redirect, session
import psycopg2
from flask_session import Session
from flask_cors import CORS
from flask_cors import cross_origin
from datetime import datetime
import pytz
import random

app = Flask(__name__)
cors = CORS(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '6d5b6348fad22778e627f12fe5084bab06a4b830804814d1'  # Replace with your secret key
Session(app)


conn = psycopg2.connect(database="logdetect", user="DBadmin", password="DBadmin123!", host="192.168.1.183", port="5432")

################ UPDATED ##################
@app.route('/api/data', methods=['GET'])
@cross_origin()
def get_data():
    conn = psycopg2.connect(database="logdetect", user="DBadmin", password="DBadmin123!", host="192.168.1.183", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    data = cur.fetchall()
    cur.close()

    result = []
    for row in data:
        account_type = "Admin" if row[10] == 1 else "Standard"
        status = "Logged In" if row[7] == 1 else "Logged Out"
        capitalized_f_name = row[2].capitalize()
        capitalized_l_name = row[3].capitalize()
        full_name = capitalized_f_name + ' ' + capitalized_l_name
        result.append({
            'id': row[1],
            'name': full_name,
            'username': row[5],
            'email': row[4],
            'account_type': account_type,
            'status': status
        })
    return jsonify(result)
################ CLOSE UPDATED ##################


@app.route('/api/logs', methods=['GET'])
@cross_origin()
def get_logs():
    # Fetch data from the database
    conn = psycopg2.connect(database="logdetect", user="DBadmin", password="DBadmin123!", host="192.168.1.183", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM logs;")
    data = cur.fetchall()
    cur.close()

    import datetime

    # Convert the data to a list of dictionaries
    result = []
    for row in data:
        priority_mapping = {
            1: "Critical",
            2: "High",
            3: "Medium",
            4: "Low"
        }
        message_string = json.dumps(row[39], indent=4)
        formatted_timestamp = row[38].strftime('%Y-%m-%dT%H:%M:%S')
        priority = priority_mapping.get(row[21], "Unknown")
        result.append({
            'id': row[0],
            'description': row[16],
            'timestamp': formatted_timestamp,
            'target': row[5],
            'priority': priority,
            'message': message_string
        })

    # Return the data as JSON
    return jsonify(result)

# Get Alerts
@app.route('/api/alerts', methods=['GET'])
@cross_origin()
def get_alerts():
    # Fetch data from the database
    conn = psycopg2.connect(database="logdetect", user="DBadmin", password="DBadmin123!", host="192.168.1.183", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM alerts;")
    data = cur.fetchall()
    cur.close()

    import datetime

    # Convert the data to a list of dictionaries
    result = []
    for row in data:
        priority_mapping = {
            1: "Critical",
            2: "High",
            3: "Medium",
            4: "Low"
        }
        status_mapping = {
            1: "New",
            2: "Open",
            3: "Pending",
            4: "Closed"
        }
        message_string = json.dumps(row[7], indent=4)
        formatted_timestamp = row[6].strftime('%Y-%m-%dT%H:%M:%SZ')
        priority = priority_mapping.get(row[3], "Unknown")
        status = status_mapping.get(row[2], "Unknown")
        new_description = "[" + priority + "]Alert: " + row[4]
        result.append({
            'id': row[1],
            'status': status,
            'description': new_description,
            'requested': formatted_timestamp,
            # 'target': row[5],
            'priority': priority,
            'message': message_string,
            'log_id': row[10]
        })

    # Return the data as JSON
    return jsonify(result)


@app.route('/api/focus/<alertId>', methods=['GET'])
@cross_origin()
def get_alert_focus(alertId):
    # Fetch data for the specific ticket from the database
    conn = psycopg2.connect(database="logdetect", user="DBadmin", password="DBadmin123!", host="192.168.1.183", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM alerts WHERE idno = %s;", (alertId,))
    data = cur.fetchone()
    cur.close()

    # if data is None:
    #     return jsonify({'error': 'Alert not found'}), 404

    # priority_mapping = {
    #     1: "Critical",
    #     2: "High",
    #     3: "Medium",
    #     4: "Low"
    # }
    # status_mapping = {
    #     1: "New",
    #     2: "Open",
    #     3: "Pending",
    #     4: "Closed"
    # }
    # message_string = json.dumps(data[7], indent=4)
    # formatted_timestamp = data[6].strftime('%Y-%m-%dT%H:%M:%SZ')
    # priority = priority_mapping.get(data[3], "Unknown")
    # status = status_mapping.get(data[2], "Unknown")
    # new_description = "[" + priority + "] Alert: " + data[4]

    # alert = {
    #     'id': data[1],
    #     'status': status,
    #     'description': new_description,
    #     'requested': formatted_timestamp,
    #     'priority': priority,
    #     'message': message_string,
    #     'log_id': data[10]
    # }


    # Return the ticket data as JSON
    # return jsonify(alert)
    return "hello"






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
        session['logged_in'] = False
        cur = conn.cursor()
        cur.execute("UPDATE users SET loggedin = 0 WHERE username = %s", (username,))
        conn.commit()
        cur.close()

        # Clear the session data
        session.clear()

    # Redirect the user to the login page
    return redirect('https://logdetect.morganserver.com/core/entry/login')


# @app.route('/insert_alert', methods=['POST'])
# def insert_alert():
#     # Connect to the database
#     conn = psycopg2.connect(database="logdetect", user="DBadmin", password="DBadmin123!", host="192.168.1.183", port="5432")
#     cursor = conn.cursor()

#     log_id = request.form['log_id']
#     select_query = "SELECT priority, msg FROM logs WHERE id = %s"
#     cursor.execute(select_query, (log_id,))
#     result = cursor.fetchone()

#     if result:
#         # Check if the log ID already exists in the alerts table
#         check_query = "SELECT COUNT(*) FROM alerts WHERE log_id = %s"
#         cursor.execute(check_query, (log_id,))
#         count = cursor.fetchone()[0]

#         if count == 0:  # Log ID doesn't exist in the alerts table, proceed with insertion
#             priority = result[0]
#             description = result[1]
#             status = 2

#             # Insert the data into the alerts table
#             insert_query = "INSERT INTO alerts (log_id, priority, description, status) VALUES (%s, %s, %s, %s)"
#             cursor.execute(insert_query, (log_id, priority, description, status,))

#             # Commit the changes
#             conn.commit()

#             # Delete the log from the logs table
#             delete_query = "DELETE FROM logs WHERE id = %s"
#             cursor.execute(delete_query, (log_id,))

#             # Commit the deletion
#             conn.commit()

#             cursor.close()
#             conn.close()

#             return redirect('https://logdetect.morganserver.com/core/logs')
#         else:
#             # Log ID already exists in the alerts table, skip insertion
#             cursor.close()
#             conn.close()
#             return 'Log ID already exists in the alerts table'
#     else:
#         cursor.close()
#         conn.close()
#         return 'Log ID not found'

import os
import json

@app.route('/insert_alert', methods=['POST'])
def insert_alert():
    # Connect to the database
    conn = psycopg2.connect(database="logdetect", user="DBadmin", password="DBadmin123!", host="192.168.1.183", port="5432")
    cursor = conn.cursor()

    log_id = request.form['log_id']
    # log_seconds = request.form['log_seconds']
    select_query = "SELECT seconds, priority, msg FROM logs WHERE id = %s"
    cursor.execute(select_query, (log_id,))
    result = cursor.fetchone()

    if result:
        # Check if the log seconds already exist in the alerts table
        check_query = "SELECT COUNT(*) FROM alerts WHERE log_id = %s"
        cursor.execute(check_query, (log_id,))
        count = cursor.fetchone()[0]

        if count == 0:  # Log seconds doesn't exist in the alerts table, proceed with insertion
            seconds = result[0]
            priority = result[1]
            description = result[2]
            status = 2

            # Generate the next idno value
            next_idno = generate_next_idno(cursor)

            # Insert the data into the alerts table
            insert_query = "INSERT INTO alerts (idno, seconds, priority, description, status) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (next_idno, seconds, priority, description, status,))

            # Commit the changes
            conn.commit()

            # Delete the log from the logs table
            delete_query = "DELETE FROM logs WHERE seconds = %s"
            cursor.execute(delete_query, (seconds,))

            # Commit the deletion
            conn.commit()

            # Delete the line from the file
            file_path = '/var/log/snort/alert_json.txt'
            delete_line_from_file(file_path, seconds)

            cursor.close()
            conn.close()

            return redirect('https://logdetect.morganserver.com/core/logs')
        else:
            # Log seconds already exist in the alerts table, skip insertion
            cursor.close()
            conn.close()
            return 'Log seconds already exist in the alerts table'
    else:
        cursor.close()
        conn.close()
        return 'Log seconds not found'
    
def generate_next_idno(cursor):
    select_query = "SELECT MAX(idno) FROM alerts"
    cursor.execute(select_query)
    result = cursor.fetchone()[0]
    if result:
        max_idno = int(result)
        next_idno = str(max_idno + 1).zfill(6)
    else:
        next_idno = '000001'
    return next_idno

def delete_line_from_file(file_path, log_seconds):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                log_data = json.loads(line)
                if 'seconds' in log_data and log_data['seconds'] == log_seconds:
                    continue
            except json.JSONDecodeError:
                pass
            lines.append(line)
    with open(file_path, 'w') as file:
        file.writelines(lines)






import json

# Endpoint to handle the JSON data from the file and insert it into the PostgreSQL database
@app.route('/insert_log', methods=['POST'])
def insert_log():
    # Read the JSON data from the file
    with open('/var/log/snort/alert_json.txt', 'r') as file:
        for line in file:
            try:
                json_data = json.loads(line)
                # print(json_data)
                # Extract the data from the JSON object
                # idno = random.randint(100000, 999999)
                # message = json_data
                seconds = json_data['seconds']
                action = json_data['action']
                class_name = json_data['class']
                dir = json_data['dir']
                dst_addr = json_data['dst_addr']
                dst_ap = json_data['dst_ap']
                dst_port = json_data['dst_port']
                eth_dst = json_data['eth_dst']
                eth_len = json_data['eth_len']
                eth_src = json_data['eth_src']
                eth_type = json_data['eth_type']
                gid = json_data['gid']
                iface = json_data['iface']
                ip_id = json_data['ip_id']
                ip_len = json_data['ip_len']
                msg = json_data['msg']
                mpls = json_data['mpls']
                pkt_gen = json_data['pkt_gen']
                pkt_len = json_data['pkt_len']
                pkt_num = json_data['pkt_num']
                priority = json_data['priority']
                proto = json_data['proto']
                rev = json_data['rev']
                rule = json_data['rule']
                service = json_data['service']
                sid = json_data['sid']
                src_addr = json_data['src_addr']
                src_ap = json_data['src_ap']
                src_port = json_data['src_port']
                tcp_ack = json_data['tcp_ack']
                tcp_flags = json_data['tcp_flags']
                tcp_len = json_data['tcp_len']
                tcp_seq = json_data['tcp_seq']
                tcp_win = json_data['tcp_win']
                tos = json_data['tos']
                ttl = json_data['ttl']
                vlan = json_data['vlan']
                timestamp = json_data['timestamp']


                # Extract other fields as needed
                # idno_str = str(idno)
                conn = psycopg2.connect(database="logdetect", user="DBadmin", password="DBadmin123!", host="192.168.1.183", port="5432")
                # Create a cursor object to interact with the database
                cursor = conn.cursor()

                # Convert the timestamp to the desired format
                local_datetime = datetime.strptime(timestamp, '%m/%d-%H:%M:%S.%f').replace(year=datetime.now().year)
                local_datetime = local_datetime.replace(tzinfo=pytz.UTC)
                new_timestamp = local_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')

                # Check if the alert with the same timestamp already exists in the database
                select_query = "SELECT COUNT(*) FROM logs WHERE timestamp = %s"
                cursor.execute(select_query, (new_timestamp,))
                count = cursor.fetchone()[0]

                if count > 0:
                    # Alert already exists, skip inserting
                    continue

                # Define the SQL query to insert the data into the database
                insert_query = "INSERT INTO logs (seconds, action, class, dir, dst_addr, dst_ap, dst_port, eth_dst, eth_len, eth_src, eth_type, gid, iface, ip_id, ip_len, msg, message, mpls, pkt_gen, pkt_len, pkt_num, priority, proto, rev, rule, service, sid, src_addr, src_ap, src_port, tcp_ack, tcp_flags, tcp_len, tcp_seq, tcp_win, tos, ttl, vlan, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                # Execute the SQL query with the data
                cursor.execute(insert_query, (seconds, action, class_name, dir, dst_addr, dst_ap, dst_port, eth_dst, eth_len, eth_src, eth_type, gid, iface, ip_id, ip_len, msg, json.dumps(json_data), mpls, pkt_gen, pkt_len, pkt_num, priority, proto, rev, rule, service, sid, src_addr, src_ap, src_port, tcp_ack, tcp_flags, tcp_len, tcp_seq, tcp_win, tos, ttl, vlan, new_timestamp))

                # Commit the changes to the database
                conn.commit()

                # Close the cursor and database connection
                cursor.close()
                conn.close()

            except json.JSONDecodeError:
                # Handle JSON decoding errors if any
                continue

    return 'Logs inserted into the database'











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

# import json

# json_data = '''
# {
#   "seconds": 1684013469,
#   "action": "allow",
#   "class": "Attempt to login by a known username and password",
#   "dir": "C2S",
#   "dst_addr": "192.168.1.183",
#   "dst_ap": "192.168.1.183:22",
#   "dst_port": 22,
#   "eth_dst": "06:B0:F8:9F:00:B7",
#   "eth_len": 78,
#   "eth_src": "A4:83:E7:5B:F5:9F",
#   "eth_type": "0x800",
#   "gid": 1,
#   "iface": "eth0",
#   "ip_id": 0,
#   "ip_len": 44,
#   "msg": "SSH Login Attempt",
#   "mpls": 0,
#   "pkt_gen": "raw",
#   "pkt_len": 64,
#   "pkt_num": 5263650,
#   "priority": 3,
#   "proto": "TCP",
#   "rev": 0,
#   "rule": "1:1000001:0",
#   "service": "unknown",
#   "sid": 1000001,
#   "src_addr": "192.168.1.185",
#   "src_ap": "192.168.1.185:61172",
#   "src_port": 61172,
#   "tcp_ack": 0,
#   "tcp_flags": "******S*",
#   "tcp_len": 44,
#   "tcp_seq": 2522252635,
#   "tcp_win": 65535,
#   "tos": 0,
#   "ttl": 64,
#   "vlan": 0,
#   "timestamp": "05/13-21:31:09.052870"
# }
# '''
# seconds = data['seconds']
#             action = data['action']
#             class_ = data['class']
#             dir_ = data['dir']
#             dst_addr = data['dst_addr']
#             dst_ap = data['dst_ap']
#             dst_port = data['dst_port']
#             eth_dst = data['eth_dst']
#             eth_len = data['eth_len']
#             eth_src = data['eth_src']
#             eth_type = data['eth_type']
#             gid = data['gid']
#             iface = data['iface']
#             ip_id = data['ip_id']
#             ip_len = data['ip_len']
#             msg = data['msg']
#             mpls = data['mpls']
#             pkt_gen = data['pkt_gen']
#             pkt_len = data['pkt_len']
#             pkt_num = data['pkt_num']
#             priority = data['priority']
#             proto = data['proto']
#             rev = data['rev']
#             rule = data['rule']
#             service = data['service']
#             sid = data['sid']
#             src_addr = data['src_addr']
#             src_ap = data['src_ap']
#             src_port = data['src_port']
#             tcp_ack = data['tcp_ack']
#             tcp_flags = data['tcp_flags']
#             tcp_len = data['tcp_len']
#             tcp_seq = data['tcp_seq']
#             tcp_win = data['tcp_win']
#             tos = data['tos']
#             ttl = data['ttl']
#             vlan = data['vlan']
#             timestamp = data['timestamp']

# data = json.loads(json_data)






if __name__ == '__main__':
    app.run(host="192.168.1.183")
