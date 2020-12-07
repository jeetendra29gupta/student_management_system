from flask import Flask, render_template, request
import sqlite3 as sql
import logging
from datetime import datetime

logging.basicConfig(filename='student.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    try:
        with sql.connect("database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            app.logger.info('All Student are selected')
            return render_template("index.html", rows=rows)
    except Exception as ex:
        error_message = "Error in select operation --> ", ex
        app.logger.error(error_message)
        return render_template("result.html", error_message=error_message)
    finally:
        con.close()


@app.route('/dateTime')
def date_time():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")


@app.route('/addStudent')
def add_student():
    return render_template("addStudent.html")


@app.route('/save', methods=['POST'])
def save_student():
    name = request.form['name']
    mail = request.form['mail']
    phone = request.form['phone']
    semester = request.form['semester']
    subject = request.form['subject']
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO student (name,email,phone,semester,subject) VALUES(?,?,?,?,?)",
                        (name, mail, phone, semester, subject))
            con.commit()
            success_message = "Record successfully added"
            app.logger.info(success_message)
            return render_template("result.html", success_message=success_message)
    except Exception as ex:
        con.rollback()
        error_message = "Error in insert operation :: ", ex
        app.logger.error(error_message)
        return render_template("result.html", error_message=error_message)
    finally:
        con.close()


@app.route('/delete/<int:id_no>')
def delete_student(id_no):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM student WHERE id=?", (id_no,))
            con.commit()
            success_message = "Record successfully deleted"
            app.logger.info(success_message)
            return render_template("result.html", success_message=success_message)
    except Exception as ex:
        con.rollback()
        error_message = "Error in delete operation :: ", ex
        app.logger.error(error_message)
        return render_template("result.html", error_message=error_message)
    finally:
        con.close()


@app.route('/edit/<int:id_no>')
def edit_student(id_no):
    try:
        with sql.connect("database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM student WHERE id=?", (id_no,))
            rows = cur.fetchall()
            app.logger.info('Student with given id is selected', id_no)
            return render_template("editStudent.html", rows=rows)
    except Exception as ex:
        error_message = "Error in select operation --> ", ex
        app.logger.error(error_message)
        return render_template("result.html", error_message=error_message)
    finally:
        con.close()


@app.route('/update', methods=['POST'])
def update_student():
    id_no = request.form['id']
    name = request.form['name']
    email = request.form['mail']
    phone = request.form['phone']
    semester = request.form['semester']
    subject = request.form['subject']
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE student SET name=?, email=?, phone=?, semester=?, subject=? WHERE id=?",
                        (name, email, phone, semester, subject, id_no))
            con.commit()
            success_message = "Record successfully updated"
            app.logger.info(success_message)
            return render_template("result.html", success_message=success_message)
    except Exception as ex:
        con.rollback()
        error_message = "Error in update operation :: ", ex
        app.logger.error(error_message)
        return render_template("result.html", error_message=error_message)
    finally:
        con.close()


if __name__ == '__main__':
    conn = sql.connect('database.db')
    app.logger.info("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS student '
                 '(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL,'
                 'phone TEXT NOT NULL, semester TEXT NOT NULL, subject TEXT NOT NULL)')
    app.logger.info("Table created successfully")
    conn.close()
    app.run(debug=True)
