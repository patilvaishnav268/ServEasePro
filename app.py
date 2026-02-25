from flask import Flask, render_template, request, redirect, session, flash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = "secret123"


# HOME PAGE
@app.route('/')
def home():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()

    conn.close()

    return render_template("home.html", services=services)


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name,email,password,phone) VALUES (%s,%s,%s,%s)",
            (name, email, password, phone)
        )

        conn.commit()
        conn.close()

        flash("Registration Successful")
        return redirect('/login')

    return render_template("register.html")


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['user_id'] = user['id']
            session['user_name'] = user['name']

            flash("Login Successful")
            return redirect('/')

        else:
            flash("Invalid Email or Password")

    return render_template("login.html")


# LOGOUT
@app.route('/logout')
def logout():

    session.clear()
    flash("Logged out")
    return redirect('/')


# SERVICE DETAILS
@app.route('/service/<int:id>')
def service_details(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM services WHERE id=%s", (id,))
    service = cursor.fetchone()

    conn.close()

    return render_template("service_details.html", service=service)


# BOOK SERVICE
@app.route('/book/<int:service_id>')
def book(service_id):

    if 'user_id' not in session:
        flash("Please login first")
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO bookings (user_id, service_id) VALUES (%s,%s)",
        (session['user_id'], service_id)
    )

    conn.commit()
    conn.close()

    flash("Service Booked Successfully")

    return redirect('/')


# RUN
if __name__ == "__main__":
    app.run(debug=True)