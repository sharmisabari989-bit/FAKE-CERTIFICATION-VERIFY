from flask import Flask, render_template, request
import psycopg2
import qrcode
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    return conn

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student_name = request.form["student_name"]
        register_number = request.form["register_number"]
        email = request.form["email"]
        course = request.form["course"]
        college_name = request.form["college_name"]
        issue_date = request.form["issue_date"]

        certificate_id = "CERT" + str(int(__import__("time").time()))
        qr = qrcode.make(
            f"http://194.168.13.146:5000/verify/{certificate_id}"
        )

        qr_path = f"static/{certificate_id}.png"
        qr.save(qr_path)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO certificates
            (certificate_id, student_name, register_number, email, course, college_name, issue_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            certificate_id,
            student_name,
            register_number,
            email,
            course,
            college_name,
            issue_date
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return render_template(
            "success.html",
            certificate_id=certificate_id
        )

    return render_template("register.html")
@app.route("/generate_qr/<certificate_id>")
def generate_qr(certificate_id):
    qr = qrcode.make(
        f"http://194.168.13.146:5000/verify/{certificate_id}"
    )

    qr_path = f"static/{certificate_id}.png"
    qr.save(qr_path)

    return f"QR Code generated successfully: {qr_path}"
@app.route("/verify/<certificate_id>")
def verify_qr(certificate_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT certificate_id, student_name, register_number,
               email, course, college_name, issue_date
        FROM certificates
        WHERE certificate_id = %s
    """, (certificate_id,))

    certificate = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "verify.html",
        certificate=certificate,
        verified=True
    )
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        certificate_id = request.form["certificate_id"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT certificate_id, student_name, register_number,
                   email, course, college_name, issue_date
            FROM certificates
            WHERE certificate_id = %s
        """, (certificate_id,))

        certificate = cursor.fetchone()

        cursor.close()
        conn.close()

        if certificate:
            return render_template(
                "verify.html",
                certificate=certificate,
                verified=True
            )
        else:
            return render_template(
                "verify.html",
                certificate=None,
                verified=True
            )

    return render_template("verify.html")
@app.route("/test-db")
def test_db():
    conn = get_db_connection()
    conn.close()
    return "PostgreSQL Connected Successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)