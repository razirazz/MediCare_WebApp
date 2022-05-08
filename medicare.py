from flask import Flask, render_template, request, session, jsonify
import random
import datetime, time
import dateutil
from encodings.base64_codec import base64_decode
import base64
from templates.DBConnection import Db

app = Flask(__name__)
app.secret_key = "444"
static_path = "D:\\project\\medicare\\medicare\\static\\"


@app.route('/')
def hello_world():
    return render_template('login_index.html')


@app.route('/register_page')
def register_page():
    return render_template('register.html')


@app.route('/login_post', methods=['post'])
def login_post():
    username = request.form['email']
    password = request.form['pass']
    db = Db()
    qry = "SELECT * FROM login WHERE username='" + username + "' AND password='" + password + "'"
    res = db.selectOne(qry)

    if res is not None:
        session['lid'] = res['login_id']
        if res['type'] == 'admin':
            return '''<script>alert('Login Success');window.location='/admin_dashboard'</script>'''
        elif res['type'] == 'Pharmacy':
            return '''<script>alert('Login Success');window.location='/pharmacy_dashboard'</script>'''
        elif res['type'] == 'hospital':
            return '''<script>alert('Login Success');window.location='/hospital_dashboard'</script>'''
        elif res['type'] == 'doctor':
            return '''<script>alert('Login Success');window.location='/doctor_dashboard'</script>'''
        else:
            return '''<script>alert('Invalid User');window.location='/'</script>'''
    else:
        return '''<script>alert('Invalid User');window.location='/'</script>'''


@app.route('/admin_home')
def admin_home():
    return render_template('admin/home.html')


@app.route('/change_pass')
def change_pass():
    return render_template('admin/change_pass.html')


@app.route('/change_pass_post', methods=['post'])
def change_pass_post():
    print(str(session['lid']))
    c_pass = request.form['c_pass']
    new_pass = request.form['new_pass']
    confirm_pass = request.form['confirm_pass']
    db = Db()
    qry = "SELECT * FROM login WHERE password='" + c_pass + "' AND login_id='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    if res is not None:
        if new_pass == confirm_pass:
            # print(str(session['lid']))
            qry = "UPDATE login SET password='" + confirm_pass + "' WHERE login_id='" + str(session['lid']) + "'"
            # print(res)
            res = db.update(qry)
            return '''<script>alert('Password created');window.location='/'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/change_pass'</script>'''
    else:
        return '''<script>alert('Current password must be valid');window.location='/change_pass'</script>'''


@app.route('/view_approve_hospital')
def view_approve_hospital():
    db = Db()
    qry = "SELECT hospital.* FROM hospital,login WHERE login.login_id=hospital.login_id AND login.type='hpending'"
    res = db.select(qry)
    return render_template('admin/view_and_approve_hospital.html', data=res)


@app.route('/view_approve_hospital_post', methods=['post'])
def view_approve_hospital_post():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT hospital.* FROM hospital, login WHERE login.login_id=hospital.login_id AND login.type='hpending' AND hospital.hos_name LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('admin/view_and_approve_hospital.html', data=res)


@app.route('/approved_hospital')
def approved_hospital():
    db = Db()
    qry = "SELECT hospital.* FROM hospital,login WHERE login.login_id=hospital.login_id AND login.type='hospital'"
    res = db.select(qry)
    return render_template('admin/approved_hospital.html', data=res)


@app.route('/admin_search_approved_hospital', methods=['post'])
def admin_search_approved_hospital():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT hospital.* FROM hospital,login WHERE login.login_id=hospital.login_id AND login.type='hospital' AND hospital.hos_name LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('admin/approved_hospital.html', data=res)


@app.route('/rejected_hospital')
def rejected_hospital():
    db = Db()
    qry = "SELECT hospital.* FROM hospital,login WHERE login.login_id=hospital.login_id AND login.type='Rejected'"
    res = db.select(qry)
    return render_template('admin/rejected_hospital.html', data=res)


@app.route('/admin_search_rejected_hospital', methods=['post'])
def admin_search_rejected_hospital():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT hospital.* FROM hospital,login WHERE login.login_id=hospital.login_id AND login.type='Rejected' AND hospital.hos_name LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('admin/rejected_hospital.html', data=res)


@app.route('/view_approve_hospital_approving/<val>')
def view_approve_hospital_approving(val):
    db = Db()
    qry = "UPDATE login SET type='hospital' WHERE login_id='" + val + "'"
    res = db.update(qry)
    return '''<script>alert('Approved..........!!!');window.location='/view_approve_hospital'</script>'''


@app.route('/view_rejected_hospital_approving/<val>')
def view_rejected_hospital_approving(val):
    db = Db()
    qry = "UPDATE login SET type='Rejected' WHERE login_id='" + val + "'"
    res = db.update(qry)
    return '''<script>alert('Rejected..........!!!');window.location='/view_approve_hospital'</script>'''


@app.route('/admin_rejecting_approved_hospital/<val>')
def admin_rejecting_approved_hospital(val):
    db = Db()
    qry = "UPDATE login SET type='Rejected' WHERE login_id='" + val + "'"
    res = db.update(qry)
    return '''<script>alert('Rejected!');window.location='/approved_hospital'</script>'''


@app.route('/admin_approving_rejected_hospital/<val>')
def admin_approving_rejected_hospital(val):
    db = Db()
    qry = "UPDATE login SET type='hospital' WHERE login_id='" + val + "'"
    res = db.update(qry)
    return '''<script>alert('Approved!');window.location='/rejected_hospital'</script>'''


@app.route('/view_all_complaint')
def view_all_complaint():
    db = Db()
    # qry = "SELECT complaint.* , patient.pat_name FROM complaint INNER JOIN patient ON complaint.`pat_lid` = patient.`login_id`"
    qry = "SELECT complaint.* , patient.pat_name, `patient`.`pat_email`, `login`.`username` FROM complaint INNER JOIN patient ON complaint.`pat_lid` = patient.`login_id` INNER JOIN `login` ON `login`.`login_id`=`complaint`.`defendant`"
    res = db.select(qry)
    return render_template('admin/view_all_complaint.html', data=res)


@app.route('/view_pending_complaint')
def view_pending_complaint():
    db = Db()
    # qry = "SELECT complaint.* , patient.pat_name FROM complaint INNER JOIN patient ON complaint.`pat_lid` = patient.`login_id` WHERE `complaint`.`status`='pending'"
    qry = "SELECT complaint.* , patient.pat_name, `patient`.`pat_email`, `login`.`username` FROM complaint INNER JOIN patient ON complaint.`pat_lid` = patient.`login_id` INNER JOIN `login` ON `login`.`login_id`=`complaint`.`defendant` WHERE `complaint`.`status`='pending'"
    res = db.select(qry)
    return render_template('admin/view_pending_complaint.html', data=res)


@app.route('/view_replied_complaint')
def view_replied_complaint():
    db = Db()
    qry = "SELECT complaint.* , patient.pat_name, `patient`.`pat_email`, `login`.`username` FROM complaint INNER JOIN patient ON complaint.`pat_lid` = patient.`login_id` INNER JOIN `login` ON `login`.`login_id`=`complaint`.`defendant` WHERE `complaint`.`status`='replied'"
    res = db.select(qry)
    return render_template('admin/view_replied_complaint.html', data=res)


@app.route('/admin_search_complaint', methods=['post'])
def admin_search_complaint():
    f_date = request.form['f_date']
    t_date = request.form['t_date']
    db = Db()
    qry = "SELECT complaint.* , patient.pat_name FROM complaint INNER JOIN patient ON complaint.`pat_lid` = patient.`login_id` WHERE `complaint`.`status`='pending' AND `complaint`.`comp_date` BETWEEN '" + f_date + "' AND '" + t_date + "'"
    res = db.select(qry)
    return render_template('admin/view_pending_complaint.html', data=res)


@app.route('/complaint_reply_post', methods=['post'])
def complaint_reply_post():
    reply = request.form['reply']
    com_id = session['comp_id']
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    db = Db()
    qry = "UPDATE complaint SET reply='" + reply + "', `reply_date`='" + current_date + "', `complaint`.`reply_time`='" + current_time + "', `status`='replied' WHERE com_id='" + com_id + "'"
    res = db.update(qry)
    return '''<script>alert("Replied Successfully");window.location='/view_pending_complaint'</script>'''


@app.route('/complaint_reply/<val>')
def complaint_reply(val):
    db = Db()
    session['comp_id'] = val
    return render_template("admin/reply.html")


@app.route('/view_doctor')
def view_doctor():
    db = Db()
    # qry = "SELECT doctor.*, hospital.hos_name FROM doctor INNER JOIN hospital ON hospital.login_id = doctor.hos_id"
    qry = "SELECT doctor.*, hospital.hos_name FROM doctor INNER JOIN hospital ON hospital.login_id = doctor.hos_id INNER JOIN `login` ON `login`.`login_id`=`doctor`.`login_id` AND `login`.`type`='dpending'"
    res = db.select(qry)
    return render_template('admin/view_doctor.html', data=res)


@app.route('/admin_search_doctor', methods=['post'])
def admin_search_doctor():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT doctor.*, hospital.hos_name FROM doctor INNER JOIN hospital ON hospital.login_id = doctor.hos_id WHERE `doctor`.`doc_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('admin/view_doctor.html', data=res)


@app.route('/view_approved_doctor')
def view_approved_doctor():
    db = Db()
    qry = "SELECT doctor.*, hospital.hos_name FROM doctor INNER JOIN hospital ON hospital.login_id = doctor.hos_id INNER JOIN `login` ON `login`.`login_id`=`doctor`.`login_id` WHERE `login`.`type`='doctor'"
    res = db.select(qry)
    return render_template('admin/view_approved_doctors.html', data=res)


@app.route('/admin_rejecting_approved_doctor/<val>')
def admin_rejecting_approved_doctor(val):
    db = Db()
    qry = "UPDATE `login` SET `type`='rejected' WHERE `login_id`='" + val + "'"
    res = db.update(qry)
    return '''<script>alert('Doctor Rejected!');window.location='/view_approved_doctor'</script>'''


@app.route('/admin_search_approved_doctors', methods=['post'])
def admin_search_approved_doctors():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT doctor.*, hospital.hos_name FROM doctor INNER JOIN hospital ON hospital.login_id = doctor.hos_id INNER JOIN `login` ON `login`.`login_id`=`doctor`.`login_id` WHERE `login`.`type`='doctor' AND `doctor`.`doc_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('admin/view_approved_doctors.html', data=res)


@app.route('/admin_approve_doctor/<val>')
def admin_approve_doctor(val):
    db = Db()
    qry = "UPDATE `login` SET `type`='doctor' WHERE `login_id`='" + val + "'"
    res = db.update(qry)
    return '''<script>alert("Doctor Approved");window.location='/view_doctor'</script>'''


@app.route('/view_rejected_doctor')
def view_rejected_doctor():
    db = Db()
    qry = "SELECT doctor.*, hospital.hos_name FROM doctor INNER JOIN hospital ON hospital.login_id = doctor.hos_id INNER JOIN `login` ON `login`.`login_id`=`doctor`.`login_id` WHERE `login`.`type`='rejected'"
    res = db.select(qry)
    return render_template('admin/view_rejected_doctor.html', data=res)


@app.route('/admin_approving_rejected_doctor/<val>')
def admin_approving_rejected_doctor(val):
    db = Db()
    qry = "UPDATE `login` SET `type`='doctor' WHERE `login_id`='" + val + "'"
    res = db.update(qry)
    return '''<script>alert('Doctor Approved!');window.location='/view_rejected_doctor'</script>'''


