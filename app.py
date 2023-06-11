from flask import Flask, render_template, request, redirect, flash, url_for 
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Rahlff28"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
def fetch_beer_ratings():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="Rahlff28", host="localhost")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT id, AVG(\"Rating\") AS average_rating FROM \"Ratings_dis\" GROUP BY id")
    rows = cur.fetchall()
    beer_ratings = {row['id']: row['average_rating'] for row in rows}
    cur.close()
    conn.close()
    return beer_ratings
def calculate_average_rating(beer_id):
    beer_ratings = fetch_beer_ratings()
    average_rating = beer_ratings.get(beer_id, 0)
    return round(average_rating, 2)
@app.route('/')
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    table_name = "\"Beers\""
    s = f"SELECT * FROM {table_name}"
    cur.execute(s)
    list_names = cur.fetchall()
    beer_ratings = fetch_beer_ratings()
    return render_template('index.html', list_names = list_names,  beer_ratings=beer_ratings, calculate_average_rating=calculate_average_rating)

@app.route('/add_beer', methods = ["POST"])
def add_beer():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    table_name = "\"Beers\""
    if request.method == "POST":
        name = request.form["name"]
        brewery = request.form["brewery"]
        id = request.form["id"]
        type = request.form["type"]
        abv = request.form["abv"]
        cur.execute(f"INSERT INTO {table_name} (\"Name\", \"Brewery\", \"id\",\"Type\", \"abv\") VALUES (%s,%s,%s,%s, %s)", (name, brewery, id, type, abv))
        conn.commit()
        flash('Beer Added successfully')
        return redirect(url_for('index'))
    
@app.route('/beer_ratings/<beer_id>')
def beer_ratings(beer_id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    ratings_table = "\"Ratings_dis\""  # Replace with your ratings table name
    s = f"SELECT * FROM {ratings_table} WHERE \"id\" = %s"
    cur.execute(s, (beer_id,))
    beer_ratings = cur.fetchall()
    return render_template('beer_ratings.html', beer_ratings=beer_ratings)

@app.route('/add_rating', methods=["POST"])
def add_rating():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    table_name = "\"Ratings_dis\""
    if request.method == "POST":
        username = request.form["name"]
        rating = request.form["rating"]
        beer_id = request.form["beer_id"]
        cur.execute(f"INSERT INTO {table_name} VALUES (%s, %s, %s)",(username, beer_id,rating))
        conn.commit()
        flash('Rating added successfully')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
    

