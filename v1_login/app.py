#!/usr/bin/env python


from flask import Flask, render_template, request, flash, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import data_required, equal_to

from flask_sqlalchemy import SQLAlchemy

# 解决编码问题 python2
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')



app = Flask(__name__)

app.secret_key = 'testkey'


# 配置数据库地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask:password@192.168.217.128:3306/flask?charset=utf8mb4'
# 动态跟踪数据的修改，不建议开启，消耗性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 创建数据库对象
db = SQLAlchemy(app)

'''
两张表
角色(管理员/普通用户)
用户(角色id)
'''

# 数据库的模型，需要继承db.Model
class Role(db.Model):
    # 定义表
    __tablename__ = 'roles'
    # 定义字段
    # db.Column 表示是一个字段
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    # 在一方的一方，写关联
    # db.relationship('User')  表示和User模型发生关联，增加了一个users属性
    # backref='role' 表示role是User要用的属性
    users = db.relationship('User', backref='role')

    # refr方法显示一个可读字符串
    def __repr__(self):
        return '<Role: %s %s>' % (self.name, self.id)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # User希望有role属性，但是这个属性的定义需要在另一个模型中定义

    # refr方法显示一个可读字符串
    def __repr__(self):
        return '<Role: %s %s %s %s>' % (self.name, self.id, self.email, self.password)


@app.route('/')
def index():
    url_str = 'www.baidu.com'
    my_list = [1, 3, 5, 7, 9]
    my_dict = {
        'name': 'baidu',
        'url': 'www.baidu.com',
    }
    my_int = 123

    return render_template('index.html',
                           url_str=url_str,
                           my_list=my_list,
                           my_dict=my_dict,
                           my_int=my_int,
                           )


'''
目的：实现一个简单的登录的逻辑处理
1. 路由需要有get和post两种请求方式--> 需要判断请求方式
2. 获取请求的参数
3. 判断参数是否填写 & 密码是否相同
4. 如果判断都没有问题，就返回一个success
'''

'''
给模版传递消息
flash 需要对内容加密，因此需要设置secret_key，做加密消息的混淆
模板中需要遍历消息
'''
'''
使用WTF实现表单
自定义表单类
'''

class LoginForm(FlaskForm):
    username = StringField('用户名: ', validators=[data_required()])
    password = PasswordField('密码: ',  validators=[data_required()])
    password2 = PasswordField('确认密码: ', validators=[
        data_required(),
        equal_to('password', message='密码不一致')
    ]
)

    submit = SubmitField('提交')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    # 1 request:请求对象--> 获取请求方式，数据
    if request.method == 'POST':

        # 2  获取请求的参数
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 3 验证参数
        if login_form.validate_on_submit():
            print(username, password)
            return 'success'
        else:
            flash('参数有误')

    return render_template('login.html', form=login_form)

#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     #1 request:请求对象--> 获取请求方式，数据
#     if request.method == 'POST':
#
#         #2  获取请求的参数
#         username = request.form.get('username')
#         password = request.form.get('password')
#         password2 = request.form.get('password2')
#         # print(username)
#
#         #3
#         if not all([username, password, password2]):
#             # print('参数不完整')
#             flash('参数不完整')
#         elif password != password2:
#             # print('密码不一致')
#             flash('密码不一致')
#         else:
#             return 'success'
#     return render_template("login.html")




'''
1.配置数据库
    a.导入sqlalchemy扩展
    b.创建db对象，并配置参数
    c.终端创建数据库
2.添加书和作者类型
    a.模型继承db.Model
    b. __tablename__表名
    c. db.Column:字段
    d. db.relaionship:关系引用
3.添加数据
4.使用模版显示查询的数据
    a.查询所有的作者信息，让信息传递给模版
    b.模版中按照格式，依次for循环作者和书籍即可(作者获取书籍，用的是关系引用)
5.使用wtf显示表单
    a.自定义表单类
    b.模板中显示
    c.设置secret_key / 编码 / csrf_token
6.实现相关的增删逻辑
    a.增加数据
    b. 删除书籍 网页中删除  点击需要发送书籍的id给删除书籍的路由 路由需要接受参数
    url_for 的适用 / for else 的使用 / redirect 的使用
    c. 删除作者
    
'''

# 定义书和作者模型
# 作者模型
class Author(db.Model):
    # 表明
    __tablename__ = 'authors'
    # 字段
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    # 关系引用
    # books是给自己(Author)用的，author是给Book模型用的
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return 'Author: %s' % self.name

# 书籍模型
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return 'Book: %s %s' % (self.name, self.author_id)


