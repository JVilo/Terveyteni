from crypt import methods

from flask import render_template, request, redirect, url_for
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
            error = "Väärä tunnus tai salasana"
            return render_template("login.html", message=error)
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
            error = "Tunnuksessa tulee olla 1-20 merkkiä"
            return render_template("register.html", message=error)

        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            error = "Salasanat eroavat"
            return render_template("register.html", message=error)
        if password1 == "":
            error = "Salasana on tyhjä"
            return render_template("register.html", message=error)

        role = request.form["role"]
        if role not in ("1", "2"):
            error = "Tuntematon käyttäjärooli"
            return render_template("register.html", message=error)

        if not users.register(username, password1, role):
            error = "Rekisteröinti ei onnistunut"
            return render_template("error.html", message=error)
        return redirect("/")


@app.route("/messages/<id>", methods=["GET", "POST"])
def message_chain(id):
    if request.method == 'GET':
        parent = messages.get_message(id)
        ms = messages.get_answers(id)
        return render_template(
            "m_chain.html",
            parent=parent,
            ms=ms,
            count=len(ms)
        )

    print("lähetetään sisältöä")
    if "content" in request.form:
        content = request.form["content"]
        ref_key = id
        if messages.answer_mes(content, ref_key):
            return redirect(url_for('message_chain', id=id))
        else:
            print("virhe")


@app.route("/messages", methods=["GET"])
def list_messages():
    if request.method == "GET":
        lst = messages.get_list()
        return render_template("messages.html", count=len(lst), messages=lst)


@app.route("/newm", methods=['POST', 'GET'])
def new_message():
    if request.method == "GET":
        return render_template("newm.html")

    title = request.form["title"]
    if title == "":
        error = "otsikko ei voi olla tyhjä"
        return render_template("newm.html", message=error)

    content = request.form["content"]
    if content == "":
        error = "viesti ei voi olla tyhjä"
        return render_template("newm.html", message=error)

    if messages.send(title, content):
        return redirect("/messages")
    else:
        error = "Viestin lähetys ei onnistunut"
        return render_template("newm.html", message=error)


@app.route("/m_chain/<id>", methods=["POST"])
def remove(id):
    print("väärä remove")
    mes = messages.get_mes(id)
    messages.remove_message(id)
    return redirect(url_for('message_chain', id=mes[0][1]))


@app.route("/messages/<id>/delete", methods=["POST"])
def remove_chain(id):
    print("tänne piti tulla")
    messages.remove_message(id)
    return redirect(url_for("list_messages"))


@app.route("/m_chain/<id>/edit", methods=["POST"])
def edit_mes(id):
    messages.edit_mes(
        id,
        content=request.form['content']
    )
    message = messages.get_message(id)
    return redirect(url_for('message_chain', id=message['ref_key']))

@app.route("/m_chain/<id>/edit_title", methods=["POST"])
def edit_title(id):
    messages.edit_title(
        id,
        title=request.form["title"]
    )
    return redirect(url_for("list_messages"))


@app.route("/tasks", methods=["GET", "POST"])
def chose_task():
    users.require_role(2)
    if request.method == "GET":
        data = tasks.get_bmi()
        ls_bmi = []
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
                ls_bmi.append((name, weight, height, bmi))
            return render_template("tasks.html", data=ls_bmi, lst=len(ls_bmi), t=t)
        else:
            data = 0
            return render_template("tasks.html", data=data, lst=len(ls_bmi), t=t)

    if request.method == "POST":
        if "task_bmi" in request.form:
            task_bmi = request.form["task_bmi"]
            if task_bmi == "on":
                task_bmi = 1
                tasks.activate_bmi(task_bmi)

        return redirect("/")


@app.route("/tasks_p", methods=["GET"])
def do_task():
    users.require_role(1)

    if request.method == "GET":
        data = tasks.get_activ_bmi()
        lst = tasks.cal_bmi(users.user_id())

        if len(lst) > 1:
            lst = lst[0]
            weight = lst[0]
            height = lst[1]
            bmi = round((weight / ((height / 100) ** 2)), 2)
            return render_template("tasks_p.html", bmi=bmi)

        if len(data):
            data = 1
            bmi = "?"
            return render_template("tasks_p.html", data=data, bmi=bmi)
        else:
            data = 0
            bmi = "?"
            return render_template("tasks_p.html", data=data, bmi=bmi)


@app.route("/tasks_p", methods=["POST"])
def send_task():
    if request.method == "POST":
        if "weight" in request.form and "height" in request.form:
            weight = request.form["weight"]
            height = request.form["height"]
            tasks.Bmi(weight, height)
            return redirect("/tasks_p")
