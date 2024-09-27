from crypt import methods

from flask import render_template, request, redirect
from app import app
import users
import messages
import tasks


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")
        
        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Tuntematon käyttäjärooli")

        if not users.register(username, password1, role):
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")

@app.route("/messages",methods=["GET", "POST"])
def show_mess():
    if request.method == "GET":
        lst = messages.get_list()
        print(lst)
        return render_template("messages.html", count=len(lst), messages=lst)

    if request.method == "POST":
        print("viestien tuonti")
        if "message.id" in request.form:
            message = request.form["message.id"]
            print(message, "tämä on ID")
            ms = messages.mes_chain(message)
            print(ms,"tämä on tuloste")
            print(ms[0])
            return render_template("m_chain.html", ms =ms, count = len(ms))


#@app.route("/m_chain", methods=["GET"])
#def message_chain():
    #print("näytä viesti")
    #if request.method == "GET":
        #ms = messages.mes_chain(message)
        #return render_template("m_chain.html", ms = ms)

@app.route("/m_chain", methods=["POST"])
def ans_chain():
    if request.method == "POST":
        pass

@app.route("/newm")
def new():
    return render_template("newm.html")

@app.route("/send", methods=["POST"])
def send():
    title = request.form["title"]
    content = request.form["content"]
    if messages.send(title,content):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/remove",methods=["GET", "POST"])
def remove():

    if request.method == "GET":
        message = messages.get_my_message(users.user_id())
        return render_template("remove.html", list= message)

    if request.method == "POST":
        users.check_csrf()

        if "message" in request.form:
            message = request.form["message"]
            messages.remove_message(message, users.user_id())
            
        return redirect("/")
    
@app.route("/tasks",methods=["GET", "POST"])
def chose_task():
    users.require_role(2)
    if request.method == "GET":
        data = tasks.get_bmi()
        ls_bmi=[]
        if tasks.get_activ_bmi():
            t = 0
        else:
            t = 1
        if data:
            for x in data:
                name = x[0]
                weight = x[1]
                height = x[2]
                bmi = round((weight / ((height / 100) ** 2)), 2)
                ls_bmi.append((name,weight,height,bmi))
            return render_template("tasks.html", data = ls_bmi,lst = len(ls_bmi), t=t)
        else:
            data = 0
            return render_template("tasks.html",data = data,lst = len(ls_bmi), t=t)

    if request.method == "POST":
        if "task_bmi" in request.form:
            task_bmi =request.form["task_bmi"]
            if task_bmi == "on":
                task_bmi = 1
                tasks.activate_bmi(task_bmi)
    
        return redirect("/")

@app.route("/tasks_p",methods=["GET"])
def do_task():
    users.require_role(1)
    
    if request.method == "GET":
        data = tasks.get_activ_bmi()
        lst= tasks.cal_bmi(users.user_id())

        if len(lst)>1:
            lst = lst[0]
            weight = lst[0]
            height= lst[1]
            bmi = round((weight / ((height / 100) ** 2)), 2)
            return render_template("tasks_p.html", bmi = bmi)
         
        if len(data):
            data = 1
            bmi = "?"
            return render_template("tasks_p.html",data = data, bmi = bmi)
        else:
            data = 0
            bmi = "?"
            return render_template("tasks_p.html",data = data, bmi = bmi)

@app.route("/tasks_p", methods= ["POST"])
def send_task():
            
    if request.method == "POST":
        if "weight" in request.form and "height" in request.form:
            weight = request.form["weight"]
            height = request.form["height"]
            tasks.Bmi(weight,height)
            return redirect("/tasks_p")



    