@app.route('/admin_search_rejected_doctor')
def admin_search_rejected_doctor():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT doctor.*, hospital.hos_name FROM doctor INNER JOIN hospital ON hospital.login_id = doctor.hos_id INNER JOIN `login` ON `login`.`login_id`=`doctor`.`login_id` WHERE `login`.`type`='rejected' AND `doctor`.`doc_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('admin/view_rejected_doctor.html', data=res)


@app.route('/admin_reject_doctor/<val>')
def admin_reject_doctor(val):
    db = Db()
    qry = "UPDATE `login` SET `type`='rejected' WHERE `login_id`='" + val + "'"
    res = db.update(qry)
    return '''<script>alert("Doctor Rejected");window.location='/view_doctor'</script>'''


@app.route('/view_patient')
def view_patient():
    db = Db()
    qry = "SELECT * FROM patient"
    res = db.select(qry)
    return render_template('admin/view_patient.html', data=res)


@app.route('/admin_search_patient', methods=['post'])
def admin_search_patient():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT * FROM patient WHERE `pat_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('admin/view_patient.html', data=res)


@app.route('/view_approve_pharmacy')
def view_approve_pharmacy():
    db = Db()
    qry = "SELECT pharmacy.* FROM pharmacy,login WHERE login.login_id=pharmacy.login_id AND login.type='ppending'"
    res = db.select(qry)
    return render_template('admin/view_and_approve_pharmacy.html', data=res)


@app.route('/admin_search_view_approve_pharmacy', methods=['post'])
def admin_search_view_approve_pharmacy():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT pharmacy.* FROM pharmacy,login WHERE login.login_id=pharmacy.login_id AND login.type='ppending' AND pharmacy.phar_name LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('admin/view_and_approve_pharmacy.html', data=res)


@app.route('/view_approve_pharmacy_approving/<val>')
def view_approve_pharmacy_approving(val):
    db = Db()
    qry = "UPDATE login SET type='Pharmacy' WHERE login_id='" + val + "'"
    res = db.update(qry)
    return '''<script>alert('Approved..........!!!');window.location='/view_approve_pharmacy'</script>'''


@app.route('/view_rejected_pharmacy_approving/<val>')
def view_rejected_pharmacy_approving(val):
    db = Db()
    qry = "UPDATE login SET type='Rejected' WHERE login_id='" + val + "'"
    res = db.update(qry)
    return '''<script>alert('Rejected..........!!!');window.location='/view_approve_pharmacy'</script>'''


@app.route('/approved_pharmacy')
def approved_pharmacy():
    db = Db()
    qry = "SELECT pharmacy.* FROM pharmacy,login WHERE login.login_id=pharmacy.login_id AND login.type='Pharmacy'"
    res = db.select(qry)
    return render_template('admin/approved_pharmacy.html', data=res)


@app.route('/admin_rejecting_approved_pharmacy/<val>')
def admin_rejecting_approved_pharmacy(val):
    db = Db()
    qry = "UPDATE login SET type='Rejected' WHERE login_id='" + val + "'"
    res = db.update(qry)
    return '''<script>alert('Rejected!');window.location='/approved_pharmacy'</script>'''


@app.route('/admin_search_approved_pharmacy', methods=['post'])
def admin_search_approved_pharmacy():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT pharmacy.* FROM pharmacy,login WHERE login.login_id=pharmacy.login_id AND login.type='Pharmacy' AND pharmacy.phar_name LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('admin/approved_pharmacy.html', data=res)


@app.route('/rejected_pharmacy')
def rejected_pharmacy():
    db = Db()
    qry = "SELECT pharmacy.* FROM pharmacy,login WHERE login.login_id=pharmacy.login_id AND login.type='Rejected'"
    res = db.select(qry)
    return render_template('admin/rejected_pharmacy.html', data=res)


@app.route('/admin_approving_rejected_pharmacy/<val>')
def admin_approving_rejected_pharmacy(val):
    db = Db()
    qry = "UPDATE login SET type='Pharmacy' WHERE login_id='" + val + "'"
    res = db.update(qry)
    return '''<script>alert('Appreved!');window.location='/rejected_pharmacy'</script>'''


@app.route('/admin_search_rejected_pharmacy', methods=['post'])
def admin_search_rejected_pharmacy():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT pharmacy.* FROM pharmacy,login WHERE login.login_id=pharmacy.login_id AND login.type='Rejected' AND pharmacy.phar_name LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('admin/rejected_pharmacy.html', data=res)


@app.route('/view_medicine')
def view_medicine():
    db = Db()
    qry = "SELECT * FROM medicine"
    res = db.select(qry)
    return render_template('admin/view_medicine.html', data=res)


@app.route('/admin_search_medicine', methods=['post'])
def admin_search_medicine():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT * FROM medicine WHERE med_name LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('admin/view_medicine.html', data=res)


@app.route('/delete_medicine/<val>')
def delete_medicine(val):
    db = Db()
    qry = "DELETE FROM medicine WHERE med_id='" + val + "'"
    res = db.delete(qry)
    return '''<script>alert('Deleted');window.location='/view_medicine'</script>'''


@app.route('/admin_dashboard')
def admin_dashboard():
    db = Db()

    hospital = "SELECT COUNT(*) AS hosp FROM `login` WHERE `type`='hpending'"
    h_res = str(db.select(hospital))
    h_count = h_res[9:-2]

    pharmacy = "SELECT COUNT(*) AS phar FROM `login` WHERE `type`='ppending'"
    p_res = str(db.select(pharmacy))
    p_count = p_res[9:-2]

    doctor = "SELECT COUNT(*) AS doct FROM `login` WHERE `type`='dpending'"
    d_res = str(db.select(doctor))
    d_count = d_res[9:-2]

    complaint = "SELECT COUNT(*) AS comp FROM `complaint` WHERE `status`='pending'"
    c_res = str(db.select(complaint))
    c_count = c_res[9:-2]

    return render_template('admin/admin_dashboard.html', hos=h_count, pharm=p_count, doc=d_count, comp=c_count)


@app.route('/admin_log_out')
def admin_log_out():
    return render_template('login_index.html')


# -----------------HOSPITAL-------------------------------------------------------------------------------------------------------


@app.route('/hospital_signup')
def hospital_signup():
    return render_template('hospital/hospital_signup.html')


@app.route('/hospital_signup_post', methods=['post'])
def hospital_signup_post():
    # hos_lid = request.form['id']
    name = request.form['name']
    mail = request.form['email']
    contact = request.form['contact']
    place = request.form['place']
    post = request.form['post']
    district = request.form['district']
    pin = request.form['pin']
    latitude = request.form['lat']
    longitude = request.form['long']
    pass1 = request.form['p1']
    pass2 = request.form['p2']

    db = Db()
    if pass1 == pass2:
        login_qry = "INSERT INTO login(username, `password`, `type`) VALUES('" + mail + "','" + pass1 + "','hpending')"
        log_id = db.insert(login_qry)
        hos_qry = "INSERT INTO hospital(hos_name, ph_number, place, district, e_mail, hos_lat, hos_long, login_id, pin, post) VALUES('" + name + "', '" + contact + "', '" + place + "', '" + district + "', '" + mail + "', '" + latitude + "', '" + longitude + "', '" + str(
            log_id) + "', '" + pin + "', '" + post + "')"
        hos_data = db.insert(hos_qry)
        return '''<script>alert("Inserted Successfully");window.location='/'</script>'''
    else:
        return '''<script>alert("Invalid password or mismatch");window.location='/hospital_signup'</script>'''


@app.route('/hospital_home')
def hospital_home():
    return render_template('hospital/home.html')


@app.route('/hospital_change_pass')
def hospital_change_pass():
    return render_template('hospital/change_pass.html')


@app.route('/hospital_change_pass_post', methods=['post'])
def hospital_change_pass_post():
    c_pass = request.form['c_pass']
    new_pass = request.form['new_pass']
    confirm_pass = request.form['confirm_pass']
    # print(c_pass+"\n")
    # print(new_pass+"\n")
    # print(confirm_pass)
    db = Db()
    qry = "SELECT * FROM login WHERE password='" + c_pass + "' AND login_id='" + str(session['lid']) + "'"
    # print(qry)
    res = db.selectOne(qry)
    # print(res)
    if res is not None:
        if new_pass == confirm_pass:
            qry = "UPDATE login SET password='" + confirm_pass + "' WHERE login_id='" + str(session['lid']) + "'"
            # print(qry)
            res = db.update(qry)
            # print(res)
            return '''<script>alert('Password created');window.location='/'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/hospital_change_pass'</script>'''
    else:
        return '''<script>alert('Current password must be valid');window.location='/hospital_change_pass'</script>'''


@app.route('/hospital_view_profile')
def hospital_view_profile():
    db = Db()
    qry = "SELECT * FROM hospital WHERE login_id='" + str(session['lid']) + "'"
    res = db.selectOne(qry)

    return render_template('hospital/view_profile.html', data=res)


@app.route('/hospital_edit_profile/<val>')
def hospital_edit_profile(val):
    db = Db()
    qry = "SELECT * FROM hospital WHERE login_id='" + val + "'"
    res = db.selectOne(qry)
    return render_template('hospital/update_hos_profile.html', data=res)


@app.route('/hospital_edit_profile_post', methods=['post'])
def hospital_edit_profile_post():
    hos_lid = request.form['lid']
    name = request.form['name']
    mail = request.form['mail']
    contact = request.form['contact']
    place = request.form['place']
    post = request.form['post']
    district = request.form['district']
    pin = request.form['pin']
    latitude = request.form['lat']
    longitude = request.form['long']

    db = Db()
    qry = "UPDATE hospital SET hos_name='" + name + "', ph_number='" + contact + "', place='" + place + "', district='" + district + "', e_mail='" + mail + "', hos_lat='" + latitude + "', hos_long='" + longitude + "', pin='" + pin + "', post='" + post + "' WHERE login_id='" + hos_lid + "'"
    res = db.update(qry)
    return '''<script>alert("Updated Successfully");window.location='/hospital_view_profile'</script>'''


@app.route('/hospital_add_doctors')
def hospital_add_doctors():
    return render_template('hospital/add_doctor_profile.html')


@app.route('/hospital_add_doctors_post', methods=['post'])
def hospital_add_doctors_post():
    name = request.form['name']
    image = request.files['img']
    dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    image.save(static_path + "hospital\\" + dt + ".jpg")
    path = "/static/hospital/" + dt + ".jpg"
    adrs = request.form['adrs']
    dob = request.form['dob']
    dist = request.form['district']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    dept = request.form['dept']
    quali = request.form['quali']
    exp = request.form['exp']
    contact = request.form['contact']
    mail = request.form['mail']
    fees = request.form['fees']
    password = str(random.randint(0000, 9999))

    db = Db()
    log = "INSERT INTO login (username, password, type) VALUES ('" + mail + "', '" + password + "', 'dpending')"
    doc_lid = db.insert(log)
    qry = "INSERT INTO doctor(doc_name,doc_img,doc_dob,doc_qualification,doc_depart,doc_exp,ph_number,doc_email, hos_id, login_id,place,post,district,pin,address,fees) VALUES ('" + name + "', '" + path + "', '" + dob + "', '" + quali + "', '" + dept + "', '" + exp + "', '" + contact + "', '" + mail + "', '" + str(
        session['lid']) + "', '" + str(
        doc_lid) + "', '" + place + "', '" + post + "', '" + dist + "', '" + pin + "', '" + adrs + "', '" + fees + "')"
    res = db.insert(qry)
    return '''<script>alert('Doctors added Successfully');window.location='/hospital_add_doctors'</script>'''


