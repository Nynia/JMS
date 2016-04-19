#! coding:utf-8
import os,time
from app import app, db
from flask import render_template, redirect, url_for, session, abort
from models import User, Positon, ExpAward, ExpEdu, ExpWork, Student, Company
from forms import LoginForm
from flask import request
from qiniu import Auth, put_file, etag


class loginSession (object):
    id = 0
    name = ''
    type = 0
    status = 'out'

    @classmethod
    def login(self, id, name, type):
        loginSession.id = id
        loginSession.name = name
        loginSession.type = type
        loginSession.status = 'in'

    def logout(self):
        loginSession.status = 'out'


@app.errorhandler (404)
def page_not_found(error):
    return render_template ('404.html'), 404


@app.route ('/')
@app.route ('/login')
def login():
    form = LoginForm ()
    return render_template ('login.html', form=form)


@app.route ('/adminSM')
def adminSM():
    students = Student.query.all ()
    return render_template ('adminSM.html', students=students)


@app.route ('/adminCM')
def adminCM():
    companys = Company.query.all ()
    return render_template ('adminCM.html', companys=companys)


@app.route ('/postpt')
def postpt():
    company = Company.query.filter_by ()


@app.route ('/index', methods=['POSt', 'GEt'])
def index():
    users = User.query.all ()
    username = request.form['username']
    password = request.form['password']
    flag = False
    for u in users:
        if u.loginname == username and u.loginpassword == password:
            flag = True
            session['username'] = request.form['username']
            # loginSession.login(u.id, u.loginname, u.type)
            if u.type == 1:
                return redirect (url_for ('jobtrends'))
            elif u.type == 2:
                return redirect (url_for ('postpt'))
            else:
                return redirect (url_for ('adminSM'))
    if flag == False:
        return redirect (url_for ('login'))


@app.route ('/profile')
def profile():
    if not session.has_key ('username'):
        return redirect (url_for ('login'))
    student = Student.query.filter_by (uid=session['username']).first ()
    if student == None:
        abort (404)
    expedu = []
    expwork = []
    expaward = []
    expedu.append (ExpEdu.query.get (student.expedu1))
    expedu.append (ExpEdu.query.get (student.expedu2))
    expedu.append (ExpEdu.query.get (student.expedu3))
    for i in range (3):
        if expedu[i] == None:
            expedu = expedu[0:i]
            break
    expwork.append (ExpWork.query.get (student.expwork1))
    expwork.append (ExpWork.query.get (student.expwork2))
    expwork.append (ExpWork.query.get (student.expwork3))
    expwork.append (ExpWork.query.get (student.expwork4))
    for i in range (4):
        if expwork[i] == None:
            expwork = expwork[0:i]
            break
    expaward.append (ExpAward.query.get (student.expaward1))
    expaward.append (ExpAward.query.get (student.expaward2))
    expaward.append (ExpAward.query.get (student.expaward3))
    expaward.append (ExpAward.query.get (student.expaward4))
    for i in range (4):
        if expaward[i] == None:
            expaward = expaward[0:i]
            break

    return render_template ("profile.html", baseinfo=student, exp=(expedu, expwork, expaward))


@app.route ('/jobtrends')
def jobtrends():
    positions = Positon.query.all ()
    return render_template ("jobtrends.html", positions=positions)


@app.route ('/mydelivery')
def mydelivery():
    return render_template ("mydelivery.html")


@app.route ('/jobdetail/<id>')
def jobdetail(id):
    position = Positon.query.get (id)
    if position:
        re = position.requirements
        return render_template ("jobdetail.html", position=position, rl=re.split (';'))
    else:
        return redirect (url_for ('404'))


@app.route ('/addStu')
def addStu():
    print request.args
    sno = request.args.get ('sno')
    name = request.args.get ('name')
    sex = request.args.get ('sex')
    age = request.args.get ('age')
    degree = request.args.get ('degree')
    major = request.args.get ('major')
    institute = request.args.get ('institute')
    stu = Student (sno, name, sex, age, degree, None, None, None, '南京林业大学', major, institute, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0)
    user = User (sno, '123456', 1)
    db.session.add (stu)
    db.session.add (user)
    db.session.commit ()
    return sno


@app.route ('/addCom')
def addCom():
    print request.args
    name = request.args.get ('name')
    industry = request.args.get ('industry')
    scale = request.args.get ('scale')
    info = request.args.get ('info')
    addr = request.args.get ('addr')
    tel = request.args.get ('tel')
    mail = request.args.get ('mail')
    com = Company (name, industry, scale, info, addr, tel, mail, 0, 0, 0)
    db.session.add (com)
    db.session.commit ()
    return str (com.id)


@app.route ('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file.save (os.path.join ("./upload", filename))

        # 需要填写你的 Access Key 和 Secret Key
        access_key = 'jJnJu4_d7YH8hhhB-J4J8Jr537T_-yk9BIsin75M'
        secret_key = 'WpidgDmScl866DLV22LT2Qon19oDkiLmRbxhDrGq'
        # 构建鉴权对象
        q = Auth (access_key, secret_key)
        # 要上传的空间
        bucket_name = 'head'
        # 上传到七牛后保存的文件名
        key = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.jpg'
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token (bucket_name, key, 3600)
        # 要上传文件的本地路径
        localfile = os.path.join ("./upload", filename)
        print os.getcwd ()

        ret, info = put_file (token, key, localfile)
        print(info.status_code)
        assert ret['key'] == key
        assert ret['hash'] == etag (localfile)
        if info.status_code == 200:
            stu = Student.query.filter_by (uid=session['username']).first ()
            stu.photo = 'http://7xt3t1.com2.z0.glb.clouddn.com/' + key
            db.session.add(stu)
            db.session.commit()

        if not session.has_key ('username'):
            return redirect (url_for ('login'))
        student = Student.query.filter_by (uid=session['username']).first ()
        if student == None:
            abort (404)
        expedu = []
        expwork = []
        expaward = []
        expedu.append (ExpEdu.query.get (student.expedu1))
        expedu.append (ExpEdu.query.get (student.expedu2))
        expedu.append (ExpEdu.query.get (student.expedu3))
        for i in range (3):
            if expedu[i] == None:
                expedu = expedu[0:i]
                break
        expwork.append (ExpWork.query.get (student.expwork1))
        expwork.append (ExpWork.query.get (student.expwork2))
        expwork.append (ExpWork.query.get (student.expwork3))
        expwork.append (ExpWork.query.get (student.expwork4))
        for i in range (4):
            if expwork[i] == None:
                expwork = expwork[0:i]
                break
        expaward.append (ExpAward.query.get (student.expaward1))
        expaward.append (ExpAward.query.get (student.expaward2))
        expaward.append (ExpAward.query.get (student.expaward3))
        expaward.append (ExpAward.query.get (student.expaward4))
        for i in range (4):
            if expaward[i] == None:
                expaward = expaward[0:i]
                break
        return render_template ("profile.html", baseinfo=student, exp=(expedu, expwork, expaward))
    return '''
    <!DOCTYPE html>
    <title>Upload New File</title>
    <h1>Upload File</h1>
    <form action="/upload" method="POST" enctype="multipart/form-data">
    <input type="file" name="file" />
    <input type="submit" value="Upload" />
    </form>
    '''
