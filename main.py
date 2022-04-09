from project_camping.DBWork import DBWork
from flask import Flask, render_template, request, redirect
import os
from project_camping.helpers import correct_date


app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

db_work = DBWork()


@app.route('/', methods=['GET', 'POST'])
def index():
    """основная страница + пользователь не авторизовался"""
    if request.method == 'GET':
        print(db_work.get_all_hiking())
        return render_template('before-login.html', db_work=db_work, hikings=db_work.get_all_hiking(), user_in=False)

    elif request.method == 'POST':
        if request.form.get('registration') != None:
            return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ авторизация """

    if request.method == 'GET':
        return render_template('login.html', mistake=None)

    if request.method == 'POST':
        if request.form.get('sign_in') is not None:
            if request.form.get('name').strip() == '' or \
                    request.form.get('password').strip() == '' or \
                    request.form.get('login').strip() == '':
                return render_template('login.html', mistake='Все поля должны быть заполнены!')
            cur_user = db_work.check_email(request.form.get('login'))
            if cur_user is not False:
                if request.form.get('password') != cur_user.hashed_password:
                    return render_template('login.html', mistake='Неверный пароль')
                else:
                    return redirect(f'/home/{db_work.get_id(request.form.get("login"))}')
            else:

                email = request.form.get('login')
                password = request.form.get('password')
                name = request.form.get('name')

                db_work.make_new_user(email, password, name)
                if request.form.get('type') == 'instructor':
                    return redirect(f'/login/{request.form.get("login")}')

                return redirect(f'/home/{db_work.get_id(email)}')


@app.route('/home/<id>', methods=['GET', 'POST'])
def home(id):
    """основная страница + пользователь  авторизовался
    :id: id пользователя"""

    if request.method == 'GET':
        return render_template('base-userin.html', type=db_work.get_type(id), db_work=db_work,
                               hikings=db_work.get_all_hiking(), user_in=True)
    elif request.method == 'POST':
        if request.form.get('home_page') is not None:
            return redirect(f'/user_page/{id}')
        elif request.form.get('new_hiking') is not None:
            return redirect(f'/new_hiking/{id}')
        elif request.form.get('like') is not None:
            hiking_id = request.form.get('like')
            db_work.add_hiking_to_user_list(user_id=id, hiking_id=hiking_id)

            return render_template('base-userin.html', type=db_work.get_type(id), db_work=db_work,
                                   hikings=db_work.get_all_hiking(), user_in=True)


@app.route('/new_hiking/<id>', methods=['GET', 'POST'])
def new_hiking(id):
    """создание нового похода
        :id: id инструктора"""
    if request.method == 'GET':
        return render_template('new_hiking.html', instructor_name=db_work.get_name(id))
    elif request.method == 'POST':

        db_work.make_new_hiking(type=request.form.get('type'),
                                name=request.form.get('hiking_name'),
                                place=request.form.get('place'),
                                date=correct_date(request.form.get('hiking_start'))+'-'+correct_date(request.form.get('hiking_end')),
                                difficulty_level=request.form.get('hiking_difficulty'),
                                instructor_id=id,
                                image=request.form.get('image'))

        return redirect(f'/home/{id}')





@app.route('/login/<email>',  methods=['POST', 'GET'])
def get_inst_skill(email):
    """ оценка скилла инструктора
    :email: email инстр """
    if request.method == 'GET':
        return render_template('inst_skill.html')
    elif request.method == 'POST':
        skill = request.form.get('skill')

        db_work.add_inst_skill(email, skill)
    return redirect(f'/home/{db_work.get_id(email)}')


@app.route('/user_page/<id>', methods=['GET', 'POST'])
def user_page(id):
    """ страница пользователя
        :id: id пользователя """
    if request.method == 'GET':
        return render_template('user_page.html', hikings=db_work.get_hiking_list(user_id=id), db_work=db_work)
    elif request.method == 'POST':
        if request.form.get('back_home') != None:
            return redirect(f'/home/{id}')


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')