@app.route('/hospital_edit_doctor/<val>')
def hospital_edit_doctor(val):
    db = Db()
    qry = "SELECT * FROM doctor WHERE doc_id='" + val + "'"
    res = db.selectOne(qry)
    return render_template('hospital/update_doc_profile.html', data=res)


@app.route('/hospital_edit_doctor_post', methods=['post'])
def hospital_edit_doctor_post():
    doc_id = request.form['doc_id']
    name = request.form['name']
    adrs = request.form['adrs']
    dob = request.form['dob']
    dist = request.form['district']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    depart = request.form['dep']
    quali = request.form['qual']
    exp = request.form['exp']
    contact = request.form['contact']
    mail = request.form['mail']
    fees = request.form['fees']

    if 'img' in request.files:
        img = request.files['img']

        dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        img.save(static_path + "hospital\\" + dt + ".jpg")
        path = "/static/hospital" + dt + ".jpg"

        if img.filename != '':
            db = Db()
            qry = "UPDATE doctor SET doc_name='" + name + "', doc_img='" + path + "', doc_dob='" + dob + "', doc_qualification='" + quali + "', doc_depart='" + depart + "', doc_exp='" + exp + "', ph_number='" + contact + "', doc_email='" + mail + "', place='" + place + "', post='" + post + "', district='" + dist + "', pin='" + pin + "', address='" + adrs + "', fees='" + fees + "' WHERE doc_id='" + str(
                doc_id) + "'"
            res = db.update(qry)
            return '''<script>alert('Updated');window.location='/hospital_view_doctor'</script>'''
        else:
            db = Db()
            qry = "UPDATE doctor SET doc_name='" + name + "', doc_dob='" + dob + "', doc_qualification='" + quali + "', doc_depart='" + depart + "', doc_exp='" + exp + "', ph_number='" + contact + "', doc_email='" + mail + "', place='" + place + "', post='" + post + "', district='" + dist + "', pin='" + pin + "', address='" + adrs + "', fees='" + fees + "' WHERE doc_id='" + str(
                doc_id) + "'"
            res = db.update(qry)
            return '''<script>alert('Updated');window.location='/hospital_view_doctor'</script>'''
    else:
        db = Db()
        qry = "UPDATE doctor SET doc_name='" + name + "', doc_dob='" + dob + "', doc_qualification='" + quali + "', doc_depart='" + depart + "', doc_exp='" + exp + "', ph_number='" + contact + "', doc_email='" + mail + "', place='" + place + "', post='" + post + "', district='" + dist + "', pin='" + pin + "', address='" + adrs + "', fees='" + fees + "' WHERE doc_id='" + str(
            doc_id) + "'"
        res = db.update(qry)
        return '''<script>alert('Updated');window.location='/hospital_view_doctor'</script>'''


@app.route('/hospital_delete_doctor/<val>')
def hospital_delete_doctor(val):
    db = Db()
    qry = "DELETE FROM doctor WHERE doc_id='" + val + "'"
    res = db.delete(qry)
    return '''<script>alert("Deleted");window.location='/hospital_view_doctor'</script>'''


@app.route('/hospital_view_doctor')
def hospital_view_doctor():
    db = Db()
    # qry = "SELECT * FROM doctor WHERE hos_id='" + str(session['lid']) + "'"
    qry = "SELECT `doctor`.* FROM `doctor` INNER JOIN `login` ON `doctor`.`login_id`=`login`.`login_id` WHERE `login`.`type`='doctor' AND `doctor`.`hos_id`='" + str(
        session['lid']) + "'"
    res = db.select(qry)
    return render_template('hospital/view_doctor.html', data=res)


@app.route('/hospital_search_doctor', methods=['post'])
def hospital_search_doctor():
    search = request.form['search_field']
    db = Db()
    # qry = "SELECT * FROM doctor WHERE hos_id='" + str(session['lid']) + "' AND `doc_name` LIKE '%" + search + "%'"
    qry = "SELECT `doctor`.* FROM `doctor` INNER JOIN `login` ON `doctor`.`login_id`=`login`.`login_id` WHERE `login`.`type`='doctor' AND `doctor`.`hos_id`='" + str(
        session['lid']) + "' AND `doctor`.`doc_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('hospital/view_doctor.html', data=res)


@app.route('/hospital_view_patient')
def hospital_view_patient():
    db = Db()
    qry = "SELECT `patient`.* FROM `patient` INNER JOIN  `doctor_booking` ON `patient`.`login_id`=`doctor_booking`.`pat_lid` WHERE `doctor_booking`.`hos_lid`='" + str(
        session['lid']) + "' GROUP BY `patient`.`pat_name`"
    res = db.select(qry)
    return render_template('hospital/view_patient.html', data=res)


@app.route('/hospital_search_patient', methods=['post'])
def hospital_search_patient():
    search = request.form['search_field']
    db = Db()
    # qry = "SELECT * FROM patient WHERE `pat_name` LIKE '%" + search + "%'"
    qry = "SELECT `patient`.* FROM `patient` INNER JOIN  `doctor_booking` ON `patient`.`login_id`=`doctor_booking`.`pat_lid` WHERE `doctor_booking`.`hos_lid`='" + str(
        session['lid']) + "' AND `patient`.`pat_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('hospital/view_patient.html', data=res)


@app.route('/hospital_view_booking')
def hospital_view_booking():
    db = Db()
    qry = "SELECT `doctor_booking`.`book_date`, `doctor_booking`.`book_time`, `patient`.*, `doctor`.`doc_name`, `doctor`.`doc_depart`, `doctor`.`fees` FROM `patient` INNER JOIN `doctor_booking` ON `doctor_booking`.`pat_lid`=`patient`.`login_id` INNER JOIN `doctor` ON `doctor_booking`.`doc_lid`=`doctor`.`login_id` WHERE `doctor_booking`.`hos_lid`='" + str(
        session['lid']) + "'"
    res = db.select(qry)
    return render_template('hospital/view_booking.html', data=res)


@app.route('/hospital_search_booking', methods=['post'])
def hospital_search_booking():
    f_date = request.form['f_date']
    t_date = request.form['t_date']
    db = Db()
    qry = "SELECT `doctor_booking`.`book_date`, `doctor_booking`.`book_time`, `patient`.*, `doctor`.`doc_name`, `doctor`.`doc_depart`, `doctor`.`fees` FROM `patient` INNER JOIN `doctor_booking` ON `doctor_booking`.`pat_lid`=`patient`.`login_id` INNER JOIN `doctor` ON `doctor_booking`.`doc_lid`=`doctor`.`login_id` WHERE `doctor_booking`.`hos_lid`='" + str(
        session['lid']) + "' AND `doctor_booking`.`book_date` BETWEEN '" + f_date + "' AND '" + t_date + "'"
    res = db.select(qry)
    return render_template('hospital/view_booking.html', data=res)


@app.route('/hospital_add_schedule')
def hospital_add_schedule():
    db = Db()
    qry = "SELECT `doctor`.*, `login`.`type` FROM `login` INNER JOIN `doctor` ON `doctor`.`login_id`=`login`.`login_id` WHERE `login`.`type`='doctor' AND `doctor`.`hos_id`='" + str(
        session["lid"]) + "'"
    res = db.select(qry)
    return render_template('hospital/add_schedule.html', doctor=res)


@app.route('/hospital_add_schedule_post', methods=['post'])
def hospital_add_schedule_post():
    doctor_id = request.form['name']
    f_time = request.form['ftime']
    t_time = request.form['ttime']
    date = request.form['date']
    db = Db()
    qry = "INSERT INTO `schedule`(`sch_ftime`,`sch_ttime`,`doc_id`,`sch_date`,`hospital_logid`) VALUES('" + f_time + "','" + t_time + "','" + doctor_id + "','" + date + "','" + str(
        session['lid']) + "')"
    res = db.insert(qry)

    return '''<script>alert('schedule updated Successfully');window.location='/hospital_add_schedule'</script>'''


@app.route('/hospital_view_schedule')
def hospital_view_schedule():
    db = Db()
    # qry = "SELECT schedule.*, doctor.doc_name,doctor.doc_depart FROM doctor INNER JOIN `schedule` ON schedule.doc_id=doctor.login_id"
    qry = "SELECT `schedule`.*, `doctor`.`doc_name`, `doctor`.`doc_depart` FROM `doctor` INNER JOIN `schedule` ON `schedule`.`doc_id`=`doctor`.`login_id` WHERE `doctor`.`hos_id`='" + str(
        session['lid']) + "'"
    res = db.select(qry)
    return render_template('hospital/view_schedule.html', data=res)


@app.route('/hospital_search_schedule', methods=['post'])
def hospital_search_schedule():
    fdate = request.form['f_date']
    tdate = request.form['t_date']
    db = Db()
    qry = "SELECT `schedule`.*, `doctor`.`doc_name`, `doctor`.`doc_depart` FROM `doctor` INNER JOIN `schedule` ON `schedule`.`doc_id`=`doctor`.`login_id` WHERE `doctor`.`hos_id`='" + str(
        session['lid']) + "' AND `schedule`.`sch_date` BETWEEN '" + fdate + "' AND '" + tdate + "'"
    res = db.select(qry)
    return render_template('hospital/view_schedule.html', data=res)


@app.route('/hospital_edit_schedule/<val>')
def hospital_edit_schedule(val):
    db = Db()
    qry = "SELECT * FROM schedule WHERE sch_id='" + val + "'"
    res = db.selectOne(qry)
    return render_template('hospital/update_schedule.html', data=res)


@app.route('/hospital_delete_schedule/<val>')
def hospital_delete_schedule(val):
    db = Db()
    qry = "DELETE FROM `schedule` WHERE sch_id='" + val + "'"
    res = db.delete(qry)
    return '''<script>alert("Deleted");window.location='/hospital_view_schedule'</script>'''


@app.route('/hospital_edit_schedule_post', methods=['post'])
def hospital_edit_schedule_post():
    sch_id = request.form['sch_id']
    f_time = request.form['ftime']
    t_time = request.form['ttime']
    date = request.form['date']

    db = Db()
    qry = "UPDATE schedule SET sch_ftime='" + f_time + "', sch_ttime='" + t_time + "', sch_date='" + date + "' WHERE sch_id='" + str(
        sch_id) + "'"
    res = db.update(qry)
    return '''<script>alert("Updated");window.location='/hospital_view_schedule'</script>'''


@app.route('/hospital_log_out')
def hospital_log_out():
    return render_template('login_index.html')


@app.route('/hospital_dashboard')
def hospital_dashboard():
    db = Db()

    doct = "SELECT COUNT(*) AS doctor FROM `doctor` INNER JOIN `login` ON `login`.`login_id`=`doctor`.`login_id` WHERE `login`.`type`='doctor' AND `hos_id`='" + str(
        session['lid']) + "'"
    doct_res = str(db.select(doct))
    d_count = doct_res[12:-2]

    return render_template('hospital/hospital_dashboard.html', doctor=d_count)


# ------------------------------------------------------------------------PHARMACY----------------------------------------------------------------------------------------------------


