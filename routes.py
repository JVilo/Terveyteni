from crypt import methods

from flask import render_template, request, redirect, url_for
from app import app
import users
import messages
import tasks
from messages import longest_answers


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
            return render_template("login.html", message=error, username=username)
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
        user = users.user_name()
        names =[]
        for name in user:
            name =','.join(name)
            names.append(name)

        if username in names:
            error= "käyttäjätunnus on jo käytössä"
            print(error)
            return render_template("register.html", message=error,username=username)

        password1 = request.form["password1"]

        role = request.form["role"]
        if role not in ("1", "2"):
            error = "Tuntematon käyttäjärooli"
            return render_template("register.html", message=error)

        if not users.register(username, password1, role):
            error = "Rekisteröinti ei onnistunut"
            return render_template("register.html", message=error,username=username)
        return redirect("/")


@app.route("/messages/<id>", methods=["GET", "POST"])
def message_chain(id):
    if request.method == 'GET':
        longest_mes = messages.longest_mes(id)
        print(longest_mes[0])
        longest_answers = messages.longest_answers(id)
        print(longest_answers[0])
        longest_ms = max(longest_answers[0],longest_mes[0])
        parent = messages.get_message(id)
        ms = messages.get_answers(id)
        return render_template(
            "m_chain.html",
            parent=parent,
            ms=ms,
            count=len(ms)+1,
            longest= longest_ms
        )

    if "content" in request.form:
        users.check_csrf()
        content = request.form["content"]
        ref_key = id
        if messages.answer_mes(content, ref_key):
            return redirect(url_for('message_chain', id=id))


@app.route("/messages", methods=["GET"])
def list_messages():
    if request.method == "GET":
        lst = messages.get_list()
        cnt = messages.lst_count()
        frz = messages.get_freeze()
        frz_cnt = messages.freeze_count()
        return render_template("messages.html", count=cnt, messages=lst, freeze =frz, freeze_cnt = frz_cnt)


@app.route("/newm", methods=['POST', 'GET'])
def new_message():

    if request.method == "GET":
        return render_template("newm.html")

    if request.method == "POST":
        users.check_csrf()
        title = request.form["title"]
        content = request.form["content"]
        if messages.send(title, content):
            return redirect("/messages")


@app.route("/m_chain/<id>", methods=["POST"])
def remove(id):
    mes = messages.get_mes(id)
    messages.remove_message(id)
    return redirect(url_for('message_chain', id=mes[0][1]))


@app.route("/messages/<id>/delete", methods=["POST"])
def remove_chain(id):
    messages.remove_message(id)
    return redirect(url_for("list_messages"))


@app.route("/m_chain/<id>/edit", methods=["POST"])
def edit_mes(id):
    users.check_csrf()
    messages.edit_mes(
        id,
        content=request.form['content']
    )
    message = messages.get_message(id)
    return redirect(url_for('message_chain', id=message['ref_key']))


@app.route("/m_chain/<id>/edit_title", methods=["POST"])
def edit_title(id):
    users.check_csrf()
    messages.edit_title(
        id,
        title=request.form["title"]
    )
    return redirect(url_for("list_messages"))

@app.route("/m_chain/<id>/freeze", methods=["POST"])
def freeze_mes(id):
    messages.freeze(id)
    return redirect(url_for("list_messages"))

@app.route("/frozen_mes/<id>",methods=["GET"])
def get_frozen_mes(id):
    parent = messages.get_message(id, visible_status=3)
    child = messages.get_answers(id)
    return render_template(
        "frozen_mes.html",
        parent=parent,
        child=child
    )



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
        users.check_csrf()
        if "weight" in request.form and "height" in request.form:
            weight = request.form["weight"]
            height = request.form["height"]
            tasks.Bmi(weight, height)
            return redirect("/tasks_p")


@app.route("/private-chats", methods=["GET"])
def private_chat_list_dr():
    if users.get_current_role() == 2:
        patients = tasks.get_users()
        ended = messages.get_private_messages_d(users.user_id(), 2)
        return render_template("private_chat.html", patients=patients, user_role=users.get_current_role(),ended =ended)

    if users.get_current_role() == 1:
        lst = messages.get_private_messages_p(users.user_id())
        mlst = []
        for x in lst:
            if None not in x:
                mlst.append(x)
        ended = messages.get_private_messages_p(users.user_id(),2)
        return render_template("private_chat.html", lst=mlst, user_role=users.get_current_role(),
                               current_user_id=users.user_id(), length=len(mlst),ended =ended)

@app.route("/end-priv-cha/<id>",methods=["POST"])
def end_priv_cha(id):
    messages.end_priv_mes(id)
    return redirect("/")

@app.route("/patient/private-chat-ended/<dr_id>", methods=["GET"])
def show_chat_ended_p(dr_id):
    if request.method == 'GET':
        if users.user_id() != dr_id:
            users.require_role(1)
            lst = messages.get_private_messages(
                patient_id=users.user_id(),
                doctor_id=dr_id,
                visible_status=2
            )

            return render_template(
                "private_chat_ended.html",
                lst=lst,
                patient_id=users.user_id(),
                form_url=url_for("show_chat_ended_p", dr_id=dr_id),
            )

