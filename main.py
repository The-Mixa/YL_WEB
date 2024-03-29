from flask import Flask, render_template, redirect, request
from flask import make_response, jsonify, abort

from data import db_session
from data import jobs_api
from data import users_api

from data.users import User
from data.jobs import Jobs
from data.departaments import Departments
from data.category import Category

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.login import LoginForm
from forms.user import RegisterForm
from forms.jobs import JobsForm
from forms.departments import DepartmentsForm
from forms.category import CategoryForm

from requests import get
from os import chdir, mkdir


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run('127.0.0.1', port=800)


@app.route("/")
def index():
    db = db_session.create_session()

    jobs = db.query(Jobs).all()
    data = []
    ides = []
    users = []
    for job in jobs:
        team_leader = db.query(User).filter(User.id == job.team_leader).first()
        data.append((job.job, f'{team_leader.surname} {team_leader.name}',
                    job.work_size, job.collaborators, ', '.join([i.name for i in job.categories]), job.is_finished))
        ides.append(job.id)
        users.append(job.user)

    return render_template('index.html', data=data, ides=ides, title='Страница Миссии', users=users)


@app.route('/departments')
def departments():
    db = db_session.create_session()

    departments = db.query(Departments).all()
    data = []
    ides = []
    users = []
    for dep in departments:
        chief = db.query(User).filter(User.id == dep.chief).first()
        data.append(
            (dep.title, f'{chief.surname} {chief.name}', dep.members, dep.email))
        ides.append(dep.id)
        users.append(dep.user)

    return render_template('departments.html', data=data, ides=ides, title='Страница Миссии', users=users)


@app.route('/departments_add',  methods=['GET', 'POST'])
@login_required
def departments_add():
    form = DepartmentsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Departments()
        dep.title = form.title.data
        dep.chief = form.chief.data
        dep.members = form.members.data
        dep.email = form.email.data
        current_user.departments.append(dep)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_department.html', title='Добавление Департамента', form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dep(id):
    form = DepartmentsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Departments).filter(Departments.id == id,
                                                Departments.user == current_user
                                                ).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db = db_session.create_session()
        dep = db.query(Departments).filter(Departments.id == id,
                                           Departments.user == current_user
                                           ).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            db.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('add_department.html',
                           title='Редактирование департамента',
                           form=form)


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def dep_delete(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Departments).filter(Departments.id == id,
                                            Departments.user == current_user
                                            ).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            city_from=form.city_from.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = form.team_leader_id.data
        job.is_finished = form.is_finished.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        current_user.jobs.append(job)
        db.merge(current_user)
        db.commit()
        job = db.query(Jobs).all()[-1]

        categories = db.query(Category).filter(Category.id.in_(
            map(int, form.categories.data.split(', ')))).all()
        if categories:
            job.categories = categories

        db.commit()

        return redirect('/')
    return render_template('jobs.html', title='Добавление Работы', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         Jobs.user == current_user
                                         ).first()
        if job:
            form.title.data = job.job
            form.team_leader_id.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.categories.data = ', '.join(
                [str(i.id) for i in job.categories])
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db = db_session.create_session()
        job = db.query(Jobs).filter(Jobs.id == id,
                                    Jobs.user == current_user
                                    ).first()
        if job:
            job.job = form.title.data
            job.team_leader = form.team_leader_id.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            job.categories = db.query(Category).filter(Category.id.in_(
                map(int, form.categories.data.split(', ')))).all()
            db.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == current_user
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.route('/category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        category = Category()
        category.name = form.name.data
        db.add(category)
        db.commit()
        return redirect('/')
    return render_template('category.html', title='Добавление Категории', form=form)


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    response = get(f'http://localhost:800/api/users/{user_id}').json()['user']
    city_from = response['city_from']
    name = f"{response['surname']} {response['name']}"

    geocoder_server =  "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": city_from,
    "format": "json"}
    response = get(geocoder_server, params=geocoder_params).json()

    toponym = response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "z": 12,
        "l": "sat"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = get(map_api_server, params=map_params)
    try:
        chdir('static\\img\\')
    except Exception:
        pass
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return render_template('user_show.html', city_from=city_from, name=name)


if __name__ == '__main__':
    main()