@app.route('/pharmacy_dashboard')
def pharmacy_dashboard():
    lid = str(session['lid'])
    db = Db()
    book = "SELECT COUNT(*) AS booking FROM `medicine_booking` INNER JOIN `pharmacy` ON `pharmacy`.`login_id`=`medicine_booking`.`phar_lid` WHERE `pharmacy`.`login_id`='" + lid + "'"
    book_res = str(db.select(book))
    book_count = book_res[12:-2]
    medicine = "SELECT COUNT(*) AS medicine FROM `medicine` INNER JOIN `pharmacy` ON `pharmacy`.`login_id`=`medicine`.`phar_lid` WHERE `pharmacy`.`login_id`='" + lid + "'"
    med_res = str(db.select(medicine))
    print(med_res)
    med_count = med_res[14:-2]
    return render_template('pharmacy/pharmacy_dashboard.html', book=book_count, med=med_count)


@app.route('/pharmacy_signup')
def pharmacy_signup():
    return render_template('pharmacy/pharmacy_signup.html')


@app.route('/pharmacy_signup_post', methods=['post'])
def pharmacy_signup_post():
    # hos_lid = request.form['id']
    name = request.form['name']
    mail = request.form['email']
    contact = request.form['contact']
    place = request.form['place']
    post = request.form['post']
    district = request.form['district']
    pin = request.form['pin']
    license_no = request.form['license']
    latitude = request.form['lat']
    longitude = request.form['lon']
    pass1 = request.form['p1']
    pass2 = request.form['p2']

    db = Db()
    if pass1 == pass2:
        login_qry = "INSERT INTO login(username, `password`, `type`) VALUES('" + mail + "','" + pass1 + "','ppending')"
        log_id = db.insert(login_qry)
        hos_qry = "INSERT INTO `pharmacy` (`phar_name`, `phar_number`, `pin`, `e_mail`, `district`, `phar_lat`, `phar_long`, `licence_number`, `login_id`, `post`, `place`) VALUES ('" + name + "', '" + contact + "', '" + pin + "', '" + mail + "', '" + district + "', '" + latitude + "', '" + longitude + "', '" + license_no + "', '" + str(
            log_id) + "', '" + post + "', '" + place + "');"
        hos_data = db.insert(hos_qry)
        return '''<script>alert("Inserted Successfully");window.location='/'</script>'''
    else:
        return '''<script>alert("Invalid password or mismatch");window.location='/pharmacy_signup'</script>'''


@app.route('/pharmacy_home')
def pharmacy_home():
    return render_template('pharmacy/home.html')


@app.route('/pharmacy_change_password')
def pharmacy_change_password():
    return render_template('pharmacy/change_pass.html')


@app.route('/pharmacy_change_pass_post', methods=['post'])
def pharmacy_change_pass_post():
    c_pass = request.form['c_pass']
    new_pass = request.form['new_pass']
    confirm_pass = request.form['confirm_pass']
    db = Db()
    qry = "SELECT * FROM login WHERE password='" + c_pass + "' AND login_id='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    if res is not None:
        if new_pass == confirm_pass:
            qry = "UPDATE login SET password='" + confirm_pass + "' WHERE login_id='" + str(session['lid']) + "'"
            res = db.update(qry)
            return '''<script>alert('Password changed');window.location='/'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/pharmacy_change_pass'</script>'''
    else:
        return '''<script>alert('Current password must be valid');window.location='/pharmacy_change_pass'</script>'''


@app.route('/pharmacy_view_profile')
def pharmacy_view_profile():
    db = Db()
    qry = "SELECT * FROM pharmacy WHERE login_id='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    return render_template('pharmacy/view_profile.html', data=res)


@app.route('/pharmacy_edit_profile')
def pharmacy_edit_profile():
    db = Db()
    qry = "SELECT * FROM pharmacy WHERE login_id='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    return render_template('pharmacy/update_profile.html', data=res)


@app.route('/pharmacy_edit_profile_post', methods=['post'])
def pharmacy_edit_profile_post():
    pharm_lid = request.form['lid']
    name = request.form['name']
    contact = request.form['contact']
    pin = request.form['pin']
    mail = request.form['mail']
    district = request.form['district']
    latitude = request.form['lat']
    longitude = request.form['long']
    license_no = request.form['license']
    post = request.form['post']
    place = request.form['place']
    db = Db()
    qry = "UPDATE pharmacy SET phar_name='" + name + "', phar_number='" + contact + "', pin='" + pin + "', e_mail='" + mail + "', district='" + district + "', phar_lat='" + latitude + "', phar_long='" + longitude + "', licence_number='" + license_no + "', post='" + post + "', place='" + place + "' WHERE login_id='" + pharm_lid + "'"
    res = db.update(qry)
    return '''<script>alert("Updated Successfully");window.location='/pharmacy_view_profile'</script>'''


@app.route('/pharmacy_view_medicine')
def pharmacy_view_medicine():
    db = Db()
    qry = "SELECT * FROM medicine WHERE phar_lid='" + str(session['lid']) + "'"
    res = db.select(qry)
    return render_template('pharmacy/view_medicine.html', data=res)


@app.route('/pharmacy_search_medicine', methods=['post'])
def pharmacy_search_medicine():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT * FROM medicine WHERE phar_lid='5' AND `med_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('pharmacy/view_medicine.html', data=res)


@app.route('/pharmacy_add_medicine')
def pharmacy_add_medicine():
    return render_template('pharmacy/add_medicine.html')


@app.route('/pharmacy_add_medicine_post', methods=['post'])
def pharmacy_add_medicine_post():
    name = request.form['name']
    image = request.files['img']
    dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    image.save(static_path + "medicine\\" + dt + ".jpg")
    path = "/static/medicine/" + dt + ".jpg"
    price = request.form['price']
    description = request.form['desc']
    brand = request.form['brand']
    quantity = request.form['quantity']
    db = Db()
    qry_medicine = "INSERT INTO `medicine`(`med_name`, `med_img`, `price`, `description`, `med_brand`, `phar_lid`) VALUES ('" + name + "', '" + path + "', '" + price + "', '" + description + "', '" + brand + "', '" + str(
        session['lid']) + "')"
    res_med = db.insert(qry_medicine)
    qry_stock = "INSERT INTO `stock` (`quantity`, `med_lid`, `phar_lid`) VALUES ('" + quantity + "', '" + str(
        res_med) + "', '" + str(session['lid']) + "')"
    res_stock = db.insert(qry_stock)
    return '''<script>alert("Medicine added successfully");window.location='/pharmacy_add_medicine'</script>'''


@app.route('/pharmacy_edit_medicine/<val>')
def pharmacy_edit_medicine(val):
    db = Db()
    qry = "SELECT * FROM `medicine` WHERE `med_id`='" + val + "'"
    res = db.selectOne(qry)
    return render_template('pharmacy/update_medicine.html', data=res)


@app.route('/pharmacy_edit_medicine_post', methods=['post'])
def pharmacy_edit_medicine_post():
    med_id = request.form['medic_id']
    name = request.form['name']
    price = request.form['price']
    description = request.form['desc']
    brand = request.form['brand']

    if 'img' in request.files:
        img = request.files['img']

        dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        img.save(static_path + "medicine\\" + dt + ".jpg")
        path = "/static/medicine" + dt + ".jpg"

        db = Db()
        if img.filename != '':
            qry = "UPDATE `medicine` SET `med_name`='" + name + "', `med_img`='" + path + "', `price`='" + price + "', `description`='" + description + "', `med_brand`='" + brand + "' WHERE `med_id`='" + med_id + "'"
            res = db.update(qry)
            return '''<script>alert("Medicine Updated Successfully");window.location='/pharmacy_view_medicine
            '</script> '''
        else:
            qry = "UPDATE `medicine` SET `med_name`='" + name + "', `price`='" + price + "', `description`='" + description + "', `med_brand`='" + brand + "' WHERE `med_id`='" + med_id + "'"
            res = db.update(qry)
            return '''<script>alert("Medicine Updated Successfully");window.location='/pharmacy_view_medicine
            '</script>'''


@app.route('/pharmacy_delete_medicine_post/<val>')
def pharmacy_delete_medicine_post(val):
    db = Db()
    qry = "DELETE FROM `medicine` WHERE `med_id`='" + val + "'"
    res = db.delete(qry)
    return '''<script>alert("Deleted Successfully");window.location='/pharmacy_view_medicine'</script>'''


@app.route('/pharmacy_view_patient')
def pharmacy_view_patient():
    db = Db()
    qry = "SELECT `patient`.*, `medicine_booking`.`patient_lid`, `medicine_booking`.`phar_lid` FROM `patient` INNER JOIN `medicine_booking` ON `patient`.pat_id=`medicine_booking`.`patient_lid` AND `medicine_booking`.`phar_lid`='" + str(
        session['lid']) + "'"
    # print(qry)
    res = db.select(qry)
    # print(res)
    return render_template('pharmacy/view_patient.html', data=res)


@app.route('/pharmacy_search_patient', methods=['post'])
def pharmacy_search_patient():
    search = request.form['search_field']
    db = Db()
    qry = "SELECT `patient`.*, `medicine_booking`.pat_id, `medicine_booking`.`phar_lid` FROM `patient` INNER JOIN `medicine_booking` ON `patient`.pat_id=`medicine_booking`.pat_id AND `medicine_booking`.`phar_lid`='" + str(
        session['lid']) + "' AND `patient`.`pat_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('pharmacy/view_patient.html', data=res)


@app.route('/pharmacy_view_booking')
def pharmacy_view_booking():
    db = Db()
    qry = "SELECT `medicine_booking`.*, `patient`.`pat_name`, `patient`.`pat_email`, `patient`.`pat_number` FROM `patient` INNER JOIN `medicine_booking` ON `medicine_booking`.`patient_lid`=`patient`.`login_id` WHERE `medicine_booking`.`phar_lid`='" + str(
        session['lid']) + "'"
    # qry = "SELECT `medicine_booking`.*, `patient`.`pat_name`, `patient`.`pat_email`, `patient`.`pat_number` FROM `patient` INNER JOIN `medicine_booking` ON `medicine_booking`.`patient_lid`=`patient`.`login_id` WHERE `medicine_booking`.`phar_lid`='" + str(session['lid']) + "' GROUP BY `patient`.`login_id`=''"
    res = db.select(qry)
    # print(res)
    return render_template('pharmacy/view_med_booking.html', data=res)


@app.route('/pharmacy_view_more_booking/<val>')
def pharmacy_view_more_booking(val):
    db = Db()
    qry = "SELECT `med_booking_sub`.*, `medicine_booking`.date, `medicine`.* FROM `medicine_booking` INNER JOIN `med_booking_sub` ON `med_booking_sub`.`med_book_id`=`medicine_booking`.`medbook_id` INNER JOIN `medicine` ON `medicine`.`med_id`=`med_booking_sub`.`med_id` WHERE `medicine_booking`.`medbook_id`='" + val + "'"
    res = db.selectOne(qry)
    return render_template('pharmacy/view_more_booking.html', data=res)


@app.route('/pharmacy_search_booking', methods=['post'])
def pharmacy_search_booking():
    search = request.form['search_field']
    print(search)
    db = Db()
    qry = "SELECT `medicine_booking`.*, `patient`.`pat_name`, `patient`.`pat_email`, `patient`.`pat_number` FROM `patient` INNER JOIN `medicine_booking` ON `medicine_booking`.`patient_lid`=`patient`.`login_id` WHERE `medicine_booking`.`phar_lid`='" + str(
        session['lid']) + "' AND `patient`.`pat_name` LIKE '%" + search + "%'"
    print(qry)
    res = db.select(qry)
    return render_template('pharmacy/view_med_booking.html', data=res)


# ================= PHARMACY SEARCH MEDICINE ===================================================================================

