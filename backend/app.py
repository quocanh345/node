from flask import Flask, jsonify, request, redirect, url_for
from db.init_db import pool_get, pool_put, pool_create
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return redirect(url_for("table_list"))
    

@app.route("/users", methods=["GET", "POST"])
def table_list():
    cur, con = pool_get()
    if request.method == "GET":
        try:
            cur.execute("SELECT * FROM users;")
            tab = cur.fetchall()
            return jsonify(tab)
        except Exception as e:
            print(e)
        finally:
            pool_put(con)
    else:
        try:
            data = request.get_json()
            name = data.get("name")
            email = data.get("email")
            
            cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (name, email))
            con.commit()
            return "", 204
        except Exception as e:
            con.rollback()
            print(e)
        finally:
            pool_put(con)
            
            
@app.route("/users/<int:uid>", methods=["DELETE", "PUT"])
def table_detail(uid):
    cur, con = pool_get()
    if request.method == "DELETE":
        try:
            cur.execute("DELETE FROM users WHERE id = %s;", (uid,))
            con.commit()
            return "", 204
        except Exception as e:
            con.rollback()
            print(e)
        finally:
            pool_put(con)
    else:
        try:
            data = request.get_json()
            name = data.get("name")
            email = data.get("email")
            
            cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s;", (name, email,uid))
            con.commit()
            return "", 204
        except Exception as e:
            print(e)
            con.rollback()
        finally:
            pool_put(con)
            

if __name__ == "__main__":
    pool_create()
    app.run(debug=True)
