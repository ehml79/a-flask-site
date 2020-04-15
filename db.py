from app import *


# insert
role = Role(name='admin')
db.session.add(role)
db.session.commit()

user =User(name='app', role_id=role.id)

db.session.add(user)

user1 = User(name='zs', role_id=role.id)
user2 = User(name='ls', role_id=role.id)

db.session.add_all([user1, user2])

db.session.commit()

# update
user.name = 'chengxuyuan'
db.session.commit()

# del

db.session.delete(user)
db.session.commit()


# select
# 查询过滤器
filter()
filter_by()
limit
offset()
order_by()
group_by()

# 查询执行器
all()
User.query.all()
User.query.count()

first()
User.query.first()

first_or_404()

get()
User.query.get(4)
User.query.filter_by(id=4).first()
User.query.filter(User.id==4).first()

# filter_by: 属性=
# filter: 对象.属性==
# filter 功能更强大可以实现更多的一些查询条件，比如支持比较运算符

get_or_404()
count()
paginate()