# @app.route('/pharmacy_search_medicine', methods=['post'])
# def pharmacy_search_medicine():
#     search = request.form['search_field']
#     db = Db()
#     qry = "SELECT `medicine_booking`.*, `patient`.`pat_name`, `patient`.`pat_email`, `patient`.`pat_number` FROM `patient` INNER JOIN `medicine_booking` ON `medicine_booking`.`patient_lid`=`patient`.`login_id` WHERE `medicine_booking`.`phar_lid`='"+str(session['lid'])+"' AND "
#     res = db.select(qry)
#     return render_template('pharmacy/view_med_booking.html', data=res)


# =================================================================================================================


@app.route('/pharmacy_view_stock')
def pharmacy_view_stock():
    db = Db()
    qry = "SELECT `stock`.*, `medicine`.`med_name`, `medicine`.`med_brand` FROM `stock` INNER JOIN `medicine` ON `stock`.`med_lid`=`medicine`.`med_id` WHERE `stock`.`phar_lid`='" + str(
        session['lid']) + "'"
    res = db.select(qry)
    return render_template('pharmacy/view_stock.html', data=res)


@app.route('/pharmacy_search_stock', methods=['post'])
def pharmacy_search_stock():
    search = request.form['search']
    db = Db()
    qry = "SELECT `stock`.*, `medicine`.`med_name`, `medicine`.`med_brand` FROM `stock` INNER JOIN `medicine` ON `stock`.`med_lid`=`medicine`.`med_id` WHERE `stock`.`phar_lid`='" + str(
        session['lid']) + "' AND `medicine`.`med_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('pharmacy/view_stock.html', data=res)


@app.route('/pharmacy_update_stock/<val>')
def pharmacy_update_stock(val):
    db = Db()
    # qry = "SELECT `stock`.`quantity`, `medicine`.`med_name`, `medicine`.`med_brand` FROM `stock` INNER JOIN `medicine` ON `stock`.`stock_id`='"+ id +"'"
    qry = "SELECT * FROM stock WHERE stock_id='" + val + "'"
    res = db.selectOne(qry)
    return render_template('pharmacy/update_stock.html', data=res)


@app.route('/pharmacy_update_stock_post', methods=['post'])
def pharmacy_update_stock_post():
    s_id = request.form['s_id']
    quantity = request.form['quantity']
    db = Db()
    qry = "UPDATE `stock` SET `quantity`='" + quantity + "' WHERE `stock_id`='" + str(s_id) + "'"
    res = db.update(qry)
    return '''<script>alert("Updated Successfully");window.location='/pharmacy_view_stock'</script>'''


@app.route('/pharmacy_delete_stock/<val>')
def pharmacy_delete_stock(val):
    db = Db()
    del_stock = "DELETE FROM `stock` WHERE `stock_id`='" + val + "'"
    res = db.delete(del_stock)
    # del_med = ""
    # res = db.delete(del_med)
    return '''<script>alert("Deleted Successfully");window.location='/pharmacy_view_stock'</script>'''


# @app.route('/pharmacy_view_discount')
# def pharmacy_view_discount():
#     db = Db()
#     qry = "SELECT `discount`.*, `medicine`.* FROM `medicine` INNER JOIN `discount` ON `discount`.`med_id`=`medicine`.`med_id` AND `discount`.`phar_lid`='" + str(
#         session['lid']) + "'"
#     res = db.select(qry)
#     return render_template('pharmacy/view_discount.html', data=res)


@app.route('/pharmacy_add_discount')
def pharmacy_add_discount():
    db = Db()
    qry = "SELECT `medicine`.* FROM `medicine` INNER JOIN `pharmacy` ON `pharmacy`.`login_id`=`medicine`.`phar_lid` WHERE `medicine`.`phar_lid`='" + str(
        session['lid']) + "'"
    res = db.select(qry)
    return render_template('pharmacy/add_discount.html', medicine=res)


@app.route('/brandload', methods=['post'])
def brandload():
    db = Db()
    e = request.form['ff']
    qry = "SELECT med_brand FROM `medicine` WHERE med_id='" + e + "'"
    res = db.selectOne(qry)
    data = {"data": res}
    return jsonify(res)


@app.route('/pharmacy_add_discount_post', methods=['post'])
def pharmacy_add_discount_post():
    med_id = request.form['name']
    offer = request.form['offer']
    ftime = request.form['ftime']
    ttime = request.form['ttime']
    fdate = request.form['fdate']
    tdate = request.form['tdate']

    db = Db()
    qry = "INSERT INTO `discount`(`med_id`,`dis_ftime`,`dis_ttime`,`phar_lid`,`offer`,`dis_fdate`,`dis_tdate`)VALUES('" + med_id + "', '" + ftime + "', '" + ttime + "', '" + str(
        session['lid']) + "', '" + offer + "', '" + fdate + "', '" + tdate + "')"
    res = db.insert(qry)
    return '''<script>alert("Discount added Successfully");window.location='/pharmacy_view_discount'</script>'''


@app.route('/pharmacy_update_discount/<val>')
def pharmacy_update_discount(val):
    db = Db()
    qry = "SELECT `discount`.*, `medicine`.* FROM `medicine` INNER JOIN `discount` ON `discount`.`med_id`=`medicine`.`med_id` AND `discount`.`dis_id`='" + val + "'"
    res = db.selectOne(qry)
    return render_template('pharmacy/update_discount.html', data=res)


@app.route('/pharmacy_update_discount_post', methods=['post'])
def pharmacy_update_discount_post():
    dis_id = request.form['dis_id']
    offer = request.form['offer']
    fdate = request.form['fdate']
    tdate = request.form['tdate']
    ftime = request.form['ftime']
    ttime = request.form['ttime']

    db = Db()
    qry = "UPDATE `discount` SET `dis_ftime`='" + ftime + "', `dis_ttime`='" + ttime + "', `offer`='" + offer + "', `dis_fdate`='" + fdate + "', `dis_tdate`='" + tdate + "' WHERE `phar_lid`='" + str(
        session['lid']) + "'"
    res = db.update(qry)
    return '''<script>alert("Updated Successfully");window.location='/pharmacy_view_discount'</script>'''


@app.route('/pharmacy_delete_discount/<id>')
def pharmacy_delete_discount(id):
    db = Db()
    qry = "DELETE FROM `discount` WHERE `dis_id`='" + id + "'"
    res = db.delete(qry)
    return '''<script>alert("Deleted Successfully");window.location='/pharmacy_view_discount'</script>'''


@app.route('/pharmacy_view_other_discount')
def pharmacy_view_other_discount():
    db = Db()
    qry = "SELECT `discount`.*, `pharmacy`.*, `medicine`.`med_name`, `medicine`.`med_brand` FROM `pharmacy` INNER JOIN `discount` ON `discount`.`phar_lid`=`pharmacy`.`login_id` INNER JOIN `medicine` ON `discount`.`med_id`=`medicine`.`med_id` WHERE `discount`.`phar_lid`!='" + str(
        session['lid']) + "'"
    res = db.select(qry)
    return render_template('pharmacy/view_discount_others.html', data=res)


@app.route('/pharmacy_search_other_discount', methods=['post'])
def pharmacy_search_other_discount():
    search = request.form['search']
    db = Db()
    qry = "SELECT `discount`.*, `pharmacy`.*, `medicine`.`med_name`, `medicine`.`med_brand` FROM `pharmacy` INNER JOIN `discount` ON `discount`.`phar_lid`=`pharmacy`.`login_id` INNER JOIN `medicine` ON `discount`.`med_id`=`medicine`.`med_id` WHERE `discount`.`phar_lid`!='" + str(
        session['lid']) + "' AND `pharmacy`.`phar_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('pharmacy/view_discount_others.html', data=res)


@app.route('/pharmacy_view_sales_report')
def pharmacy_view_sales_report():
    db = Db()
    qry = "SELECT SUM(`med_booking_sub`.`quantity`) AS med_quantity, SUM(`med_booking_sub`.`cost`) AS total_amount, `medicine`.*, `med_booking_sub`.* FROM `med_booking_sub` INNER JOIN `medicine` ON `medicine`.`med_id`=`med_booking_sub`.`med_id` GROUP BY `medicine`.`med_name`"
    res = db.select(qry)
    return render_template('pharmacy/view_sales_report.html', data=res)


@app.route('/pharmacy_view_sales_report_more/<val>')
def pharmacy_view_sales_report_more(val):
    db = Db()
    qry = "SELECT SUM(`med_booking_sub`.`quantity`) AS med_quantity, SUM(`med_booking_sub`.`cost`) AS total_amount, `medicine`.*, `med_booking_sub`.*, `medicine_booking`.* FROM `med_booking_sub` INNER JOIN `medicine` ON `medicine`.`med_id`=`med_booking_sub`.`med_id` INNER JOIN `medicine_booking` ON `medicine_booking`.`medbook_id`=`med_booking_sub`.`med_book_id` WHERE `medicine`.`med_id`='" + val + "' GROUP BY `medicine_booking`.`date`"
    res = db.select(qry)
    return render_template('pharmacy/view_more_sales_report.html', data=res)


@app.route('/pharmacy_search_sales_report', methods=['post'])
def pharmacy_search_sales_report():
    search = request.form['search_field']
    print(search)
    db = Db()
    qry = "SELECT SUM(`med_booking_sub`.`quantity`) AS med_quantity, SUM(`med_booking_sub`.`cost`) AS total_amount, `medicine`.*, `med_booking_sub`.* FROM `med_booking_sub` INNER JOIN `medicine` ON `medicine`.`med_id`=`med_booking_sub`.`med_id` GROUP BY `medicine`.`med_name` AND `medicine`.`med_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('pharmacy/view_sales_report.html', data=res)


@app.route('/pharmacy_logout')
def pharmacy_logout():
    return render_template('login.html')


# ---+++++++++-==============================--DOCTOR------++++++++++++++----==========================-----------+++++++++++++++++++++++++++-------------


@app.route('/doctor_signup')
def doctor_signup():
    return render_template('doctor/doctor_signup.html')


@app.route('/doctor_home')
def doctor_home():
    return render_template('doctor/home.html')


@app.route('/doctor_dashboard')
def doctor_dashboard():
    db = Db()

    schedule = "SELECT COUNT(*) AS sche FROM `schedule` WHERE `doc_id`='" + str(session['lid']) + "'"
    s_res = str(db.select(schedule))
    schedule_count = s_res[9:-2]

    booking = "SELECT COUNT(*) AS book FROM `doctor_booking` WHERE `doc_lid`='" + str(session['lid']) + "'"
    b_res = str(db.select(booking))
    booking_count = b_res[9:-2]

    return render_template('doctor/doctor_dashboard.html', schedule=schedule_count, booking=booking_count)


@app.route('/doctor_change_password')
def doctor_change_password():
    return render_template('doctor/change_pass.html')


@app.route('/doctor_change_pass_post', methods=['post'])
def doctor_change_pass_post():
    c_pass = request.form['c_pass']
    new_pass = request.form['new_pass']
    confirm_pass = request.form['confirm_pass']
    db = Db()
    qry = "SELECT * FROM login WHERE password='" + c_pass + "' AND login_id='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    if res is not None:
        if new_pass == confirm_pass:
            qry = "UPDATE login SET password='" + confirm_pass + "' WHERE login_id='" + str(session['lid']) + "'"
            res = db.update(qry)
            return '''<script>alert('Password Changed');window.location='/'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/doctor_change_password'</script>'''
    else:
        return '''<script>alert('Current password must be valid');window.location='/doctor_change_password'</script>'''


