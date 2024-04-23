from flask import Flask, request, render_template
from flask_mysqldb import MySQL

# Flask app setup
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Gj3Mm8774'
app.config['MYSQL_DB'] = 'dcc'

mysql = MySQL(app)

@app.route('/redemption', methods=["GET", "POST"])
def redemption_page():
    bond_number = request.form.get("Bond_Number", "")

    # Fetch distinct political parties for drop-down options
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT DISTINCT `Name of the Political Party` FROM eb_redemption_details WHERE `Bond Number` LIKE %s",
        (f"%{bond_number}%",)
    )
    political_parties = [row[0] for row in cursor.fetchall()]
    cursor.close()

    redemption_data = None

    if request.method == "POST":
        political_party_filter = request.form.get("Political_Party", "")

        # Fetch filtered redemption data
        redemption_query = "SELECT * FROM eb_redemption_details WHERE `Bond Number` LIKE %s"
        redemption_params = [f"%{bond_number}%"]

        if political_party_filter:
            redemption_query += " AND `Name of the Political Party` = %s"
            redemption_params.append(political_party_filter)

        cursor = mysql.connection.cursor()
        cursor.execute(redemption_query, tuple(redemption_params))
        redemption_data = cursor.fetchall()
        cursor.close()

    return render_template(
        "redemption.html",
        redemption_details=redemption_data,
        political_parties=political_parties,
        bond_number=bond_number
    )


@app.route('/purchase', methods=["GET", "POST"])
def purchase_page():
    bond_number = request.form.get("Bond_Number", "")

    # Fetch distinct purchasers for drop-down options
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT DISTINCT `Name of the Purchaser` FROM eb_purchase_details WHERE `Bond Number` LIKE %s",
        (f"%{bond_number}%",)
    )
    purchasers = [row[0] for row in cursor.fetchall()]
    cursor.close()

    purchase_data = None

    if request.method == "POST":
        purchaser_filter = request.form.get("Purchaser", "")

        # Fetch filtered purchase data
        purchase_query = "SELECT * FROM eb_purchase_details WHERE `Bond Number` LIKE %s"
        purchase_params = [f"%{bond_number}%"]

        if purchaser_filter:
            purchase_query += " AND `Name of the Purchaser` = %s"
            purchase_params.append(purchaser_filter)

        cursor = mysql.connection.cursor()
        cursor.execute(purchase_query, tuple(purchase_params))
        purchase_data = cursor.fetchall()
        cursor.close()

    return render_template(
        "purchase.html",
        purchase_details=purchase_data,
        purchasers=purchasers,
        bond_number=bond_number
    )


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
