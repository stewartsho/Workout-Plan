from flask import Flask, render_template, request
import google.generativeai as palm
import replicate
import os
import sqlite3
import datetime
from flask import Markup

flag = 1
name = ""

makersuite_api = os.getenv("MAKERSUITE_API_TOKEN")
palm.configure(api_key=makersuite_api)


model = {"model" : "models/chat-bison-001"}
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    global flag, name
    print("flag", flag)
    if flag == 1:
        name = request.form.get("q")
        current_time = datetime.datetime.now()
        conn = sqlite3.connect("log (1).db")
        c = conn.cursor()
        c.execute("insert into user (name,time) values (?,?)",(name,current_time))
        conn.commit()
        c.close()
        conn.close()
        flag = 0
    return(render_template("main.html",r=name))

@app.route("/workout",methods=["GET","POST"])
def workout():
    return(render_template("workout.html"))

@app.route("/workout_result",methods=["GET","POST"])
def workout_result():
    q = request.form.get("q")
    q = "workout pla for people with age " + q + " in table form"
    r = palm.chat(**model, messages=q)
    return(render_template("workout_result.html",r=r.last))


@app.route("/log",methods=["GET","POST"])
def log():
    conn = sqlite3.connect("log (1).db")
    c = conn.cursor()
    c.execute("select * from user")
    r = ""
    for row in c:
        r += str(row) + "<br>"
    print(r)
    r = Markup(r)
    c.close()
    conn.close()
    return(render_template("log.html",r=r))

@app.route("/delete",methods=["GET","POST"])
def delete():
    conn = sqlite3.connect('log (1).db')
    c = conn.cursor()
    c.execute("delete from user")
    conn.commit()
    c.close()
    conn.close()
    return(render_template("delete.html"))

@app.route("/end",methods=["GET","POST"])
def end():
    global flag
    flag = 1
    return(render_template("index.html"))

if __name__ == "__main__":
    app.run()