@app.route('/doctor_view_profile')
def doctor_view_profile():
    db = Db()
    qry = "SELECT * FROM `doctor` WHERE `login_id`='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    return render_template('doctor/view_profile.html', data=res)


@app.route('/doctor_update_profile')
def doctor_update_profile():
    db = Db()
    qry = "SELECT * FROM `doctor` WHERE `login_id`='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    return render_template('doctor/update_profile.html', data=res)


@app.route('/doctor_update_profile_post', methods=['post'])
def doctor_update_profile_post():
    doc_id = request.form['doc_id']
    name = request.form['name']
    adrs = request.form['adrs']
    dob = request.form['dob']
    dist = request.form['district']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    depart = request.form['dep']
    quali = request.form['qual']
    exp = request.form['exp']
    contact = request.form['contact']
    mail = request.form['mail']
    fees = request.form['fees']

    db = Db()
    if 'img' in request.files:
        img = request.files['img']

        dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        img.save(static_path + "hospital\\" + dt + ".jpg")
        path = "/static/hospital" + dt + ".jpg"

        if img.filename != '':
            qry = "UPDATE doctor SET doc_name='" + name + "', doc_img='" + path + "', doc_dob='" + dob + "', doc_qualification='" + quali + "', doc_depart='" + depart + "', doc_exp='" + exp + "', ph_number='" + contact + "', doc_email='" + mail + "', place='" + place + "', post='" + post + "', district='" + dist + "', pin='" + pin + "', address='" + adrs + "', fees='" + fees + "' WHERE doc_id='" + str(
                doc_id) + "'"
            res = db.update(qry)
            return '''<script>alert('Updated');window.location='/doctor_view_profile'</script>'''
        else:
            qry = "UPDATE doctor SET doc_name='" + name + "', doc_dob='" + dob + "', doc_qualification='" + quali + "', doc_depart='" + depart + "', doc_exp='" + exp + "', ph_number='" + contact + "', doc_email='" + mail + "', place='" + place + "', post='" + post + "', district='" + dist + "', pin='" + pin + "', address='" + adrs + "', fees='" + fees + "' WHERE doc_id='" + str(
                doc_id) + "'"
            res = db.update(qry)
            return '''<script>alert('Updated');window.location='/doctor_view_profile'</script>'''
    else:
        qry = "UPDATE doctor SET doc_name='" + name + "', doc_dob='" + dob + "', doc_qualification='" + quali + "', doc_depart='" + depart + "', doc_exp='" + exp + "', ph_number='" + contact + "', doc_email='" + mail + "', place='" + place + "', post='" + post + "', district='" + dist + "', pin='" + pin + "', address='" + adrs + "', fees='" + fees + "' WHERE doc_id='" + str(
            doc_id) + "'"
        res = db.update(qry)
        return '''<script>alert('Updated');window.location='/doctor_view_profile'</script>'''


@app.route('/doctor_view_schedule')
def doctor_view_schedule():
    db = Db()
    qry = "SELECT * FROM `schedule` WHERE `doc_id`='" + str(session['lid']) + "'"
    res = db.select(qry)
    return render_template('doctor/view_schedule.html', data=res)


@app.route('/doctor_view_booking')
def doctor_view_booking():
    db = Db()
    qry = "SELECT `doctor_booking`.*, `patient`.* FROM `patient` INNER JOIN `doctor_booking` ON `doctor_booking`.`pat_lid`=`patient`.`login_id` WHERE `doctor_booking`.`status`='pending' AND `doctor_booking`.`doc_lid`='" + str(
        session['lid']) + "'"
    res = db.select(qry)
    return render_template('doctor/view_booking.html', data=res)


@app.route('/doctor_search_booking', methods=['post'])
def doctor_search_booking():
    search = request.form['search']
    db = Db()
    qry = "SELECT `doctor_booking`.`book_date`, `doctor_booking`.`book_time`, `patient`.* FROM `patient` INNER JOIN `doctor_booking` ON `doctor_booking`.`pat_lid`=`patient`.`login_id` WHERE `doctor_booking`.`status`='pending' AND `doctor_booking`.`doc_lid`='" + str(
        session['lid']) + "' AND `patient`.`pat_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('doctor/view_booking.html', data=res)


@app.route('/doctor_search_prescription_date')
def doctor_search_prescription_date():
    db = Db()
    qry = "SELECT `prescription`.*, `patient`.* FROM `patient` INNER JOIN `prescription` ON `prescription`.`pat_id`=`patient`.`login_id` WHERE `prescription`.`doc_id`='" + str(
        session['lid']) + "'"
    res = db.select(qry)
    return render_template('doctor/view_prescription.html', data=res)


@app.route('/doctor_search_prescription_post', methods=['post'])
def doctor_search_prescription_date_post():
    search = request.form['search']
    db = Db()
    qry = "SELECT * FROM `prescription`, `patient` WHERE `prescription`.`pat_id`=`patient`.`login_id` AND `patient`.`pat_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return render_template('doctor/view_prescription.html', data=res)


@app.route('/doctor_add_prescription/<val>')
def doctor_add_prescription(val):
    session['db_id'] = val
    return render_template('doctor/add_prescription.html')


# @app.route('/pat_name_load_wrt_db_id', methods=['post'])
# def pat_name_load_wrt_db_id():
#     db = Db()
#     e = request.form['ff']
#     qry = "SELECT `patient`.`pat_name` FROM `patient` INNER JOIN `doctor_booking` ON `doctor_booking`.`pat_lid`=`patient`.`login_id` WHERE`doctor_booking`.`db_id`='" + e + "'"
#     res = db.selectOne(qry)
#     print(res)
#     data = {"data": res}
#     return jsonify(res)


@app.route('/doctor_add_prescription_post', methods=['post'])
def doctor_add_prescription_post():
    pres = request.form['presc']
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H:%M:%S')
    db = Db()
    pat_id_qry = "SELECT `patient`.`login_id` FROM `patient` INNER JOIN `doctor_booking` ON `doctor_booking`.`pat_lid`=`patient`.`login_id` WHERE `doctor_booking`.`db_id`='" + str(
        session['db_id']) + "'"
    pat_id = db.selectOne(pat_id_qry)
    insert_qry = "INSERT INTO `prescription`(`doc_id`, `date`, `time`, `pat_id`, `db_id`, `prescription`) VALUES ('" + str(
        session['lid']) + "', '" + date + "', '" + time + "', '" + str(pat_id['login_id']) + "', '" + str(
        session['db_id']) + "', '" + pres + "')"
    res = db.insert(insert_qry)
    update_status_query = "UPDATE `doctor_booking` SET `status`='consulted' WHERE `db_id`='" + str(
        session['db_id']) + "' AND `pat_lid`='" + str(pat_id['login_id']) + "' AND `doc_lid`='" + str(
        session['lid']) + "'"
    update_status = db.update(update_status_query)
    return '''<script>alert('Prescription Added Successfully');window.location='/doctor_view_booking'</script>'''


# @app.route('/doctor_video_chat')
# def doctor_video_chat():
#     return render_template('doctor/video_chat.html')


@app.route('/doctor_text_chat')
def doctor_text_chat():
    db = Db()
    qry = "SELECT `chat`.*, `patient`.* FROM `patient` INNER JOIN `chat` ON `patient`.`login_id`=`chat`.`from_lid` WHERE `chat`.`to_lid`='" + str(session['lid']) + "' GROUP BY `chat`.`from_lid`"
    res = db.select(qry)
    return render_template('doctor/text_chat.html', data=res)


@app.route('/doctor_search_chat', methods=['post'])
def doctor_search_chat():
    search = request.form['search']
    db = Db()
    qry = "SELECT `chat`.*, `patient`.* FROM `patient` INNER JOIN `chat` ON `patient`.`login_id`=`chat`.`from_lid` WHERE `chat`.`to_lid`='" + str(session['lid']) + "' AND `patient`.`pat_name` LIKE '%" + search + "%' GROUP BY `chat`.`from_lid`"
    res = db.select(qry)
    return render_template('doctor/text_chat.html', data=res)


@app.route('/doctor_text_chat_view_more/<val>')
def doctor_text_chat_view_more(val):
    db = Db()
    qry = "SELECT `chat`.*, `patient`.* FROM `patient` INNER JOIN `chat` ON `patient`.`login_id`=`chat`.`from_lid` WHERE `chat`.`to_lid`='" + str(session['lid']) + "' AND `chat`.`from_lid`='" + val + "'"
    res = db.select(qry)
    # print("----------------------------------------------------------",res['from_lid'])
    return render_template('doctor/text_chat_view_more.html', data=res)


@app.route('/doctor_chat_reply/<val>')
def doctor_chat_reply(val):
    db = Db()
    session['chat_pat_id'] = val
    return render_template('doctor/reply.html')


@app.route('/doctor_chat_reply_post', methods=['post'])
def doctor_chat_reply_post():
    pat_lid = session['chat_pat_id']
    reply = request.form['reply']
    db = Db()
    qry = "INSERT INTO `chat` (`from_lid`, `to_lid`, `msg`, `date`, `time`) VALUES ('" + str(session['lid']) + "', '" + str(pat_lid) + "', '" + reply + "', curdate(), curtime())"
    res = db.insert(qry)
    return '''<script>alert("Reply sent successfully");window.location='/doctor_text_chat'</script>'''


# ======================TEMPLATES============================


@app.route('/admin_index')
def admin_index():
    return render_template('admin/admin_index.html')


@app.route('/hospital_index')
def hospital_index():
    return render_template('hospital/hospital_index.html')


@app.route('/pharmacy_index')
def pharmacy_index():
    return render_template('pharmacy/pharmacy_index.html')


@app.route('/doctor_index')
def doctor_index():
    return render_template('doctor/doctor_index.html')


@app.route('/doctor_log_out')
def doctor_log_out():
    return render_template('login_index.html')


# ========================= ANDROID ==========================


@app.route('/patient_login', methods=['post'])
def patient_login():
    print("================================hello")
    user_name = request.form['user_name']
    password = request.form['password']
    db = Db()
    qry = "SELECT * FROM login WHERE username='" + user_name + "' AND password='" + password + "'"
    res = db.selectOne(qry)
    print(res)
    if res is not None:
        return jsonify(status='ok', lid=res['login_id'], type=res['type'])
    else:
        return jsonify(status="no")


@app.route('/patient_signup', methods=['post'])
def patient_signup():
    name = request.form['name']
    image = request.form['photo']
    timestr = time.strftime("%Y%m%d-%H%M%S")
    a = base64.b64decode(image)
    fh = open("D:\\project\\medicare\\medicare\\static\\patient\\" + timestr + ".jpg", "wb")
    pic = "/static/patient/" + timestr + ".jpg"
    fh.write(a)
    fh.close()
    contact = request.form['contact']
    mail = request.form['e_mail']
    gender = request.form['gender']
    dob = request.form['dob']
    address = request.form['address']
    post = request.form['post']
    place = request.form['place']
    pin = request.form['pin']
    district = request.form['district']
    password = request.form['password']
    confirm_pass = request.form['confirm_pass']

    if password == confirm_pass:
        db = Db()
        qry_lid = "INSERT INTO `login`(`username`, `password`, `type`) VALUES ('" + mail + "', '" + password + "', 'patient')"
        res_lid = db.insert(qry_lid)
        qry = "INSERT INTO `patient`(`pat_name`, `pat_place`, `pat_number`, `gender`, `dob`, `pin`, `post`, `district`, `img`, `pat_email`, `login_id`, `address`) VALUES ('" + name + "', '" + place + "', '" + contact + "', '" + gender + "', '" + dob + "', '" + pin + "', '" + post + "', '" + district + "', '" + pic + "', '" + mail + "', '" + str(
            res_lid) + "', '" + address + "')"
        res = db.insert(qry)
        return jsonify(status='ok')
    else:
        return jsonify(status='Password mismatch')


