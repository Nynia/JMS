from app import db

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    loginname = db.Column(db.String(20),unique=True)
    loginpassword = db.Column(db.String(20))
    type = db.Column(db.Integer)
    def __init__(self, username, password, type):
        self.loginname = username
        self.loginpassword = password
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.loginname

    def get_user_type(self):
        return self.type

class Positon(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(50))
    name = db.Column(db.String(50))
    salary = db.Column(db.Integer)
    num = db.Column(db.Integer)
    edu = db.Column(db.String(10))
    tel = db.Column(db.String(11))
    city = db.Column(db.String(20))
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    create_date = db.Column(db.Date)

    def __init__(self, company_name, name, salary, num, edu, tel,
                 city, description, requirements, create_date):
        self.company_name = company_name
        self.name = name
        self.salary = salary
        self.num = num
        self.edu = edu
        self.tel = tel
        self.city = city
        self.description = description
        self.requirements = requirements
        self.create_date = create_date
    def __repr__(self):
        return '<company %r>' % self.company_name

class Student(db.Model):
    __tablename__ = 'seeker'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    name = db.Column(db.String(10))
    sex = db.Column(db.String(1))
    age = db.Column(db.String(11))
    degree = db.Column(db.String(10))
    nation = db.Column(db.String(10))
    tel = db.Column(db.String(11))
    mail = db.Column(db.String(50))
    school = db.Column(db.String(50))
    major = db.Column(db.String(50))
    institute = db.Column(db.String(50))
    expedu1 = db.Column(db.Integer)
    expedu2 = db.Column(db.Integer)
    expedu3 = db.Column(db.Integer)
    expwork1 = db.Column(db.Integer)
    expwork2 = db.Column(db.Integer)
    expwork3 = db.Column(db.Integer)
    expwork4 = db.Column(db.Integer)
    expaward1 = db.Column(db.Integer)
    expaward2 = db.Column(db.Integer)
    expaward3 = db.Column(db.Integer)
    expaward4 = db.Column(db.Integer)

    def __init__(self, uid, name, sex, age, degree, nation, tel, mail, school, major,
                 institute, expedu1, expedu2, expedu3, expwork1, expwork2, expwork3, expwork4,
                 expaward1, expaward2, expaward3, expaward4):
        self.uid = uid
        self.name = name
        self.sex = sex
        self.age = age
        self.degree = degree
        self.nation = nation
        self.tel = tel
        self.mail = mail
        self.school = school
        self.major = major
        self.institute = institute
        self.expedu1 = expedu1
        self.expedu2 = expedu2
        self.expedu3 = expedu3
        self.expwork1 = expwork1
        self.expwork2 = expwork2
        self.expwork3 = expwork3
        self.expwork4 = expwork4
        self.expaward1 = expaward1
        self.expaward2 = expaward2
        self.expaward3 = expaward3
        self.expaward4 = expaward4

    def __repr__(self):
        return '<name %r>' % self.name

class ExpEdu(db.Model):
    __tablename__ = 'expedu'
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(50))
    major = db.Column(db.String(50))
    degree = db.Column(db.String(20))
    datefrom = db.Column(db.Date)
    dateto = db.Column(db.Date)
    def __init__(self, school, major, degree, datefrom, dateto):
        self.school = school
        self.major = major
        self.degree = degree
        self.datefrom = datefrom
        self.dateto = dateto
    def __repr__(self):
        return '<name %r>' % self.school

class ExpWork(db.Model):
    __tablename__ = 'expwork'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(50))
    position = db.Column(db.String(20))
    jobdescription = db.Column(db.Text)
    datefrom = db.Column(db.Date)
    dateto = db.Column(db.Date)
    def __init__(self, company, position, jobdescription, datefrom, dateto):
        self.company = company
        self.position = position
        self.jobdescription = jobdescription
        self.datefrom = datefrom
        self.dateto = dateto
    def __repr__(self):
        return '<name %r>' % self.company

class ExpAward(db.Model):
    __tablename__ = 'expaward'
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date = db.Column(db.Date)
    rank = db.Column(db.String(20))
    def __init__(self, name, date, rank):
        self.name = name
        self.date = date
        self.rank = rank
    def __repr__(self):
        return '<name %r>' % self.name

class Company(db.Model):
    __tablename__ = 'hunter'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5))
    industry = db.Column(db.String(50))
    scale = db.Column(db.Integer)
    info = db.Column(db.Text)
    addr = db.Column(db.String(50))
    tel = db.Column(db.String(11))
    mail = db.Column(db.String(50))
    position1 = db.Column(db.Integer)
    position2 = db.Column(db.Integer)
    position3 = db.Column(db.Integer)

    def __init__(self,name,industry,scale,info,addr,tel,mail,p1,p2,p3):
        self.name = name
        self.industry = industry
        self.scale = scale
        self.info = info
        self.addr = addr
        self.tel = tel
        self.mail = mail
        self.position1 = p1
        self.position2 = p2
        self.position3 = p3
