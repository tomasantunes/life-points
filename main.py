from flask import Flask, render_template, request
import datetime
import sqlite3

app = Flask(__name__)

def exportUsersMarkdown():
    connection = sqlite3.connect('life_points.db')
    cur = connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    with open("Life Points.md", "w", encoding="utf8") as f:
        file_string = "# Life Points\n\n"
        for user in users:
            file_string += "## " + user[1] + "\n"
            file_string += "- " + str(user[2]) + "\n\n"
        f.write(file_string)

@app.route("/submit-points")
def submitPoints():
    connection = sqlite3.connect('life_points.db')
    cur = connection.cursor()

    id = request.args.get("id")
    value = int(request.args.get("value"))
    justification = request.args.get("justification")
    time = str(datetime.datetime.now().replace(microsecond=0))
    cur.execute("SELECT name FROM users WHERE id = ?", (id,))
    name = cur.fetchone()[0]

    point_text = ""
    if value == 1:
        point_text = "Positive point to " + name
    elif value > 1:
        point_text = str(value) + " positive points to " + name
    elif value == -1:
        point_text = "Negative point to " + name
    elif value < -1:
        point_text = str(value) + " negative points to " + name

    cur.execute("UPDATE users SET points = points + ? WHERE id = ?", (value, id))
    cur.execute("INSERT INTO transactions (created, user_id, point_text, justification, value) VALUES (?, ?, ?, ?, ?)", (time, id, point_text, justification, value))

    connection.commit()
    connection.close()

    log_file = open("life-points-log.md", "a", encoding="utf8")
    log_file.write("- " + time + " - " + point_text + " - " + justification + "\n")
    log_file.close()
    exportUsersMarkdown()

    return "OK"

@app.route("/add-user")
def addUser():
    name = request.args.get("name")
    connection = sqlite3.connect('life_points.db')

    cur = connection.cursor()

    user = {"name": name, "value": 0}
    cur.execute("INSERT INTO users (name, points) VALUES (?, ?)", (user['name'], user['value']))

    connection.commit()
    connection.close()
    exportUsersMarkdown()

    return "OK"

@app.route("/add-user-form")
def addUserForm():
    return render_template("add-user-form.html")

@app.route("/daily-balance")
def dailyBalance():
    connection = sqlite3.connect('life_points.db')
    cur = connection.cursor()

    cur.execute("SELECT * FROM transactions WHERE date(created) = date('now')")
    points = cur.fetchall()

    positive = 0
    negative = 0
    for point in points:
        print(point[5])
        if point[5] > 0:
            positive += point[5]
        elif point[5] < 0:
            negative += abs(point[5])

    total = positive - negative

    connection.close()

    return render_template("daily-balance.html", total=total, positive=positive, negative=negative)

@app.route("/")
def home():
    connection = sqlite3.connect('life_points.db')
    cur = connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.execute("SELECT SUM(points) from users")
    total = cur.fetchone()[0]
    connection.close()

    return render_template("index.html", users=users, total=total)

if __name__ == "__main__":
    app.run()