@app.route("/patient_change_password", methods=['post'])
def patient_change_password():
    lid = request.form['lid']
    current_pass = request.form['currentpassword']
    new_pass = request.form['newpassword']
    db = Db()
    qry = "SELECT * FROM login WHERE PASSWORD='" + current_pass + "' AND login_id='" + lid + "'"
    res = db.selectOne(qry)
    if res is not None:
        qry2 = "UPDATE login SET PASSWORD='" + new_pass + "' WHERE login_id='" + lid + "'"
        db.update(qry2)
        return jsonify(status="ok")
    else:
        return jsonify(status="no")


@app.route('/patient_view_profile', methods=['post'])
def patient_view_profile():
    db = Db()
    lid = request.form['lid']
    qry = "SELECT * FROM `patient` WHERE `login_id`='" + str(lid) + "'"
    print(qry)
    res = db.selectOne(qry)
    birth_date = res['dob']
    ff = str(birth_date)
    try:
        dd = ff.split("/")
        print(dd)
        dvd = dd[2] + "-" + dd[1] + "-" + dd[0]
    except:
        dd = ff.split("-")
        print(dd)
        dvd = dd[2] + "-" + dd[1] + "-" + dd[0]
    return jsonify(status='ok', name=res['pat_name'], place=res['pat_place'], contact=res['pat_number'],
                   gender=res['gender'], birth_date=dvd, pin=res['pin'], post=res['post'], district=res['district'],
                   email=res['pat_email'], address=res['address'], photo=res['img'])


@app.route('/patient_update_profile', methods=['post'])
def patient_update_profile():
    name = request.form['name']
    # print(name)
    image = request.form['photo']
    contact = request.form['contact']
    mail = request.form['email']
    gender = request.form['gender']
    dob = request.form['date_birth']
    address = request.form['address']
    post = request.form['post']
    place = request.form['place']
    pin = request.form['pin']
    district = request.form['district']
    pat_lid = request.form['lid']
    db = Db()
    print(image)
    if image != "aa":
        print("yes...pics....!!!")
        timestr = time.strftime("%Y%m%d-%H%M%S")
        a = base64.b64decode(image)
        fh = open("D:\\project\\medicare\\medicare\\static\\patient\\" + timestr + ".jpg", "wb")
        pic = "/static/patient/" + timestr + ".jpg"
        fh.write(a)
        fh.close()
        qry = "UPDATE `patient` SET `pat_name`='" + name + "', `pat_place`='" + place + "', `pat_number`='" + contact + "', `gender`='" + gender + "', `dob`='" + dob + "', `pin`='" + pin + "', `post`='" + post + "', `district`='" + district + "', `img`='" + pic + "', `pat_email`='" + mail + "', `address`='" + address + "' WHERE `login_id`='" + pat_lid + "'"
        res = db.update(qry)
        # print(qry)
        return jsonify(status='ok')
    else:
        print("no...pics....!!!")
        qry = "UPDATE `patient` SET `pat_name`='" + name + "', `pat_place`='" + place + "', `pat_number`='" + contact + "', `gender`='" + gender + "', `dob`='" + dob + "', `pin`='" + pin + "', `post`='" + post + "', `district`='" + district + "', `pat_email`='" + mail + "', `address`='" + address + "' WHERE `login_id`='" + pat_lid + "'"
        res = db.update(qry)
        print(res)
        return jsonify(status='ok')


@app.route('/patient_view_doctor', methods=['post'])
def patient_view_doctor():
    db = Db()
    # qry = "SELECT * FROM `doctor`"
    # qry = "SELECT `doctor`.*, `hospital`.`hos_name` FROM `hospital` INNER JOIN `doctor` ON `doctor`.`hos_id`=`hospital`.`login_id`"
    qry = "SELECT `doctor`.*, `hospital`.`hos_name` FROM `hospital` INNER JOIN `doctor` ON `doctor`.`hos_id`=`hospital`.`login_id` INNER JOIN `login` ON `login`.`login_id`=`doctor`.`login_id` WHERE `login`.`type`='doctor'"
    res = db.select(qry)
    return jsonify(status='ok', data=res)


@app.route('/patient_v_search_doctor', methods=['post'])
def patient_v_search_doctor():
    search = request.form['name']
    db = Db()
    qry = "SELECT `doctor`.*, `hospital`.`hos_name` FROM `hospital` INNER JOIN `doctor` ON `doctor`.`hos_id`=`hospital`.`login_id` WHERE `doctor`.`doc_name` LIKE '%" + search + "%'"
    print(qry)
    res = db.select(qry)
    print(res)
    return jsonify(status='ok', data=res)


@app.route('/patient_view_doctor_profile', methods=['post'])
def patient_view_doctor_profile():
    doc_id = request.form['doctorlid']
    # print("doc_id------------------------------0",doc_id)
    db = Db()
    qry = "SELECT `doctor`.*,`hospital`.* FROM `hospital` INNER JOIN `doctor` ON `doctor`.`hos_id`=`hospital`.`login_id` WHERE `doctor`.`login_id`='" + str(
        doc_id) + "'"
    # print(qry)
    res = db.selectOne(qry)
    # print(res)
    if res is not None:
        return jsonify(status='ok', doc_name=res['doc_name'], hos_name=res['hos_name'], department=res['doc_depart'],
                       quali=res['doc_qualification'], experience=res['doc_exp'], fees=res['fees'],
                       contact=res['ph_number'], email=res['doc_email'], img=res['doc_img'])
        # return jsonify(status='ok', data=res)
    else:
        return jsonify(status="no")


@app.route('/patient_view_medicine', methods=['post'])
def patient_view_medicine():
    db = Db()
    qry = "SELECT * FROM `medicine`"
    res = db.select(qry)
    return jsonify(status='ok', data=res)


@app.route('/patient_v_medicine_search', methods=['post'])
def patient_v_medicine_search():
    name = request.form['name']
    db = Db()
    qry = "SELECT * FROM `medicine` WHERE `med_name` LIKE '%" + name + "%'"
    res = db.select(qry)
    return jsonify(status='ok', data=res)


@app.route('/patient_view_medicine_profile', methods=['post'])
def patient_view_medicine_profile():
    login_id = request.form['lid']
    db = Db()
    qry = "SELECT * FROM `medicine` WHERE `med_id`='" + str(login_id) + "'"
    res = db.selectOne(qry)
    print(res)
    return jsonify(status='ok', name=res['med_name'], med_img=res['med_img'], price=res['price'], description=res['description'],
                   brand=res['med_brand'])


@app.route('/patient_view_discount', methods=['post'])
def patient_view_discount():
    db = Db()
    qry = "SELECT `medicine`.*, `discount`.`offer`, `discount`.`offer_price`, `discount`.`dis_id` FROM `medicine` INNER  JOIN `discount` ON `discount`.`med_id`=`medicine`.`med_id` "
    res = db.select(qry)
    # print(res)
    return jsonify(status='ok', data=res)


@app.route('/patient_view_discount_profile', methods=['post'])
def patient_view_discount_profile():
    dis_id = request.form['lid']
    # print("---------patient_view_discount_profile----dus_id-------"+dis_id)
    db = Db()
    qry = "SELECT `discount`.*, `medicine`.* FROM `medicine` INNER JOIN `discount` ON `discount`.`med_id`=`medicine`.`med_id` WHERE `discount`.`med_id`='" + str(
        dis_id) + "'"
    res = db.selectOne(qry)
    # print("---------patient_view_discount_profile----res-------",qry)
    # print(res['dis_fdate'])
    f_date = res['dis_fdate']
    t_date = res['dis_tdate']
    f_time = res['dis_ftime']
    t_time = res['dis_ttime']

    print("from time====", f_time)
    print("to time====", t_time)

    date = t_date - f_date
    print("++++++++++++++++++++", date)
    form_ftime = datetime.datetime.strptime(f_time, '%H:%M')
    form_ttime = datetime.datetime.strptime(t_time, '%H:%M')
    print(datetime.datetime.strptime(f_time, '%H:%M'))
    print(datetime.datetime.strptime(t_time, '%H:%M'))
    return jsonify(status='ok', name=res['med_name'], brand=res['med_brand'], description=res['description'],
                   price=res['price'], offer_price=res['offer_price'], offer_details=res['offer'], offer_date=date,
                   offer_time=time)


@app.route('/patient_add_complaint', methods=['post'])
def patient_add_compliant():
    return jsonify(status='ok')


@app.route('/patient_view_near_by_pharmacy', methods=['post'])
def patient_view_near_by_pharmacy():
    latitude = request.form['lati']
    longitude = request.form['longi']
    db = Db()
    qry = "SELECT `pharmacy`.*, SQRT(POW(69.1 * (`phar_lat` - '" + latitude + "'), 2) + POW(69.1 * ('" + longitude + "' - `phar_long`) * COS(`phar_lat` / 57.3), 2)) AS distance FROM `pharmacy` HAVING distance < 2500 ORDER BY distance;"
    print(qry)
    res = db.select(qry)
    return jsonify(status='ok', data=res)


@app.route('/patient_v_pharmacy_search', methods=['post'])
def patient_v_pharmacy_search():
    latitude = request.form['lati']
    longitude = request.form['longi']
    search = request.form['search']
    db = Db()
    qry = "SELECT `pharmacy`.*, SQRT(POW(69.1 * (`phar_lat` - '" + latitude + "'), 2) + POW(69.1 * ('" + longitude + "' - `phar_long`) * COS(`phar_lat` / 57.3), 2)) AS distance FROM `pharmacy` HAVING distance < 2500 AND `phar_name` LIKE '%" + search + "%' ORDER BY distance;"
    print(qry)
    res = db.select(qry)
    return jsonify(status='ok', data=res)


@app.route('/patient_view_near_by_hospital', methods=['post'])
def patient_view_near_by_hospital():
    latitude = request.form['lati']
    longitude = request.form['longi']
    db = Db()
    qry = "SELECT `hospital`.*, SQRT(POW(69.1 * (`hos_lat` - '" + latitude + "'), 2) +POW(69.1 * ('" + longitude + "' - `hos_long`) * COS(`hos_lat` / 57.3), 2)) AS distance FROM `hospital` HAVING distance < 2500 ORDER BY distance;"
    res = db.select(qry)
    print(res)
    return jsonify(status='ok', data=res)


@app.route('/patient_v_hospital_search', methods=['post'])
def patient_v_hospital_search():
    latitude = request.form['lati']
    longitude = request.form['longi']
    search = request.form['search']
    db = Db()
    qry = "SELECT `hospital`.*, SQRT(POW(69.1 * (`hos_lat` - '" + latitude + "'), 2) +POW(69.1 * ('" + longitude + "' - `hos_long`) * COS(`hos_lat` / 57.3), 2)) AS distance FROM `hospital` HAVING distance < 2500 AND `hos_name` LIKE '%" + search + "%' ORDER BY distance;"
    res = db.select(qry)
    print(res)
    return jsonify(status='ok', data=res)


