#! coding:utf-8
import os,time
from app import app, db
from flask import render_template, redirect, url_for, session, abort
from models import User, Positon, ExpAward, ExpEdu, ExpWork, Student, Company, StuPosition
from forms import LoginForm
from flask import request
from qiniu import Auth, put_file, etag

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
    if not session.has_key ('username'):
        return redirect (url_for ('login'))
    company = Company.query.filter_by (id=session['username']).first ()
    if company == None:
        abort (404)
    positions = Positon.query.filter_by(company_name=company.name).all()
    return render_template('postpt.html',company=company,positions=positions)


@app.route ('/index', methods=['POSt', 'GET'])
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
    uid = session['username']
    relations = StuPosition.query.filter_by(uid=uid).all()
    positions = []
    for r in relations:
        p = Positon.query.get(r.pid)
        positions.append(p)
    return render_template ("mydelivery.html", positions=positions)


@app.route ('/jobdetail/<id>')
def jobdetail(id):
    position = Positon.query.get(id)
    if position:
        re = position.requirements
        return render_template ("jobdetail.html", position=position, rl=re.split (';'),uid=session['username'])
    else:
        abort(404)


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
    mail = request.args.get('mail')
    tel = request.args.get('tel')
    stu = Student (sno, name, sex, age, degree, None, tel, mail, '南京林业大学', major, '',institute, 0, 0, 0, 0, 0, 0, 0, 0, 0,
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
    db.session.commit()
    user = Company.query.filter_by(name=name).first ()
    user = User(user.id, '123456', 2)
    db.session.add(user)
    db.session.commit()
    return str (com.id)

@app.route('/addPosition')
def addPosition():
    print request.args
    cname = request.args.get('cname')
    name = request.args.get('name')
    salary = request.args.get('salary')
    num = request.args.get('num')
    edu = request.args.get('degree')
    city = request.args.get('city')
    description = request.args.get('info')
    requirements = request.args.get('req')
    create_date = time.strftime('%Y-%m-%d')
    position = Positon(cname,name,salary,num,edu,'',city,description,requirements,0,create_date)
    db.session.add(position)
    db.session.commit()
    return cname

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
@app.route('/jobdetail/delivery')
def delivery():
    print request.args
    uid = request.args.get('uid')
    pid = request.args.get('pid')
    ddate = time.strftime("%Y-%m-%d")

    item = StuPosition(uid,pid,ddate)
    db.session.add(item)
    db.session.commit()

    position = Positon.query.get(pid)
    position.deliveried += 1
    db.session.add(position)
    db.session.commit()
    return uid

@app.route('/deliveried/<pid>')
def deliveried(pid):
    sids = StuPosition.query.filter_by(pid=pid).all()
    students = []
    print len(sids)
    for id in sids:
        students.append(Student.query.filter_by(uid=id.uid).first())
        print students
    return render_template('deliveried.html', students=students)