@app.route("/doctor/private-chat-end/<patient_id>", methods=["GET"])
def show_chat_ended_d(patient_id):
    current_user_id = users.user_id()
    if current_user_id != patient_id:
        users.require_role(2)

    private_messages = messages.get_private_messages(
        patient_id=patient_id,
        doctor_id=current_user_id,
        visible_status= 2
    )

    return render_template(
        "private_chat_ended.html",
        lst=private_messages,
        patient_id=patient_id,
        form_url=url_for("show_chat_ended_d", patient_id=patient_id),
    )

@app.route("/doctor/private-chat/<patient_id>", methods=["GET"])
def get_doctor_private_chat(patient_id):
    current_user_id = users.user_id()
    if current_user_id != patient_id:
        users.require_role(2)

    private_messages = messages.get_private_messages(
        patient_id=patient_id,
        doctor_id=current_user_id
    )

    return render_template(
        "private_chat_site.html",
        lst=private_messages,
        patient_id=patient_id,
        form_url=url_for("get_doctor_private_chat", patient_id=patient_id),
    )

@app.route("/doctor/private-chat/<patient_id>", methods=["POST"])
def post_doctor_private_chat(patient_id):
    current_user_id = users.user_id()
    if current_user_id != patient_id:
        users.require_role(2)

    private_messages = messages.get_private_messages(
        patient_id=patient_id,
        doctor_id=current_user_id
    )
    if len(private_messages) ==0:
        users.check_csrf()
        title = request.form["title"]
        content = request.form["content"]

        if messages.send_private_message(
                title,
                content,
                doctor_id=current_user_id,
                patient_id=patient_id,
        ):
            return redirect(url_for(
                "post_doctor_private_chat",
                patient_id=patient_id)
            )
        else:
            error = "Viestin lähetys ei onnistunut"
            return render_template(
                "private_chat_site.html",
                message=error,
                patient_id=patient_id,
                form_url=url_for("post_doctor_private_chat", patient_id=patient_id),
            )
    else:
        ref_key = private_messages[0][0]
        users.check_csrf()
        content = request.form["content"]
        doctor_id = current_user_id
        patient_id = patient_id
        if messages.answer_private(content, doctor_id, patient_id,ref_key):
            return redirect(url_for("post_doctor_private_chat",patient_id=patient_id))


@app.route("/patient/private-chat/<dr_id>", methods=["GET", "POST"])
def show_chat_p(dr_id):
    lst = messages.get_private_messages(
        patient_id=users.user_id(),
        doctor_id=dr_id
    )
    if request.method == 'GET':
        if users.user_id() != dr_id:
            users.require_role(1)

            return render_template(
                "private_chat_site.html",
                lst=lst,
                patient_id=users.user_id(),
                form_url=url_for("show_chat_p", dr_id=dr_id),
            )
    if request.method == "POST":
        users.check_csrf()
        ref_key =lst[0][0]
        content = request.form["content"]
        doctor_id = dr_id
        patient_id = users.user_id()
        if messages.answer_private(content, doctor_id, patient_id,ref_key):
            return redirect(url_for("show_chat_p", dr_id=dr_id))

@app.route("/remove/private_chat_site/<dr_id>/<patient_id>/<id>", methods=["POST"])
def remove_piv(id,dr_id,patient_id):
    messages.remove_message_priv(id)
    if users.user_id() != dr_id:
        users.require_role(1)
        lst = messages.get_private_messages(
            patient_id=users.user_id(),
            doctor_id=dr_id
        )
        return render_template(
            "private_chat_site.html",
            lst=lst,
            patient_id=users.user_id(),
            form_url=url_for("show_chat_p", dr_id=dr_id),
        )

    else:
        current_user_id = users.user_id()
        private_messages = messages.get_private_messages(
            patient_id=patient_id,
            doctor_id=current_user_id
        )

        return render_template(
            "private_chat_site.html",
            lst=private_messages,
            patient_id=patient_id,
            form_url=url_for("get_doctor_private_chat", patient_id=patient_id),
        )

@app.route("/private_chat_site/<dr_id>/<patient_id>/<id>/edit", methods=["POST"])
def edit_mes_priv(id,dr_id,patient_id):
    users.check_csrf()
    messages.edit_mes_priv(
        id,
        content=request.form['content']
    )
    if users.user_id() != dr_id:
        users.require_role(1)
        lst = messages.get_private_messages(
            patient_id=users.user_id(),
            doctor_id=dr_id
        )

        return render_template(
            "private_chat_site.html",
            lst=lst,
            patient_id=users.user_id(),
            form_url=url_for("show_chat_p", dr_id=dr_id),
        )
    else:
        current_user_id = users.user_id()
        private_messages = messages.get_private_messages(
            patient_id=patient_id,
            doctor_id=current_user_id
        )

        return render_template(
            "private_chat_site.html",
            lst=private_messages,
            patient_id=patient_id,
            form_url=url_for("get_doctor_private_chat", patient_id=patient_id),
        )