# 自定义 表单类
class AuthorForm(FlaskForm):
    author = StringField('作者', validators=[data_required()])
    book = StringField('书籍', validators=[data_required()])
    submit = SubmitField('提交')

@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    # 1.查询数据库，是否有该id的书，如果有就删除，没有提示错误
    book = Book.query.get(book_id)
    # 2. 如果有就删除
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除书籍出错')
            db.session.rollback()
    else:
        # 3 没有就提示
        flash('书籍不存在')


    # 如何返回当前网址 重定向
    # redirect 重定向，需要传入网络/路由地址
    # url_for('book'); 需要传入视图函数名，返回该视图函数对应的路由地址
    # redirect('/')
    return redirect(url_for('books'))

# 删除作者
@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    # 查询数据库，是否有该id的作者，如果有就删除(先删书，再删坐着)，没有提示错误
    # 1.查询数据库
    author = Author.query.get(auth_id)
    # 2. 如果有就删除(先删书，再删作者)
    if author:
        try:
            # 查询之后直接删除
            Book.query.filter_by(author_id=author.id).delete()
            # 删除作者
            db.session.delete(author)
            db.commit()
        except Exception as e:
            # 没有提示错误
            print(e)
            flash('作者找不到')
            db.session.rollback()
    return redirect(url_for('books'))

@app.route('/books', methods=['GET', 'POST'])
def books():

    # 创建自定义的表单类
    author_form = AuthorForm()
    '''
    验证逻辑
    1.调用WTF的函数实现验证
    2.验证通过获取数据
    3.判断作者是否存在
    4.如果作者存在，判断书籍是否存在，没有重复书籍就添加数据，如果重复就提示错误
    5.如果作者不存在，添加作者和书籍
    6.验证不通过就提示错误
    '''
    # 1
    if author_form.validate_on_submit():
        # 2
        author_name = author_form.author.data
        book_name = author_form.book.data
        # 3
        author = Author.query.filter_by(name=author_name).first

        if author:
            # 4
            book = Book.query.filter_by(name=book_name).first()
            if book:
                flash('已存在同名书籍')
            else:
                try:
                    new_book = Book(name=book_name, author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash('添加书籍失败')
                    db.session.rollback()
        else:
            # 5
            try:
                new_author = Author(name=author_name)
                db.session.add(new_author)
                db.session.commit()

                new_book = Book(name=book_name, author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                print(e)
                flash('添加作者和书籍失败')
                db.session.rollback()
    else:
        if request.method == 'POST':
            flash('参数不全')

    # 查询所有的作者信息，让信息传递给模版
    authors = Author.query.all()

    return render_template('books.html', authors=authors, form=author_form)



if __name__ == '__main__':

    # 删除表
    db.drop_all()
    # 创建表
    db.create_all()

    # 添加测试数据
    ro1 = Role(name='admin')
    db.session.add(ro1)

    ro2 = Role(name='user')
    db.session.add(ro2)

    us1 = User(name='wang', email='wang@163.com', password='111111', role_id=ro1.id)
    us2 = User(name='zhang', email='zhang@163.com', password='222222', role_id=ro1.id)
    us3 = User(name='chen', email='chen@163.com', password='333333', role_id=ro1.id)
    us4 = User(name='zhou', email='zhou@163.com', password='444444', role_id=ro1.id)
    us5 = User(name='tang', email='tang@163.com', password='555555', role_id=ro1.id)
    us6 = User(name='wu', email='wu@163.com', password='666666', role_id=ro1.id)
    us7 = User(name='qian', email='qian@163.com', password='777777', role_id=ro1.id)
    us8 = User(name='liu', email='liu@163.com', password='888888', role_id=ro1.id)
    us9 = User(name='li', email='li@163.com', password='999999', role_id=ro1.id)
    us10 = User(name='sun', email='sun@163.com', password='000000', role_id=ro1.id)

    db.session.add_all([us1, us2, us3, us4, us5, us6, us7, us8, us9, us10])

    # 生成数据
    au1 = Author(name='老王')
    au2 = Author(name='老惠')
    au3 = Author(name='老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])

    bk1 = Book(name='老王回忆录', author_id=au1.id)
    bk2 = Book(name='老王的书', author_id=au1.id)
    bk3 = Book(name='老惠的书', author_id=au2.id)
    bk4 = Book(name='老刘回忆录', author_id=au3.id)
    bk5 = Book(name='老李的书', author_id=au3.id)
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])

    db.session.commit()

    app.run(host='127.0.0.1', port=80, debug=True)




