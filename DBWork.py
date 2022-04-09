from project_camping import db_session
from project_camping.models import User, HikingDB
from project_camping.const import INSTRUCTOR_SKILLS


class DBWork:
    def __init__(self):
        db_session.global_init("db/camping.db")

    def get_id(self, email):  # получение id по email
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()
        return user.id

    def get_type(self, id):     # получить тип пользователя (инструтор\турист)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()

        if user.skill != None:
            return 'instructor'
        return 'tourist'

    def get_name(self, id1):    # получить name по id
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id1).first()
        return user.name

    def make_new_user(self, email, password, name):   # создание нового пользователя
        user = User()
        user.email = email
        user.name = name
        user.hashed_password = password

        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()

    def add_inst_skill(self, email, skill):     # добавление скилла инструктора
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()
        user.skill = INSTRUCTOR_SKILLS[skill]
        db_sess.commit()

    def add_hiking_to_user_list(self, user_id, hiking_id):   # добавление похода в избранное
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()

        h_list = user.hiking_list
        if not h_list:
            user.hiking_list = f'{hiking_id}'
        elif hiking_id in h_list:
            pass
        else:
            user.hiking_list += f' {hiking_id}'

        db_sess.commit()

    def make_new_hiking(self, type, name, place, date, difficulty_level, image:str, instructor_id:int):     # создание нового похода
        db_sess = db_session.create_session()
        instr_id = db_sess.query(User).filter(User.id == instructor_id).first()
        hiking = HikingDB(type=type, name=name, place=place, date=date, difficulty_level=difficulty_level,
                          user=instr_id, image=image)
        db_sess.add(hiking)
        db_sess.commit()

    def get_all_hiking(self):       # получение списка всех походов
        db_sess = db_session.create_session()
        ans = reversed(db_sess.query(HikingDB).all())
        return ans

    def get_hiking_list(self, user_id):     # получить список походов пользователя
        ans = []
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        db_sess = db_session.create_session()
        l = user.hiking_list

        if l is not None:
            for hiking_id in l.split(' '):
                ans.append(db_sess.query(HikingDB).filter(HikingDB.id == int(hiking_id)).first())

        return ans

    def check_email(self, email):       # проверка существования профиля
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()
        if user is not None:
            return user
        return False