@app.route('/patient_view_schedule', methods=['post'])
def patient_view_schedule():
    doc_lid = request.form['doctorlid']
    print("-------------------------------------doc_lid---", doc_lid)
    db = Db()
    qry = "SELECT `schedule`.*, `hospital`.*, `doctor`.* FROM `hospital` INNER JOIN `schedule` ON `hospital`.`login_id`=`schedule`.`hospital_logid` INNER JOIN `doctor` ON `doctor`.`login_id`=`schedule`.`doc_id` WHERE `doctor`.`login_id`='" + str(doc_lid) + "'"
    res = db.select(qry)
    if len(res) > 0:
        ls = []
        for i in res:
            q = "SELECT COUNT(`sch_id`) as cnt FROM `doctor_booking` WHERE `sch_id`='" + str(i["sch_id"]) + "'"
            d = Db()
            r = d.selectOne(q)
            if r is not None:
                if r["cnt"] >= 2:
                    pass
                else:
                    a = {'login_id':i['login_id'], 'sch_id':i['sch_id'], 'hos_id':i['hos_id'], 'doc_name':i['doc_name'], 'hos_name':i['hos_name'], 'doc_depart':i['doc_depart'], 'sch_date':i['sch_date'], 'sch_ftime':i['sch_ftime'], 'sch_ttime':i['sch_ttime']}
                    ls.append(a)
            else:
                    a = {'login_id':i['login_id'], 'sch_id':i['sch_id'], 'hos_id':i['hos_id'], 'doc_name':i['doc_name'], 'hos_name':i['hos_name'], 'doc_depart':i['doc_depart'], 'sch_date':i['sch_date'], 'sch_ftime':i['sch_ftime'], 'sch_ttime':i['sch_ttime']}
                    ls.append(a)
        return jsonify(status='ok', data=ls)
    else:
        return jsonify(status='no')


@app.route('/patient_v_schedule_search', methods=['post'])
def patient_v_schedule_search():
    doc_lid = request.form['doctorlid']
    search = request.form['search']
    db = Db()
    qry = "SELECT `schedule`.*, `doctor`.*, `hospital`.* FROM `doctor` INNER JOIN `schedule` ON `schedule`.`doc_id`=`doctor`.`login_id` INNER JOIN `hospital` ON `hospital`.`login_id`=`schedule`.`hospital_logid` WHERE `doctor`.`login_id`='" + str(doc_lid) + "' AND `doctor`.`doc_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return jsonify(status='ok', data=res)


@app.route('/patient_book_doctors', methods=['post'])
def patient_book_doctors():
    doc_id = request.form['doctorlid']
    print("-----------------------------------------------------------------------------------doctorlid", doc_id)
    sch_id = request.form['sch_id']
    hos_id = request.form['hos_id']
    lid = request.form['lid']
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    db = Db()
    qry = "INSERT INTO `doctor_booking` (`sch_id`, `book_date`, `book_time`, `pat_lid`, `status`, `doc_lid`, `hos_lid`) VALUES ('" + sch_id + "', '" + current_date + "', '" + current_time + "', '" + lid + "', 'pending', '" + doc_id + "', '" + hos_id + "')"
    print(qry)
    res = db.insert(qry)
    print('-------------res---', res)
    return jsonify(status='ok')


@app.route('/patient_med_add_to_cart', methods=['post'])
def patient_med_add_to_cart():
    med_id = request.form['med_id']
    pat_id = request.form['lid']
    db = Db()
    qry = "INSERT INTO `cart` (`med_lid`, `pat_lid`) VALUES ('" + med_id + "', '" + pat_id + "')"
    res = db.insert(qry)
    return jsonify(status='ok')


@app.route('/patient_med_buy', methods=['post'])
def patient_med_buy():
    phar_id = request.form['pharm_lid']
    pat_lid = request.form['lid']
    amount = request.form['price']
    med_id = request.form['med_id']
    quantity = request.form['quantity']
    cost = int(quantity) * int(amount)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    db = Db()
    qc = "SELECT `quantity` FROM `stock` WHERE `med_lid`='" + med_id + "'"
    r = db.selectOne(qc)
    print(qc)
    if r is not None:
        if int(r["quantity"]) >= int(quantity):
            qry = "INSERT INTO `medicine_booking` (`date`, `total_amount`, `phar_lid`, `patient_lid`, `status`) VALUES ('" + current_date + "', '" + amount + "', '" + phar_id + "', '" + pat_lid + "', 'pending')"
            res = db.insert(qry)
            qry_sub = "INSERT INTO `med_booking_sub` (`med_id`, `time`, `quantity`, `cost`, `med_book_id`) VALUES ('" + med_id + "', curtime(), '" + quantity + "', '" + str(cost) + "', '" + str(res) + "')"
            res_sub = db.insert(qry_sub)
            q = "UPDATE `stock` SET `quantity`=`quantity`-'"+quantity+"' WHERE `med_lid`='" + med_id + "'"
            db.update(q)
            return jsonify(status='ok')
        else:
            return jsonify(status='low')
    return jsonify(status='no')


@app.route('/patient_doc_payment', methods=['post'])
def patient_doc_payement():
    acc_no = request.form['acc_no']
    pin_no = request.form['pin_no']
    book_id = request.form['med_book_id']
    amount = request.form['amount']
    db = Db()
    check_bank = "SELECT * FROM `bank` WHERE `acc_no`='" + acc_no + "' AND `bank_pin`='" + pin_no + "'"
    res_bank = db.selectOne(check_bank)
    # print(res_bank['bank_balance'])
    if res_bank is not None:
        if res_bank['bank_balance'] > int(amount):
            qry = "INSERT INTO `payment` (`med_book_id`, `date`, `time`, `amount`, `type`) VALUES ('" + str(
                book_id) + "', curdate(), curtime(), '" + amount + "', 'doctor')"
            print(qry)
            res = db.insert(qry)
            qry333 = "UPDATE `bank` SET `bank_balance`=`bank_balance`-'" + str(
                amount) + "' WHERE `acc_no`='" + acc_no + "' AND `bank_pin`='" + pin_no + "'"
            res333 = db.update(qry333)
            qry_status = "UPDATE `doctor_booking` SET `status`='paid' WHERE `db_id`='" + str(book_id) + "'"
            res_status = db.update(qry_status)
            return jsonify(status='ok')
        else:
            return jsonify(status='less')
    else:
        return jsonify(status='no')


@app.route('/patient_med_payment', methods=['post'])
def patient_med_payment():
    acc_no = request.form['acc_no']
    pin_no = request.form['pin_no']
    book_id = request.form['med_book_id']
    amount = request.form['amount']

    print(book_id,"=====================")
    # print(acc_no)
    # print(pin_no)
    # print("--------------amount", amount)
    db = Db()
    check_bank = "SELECT * FROM `bank` WHERE `acc_no`='" + acc_no + "' AND `bank_pin`='" + pin_no + "'"
    res_bank = db.selectOne(check_bank)
    print(res_bank['bank_balance'])
    if res_bank is not None:
        if res_bank['bank_balance'] > int(amount):
            qry = "INSERT INTO `payment` (`med_book_id`, `date`, `time`, `amount`, `type`) VALUES ('" + str(
                book_id) + "', curdate(), curtime(), '" + amount + "', 'medicine')"
            print(qry)
            res = db.insert(qry)
            qry333 = "UPDATE `bank` SET `bank_balance`=`bank_balance`-'" + str(
                amount) + "' WHERE `acc_no`='" + acc_no + "' AND `bank_pin`='" + pin_no + "'"
            res333 = db.update(qry333)
            med_status_qry = "UPDATE `medicine_booking` SET `status`='paid' WHERE  `medbook_id`='" + str(book_id) + "'"
            med_status_res = db.update(med_status_qry)
            return jsonify(status='ok')
        else:
            return jsonify(status='less')
    else:
        return jsonify(status='no')


@app.route('/patient_view_doc_booking', methods=['post'])
def patient_view_doc_booking():
    pat_lid = request.form['lid']
    print(pat_lid)
    db = Db()
    qry = "SELECT `doctor_booking`.*, `doctor`.* FROM `doctor` INNER JOIN `doctor_booking` ON `doctor_booking`.`doc_lid`=`doctor`.`login_id` WHERE `doctor_booking`.`pat_lid`='" + pat_lid + "' AND `doctor_booking`.`status`='pending'"
    print(qry)
    res = db.select(qry)
    print(res)
    if res is not None:
        return jsonify(status='ok', data=res)
    else:
        return jsonify(status='none')


@app.route('/patient_v_doc_booking_search', methods=['post'])
def patient_v_doc_booking_search():
    pat_lid = request.form['lid']
    search = request.form['search']
    db = Db()
    qry = "SELECT `doctor_booking`.*, `doctor`.* FROM `doctor` INNER JOIN `doctor_booking` ON `doctor_booking`.`doc_lid`=`doctor`.`login_id` WHERE `doctor_booking`.`pat_lid`='" + pat_lid + "' AND `doctor_booking`.`status`='pending' AND `doctor`.`doc_name` LIKE '%" + search + "%'"
    res = db.select(qry)
    return jsonify(status='ok', data=res)


@app.route('/patient_view_med_booking', methods=['post'])
def patient_view_med_booking():
    pat_lid = request.form['lid']
    db = Db()
    qry = "SELECT `med_booking_sub`.*, `medicine_booking`.*, `medicine`.* FROM `medicine_booking` INNER JOIN `med_booking_sub` ON `med_booking_sub`.`med_book_id`=`medicine_booking`.`medbook_id` INNER JOIN `medicine` ON `medicine`.`med_id`=`med_booking_sub`.`med_id` WHERE `medicine_booking`.`patient_lid`='" + pat_lid + "' AND `medicine_booking`.`status`='pending'"
    res = db.select(qry)
    if res is not None:
        return jsonify(status='ok', data=res)
    else:
        return jsonify(status='no')


@app.route("/and_send_complaint", methods=['post'])
def and_send_complaint():
    lid = request.form['lid']
    complaint = request.form['complaint']
    db = Db()
    qry = "INSERT INTO `complaint` (`pat_lid`,`complaint`, `comp_date`, `comp_time`, `status`) VALUES ('" + lid + "', '" + complaint + "', CURDATE(), CURTIME(), 'pending')"
    db.insert(qry)
    return jsonify(status="ok")


@app.route("/and_view_complaint", methods=['post'])
def and_view_complaint():
    lid = request.form['lid']
    db = Db()
    qry = "SELECT * FROM `complaint` WHERE `pat_lid`='" + lid + "'"
    res = db.select(qry)
    return jsonify(status="ok", data=res)


@app.route('/in_message2', methods=['POST'])
def message():
    fr_id = request.form["fid"]
    to_id = request.form["toid"]
    message = request.form["msg"]
    print(fr_id)
    query7 = "INSERT INTO `chat`(`from_lid`, `to_lid`, `msg`, `date`, `time`) VALUES ('" + fr_id + "' ,'" + to_id + "','" + message + "',CURDATE(),CURTIME())"
    print(query7)
    db = Db()
    res = db.insert(query7)
    if res == 1:
        return jsonify(status='send')
    else:
        return jsonify(status='failed')


@app.route('/view_message2', methods=['POST'])
def msg():
    fid = request.form["fid"]
    toid = request.form["toid"]
    lmid = request.form['lastmsgid']
    db = Db()
    query = "SELECT `from_lid`, `msg`, `date`, `chat_id` FROM `chat` WHERE `chat_id`>'" + lmid + "' AND ((`to_lid`='" + toid + "' AND  `from_lid`='" + fid + "') OR (`to_lid`='" + fid + "' AND `from_lid`='" + toid + "')  )  ORDER BY `chat_id` ASC"
    sen = db.select(query)
    return jsonify(status='not found', res1=sen)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
