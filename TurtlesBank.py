from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TurtlesBank.db'
db = SQLAlchemy(app)

class credentials(db.Model):                                        #Table for Password
    un = db.Column(db.String, primary_key=True)
    pas = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

def auto_cid():
    if not customer.query.all():
        return 100000001
    else:
        C = db.session.query(customer).order_by(customer.cid.desc()).first()
        c = C.cid + 1
        return c
class customer(db.Model):                                           #Table for Customer Data
    cid = db.Column(db.Integer, primary_key=True, default=auto_cid)
    cname = db.Column(db.String(30), nullable=False)
    cadr = db.Column(db.Integer, unique=True, nullable=False)
    cage = db.Column(db.Integer, nullable=False)
    cadd = db.Column(db.Text, nullable=False)
    cmsg = db.Column(db.String(30), nullable=False)
    cdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def auto_aid():
    if not account.query.all():
        return 200000001
    else:
        A = db.session.query(account).order_by(account.aid.desc()).first()
        a = A.aid + 1
        return a
class account(db.Model):                                            #Table for Account Data
    aid = db.Column(db.Integer, primary_key=True, default=auto_aid)
    atyp = db.Column(db.String, nullable=False)
    amt = db.Column(db.Integer, nullable=False)
    amsg = db.Column(db.String(30), nullable=False)
    adate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ahol = db.Column(db.Integer, nullable=False)

def auto_tid():
    if not transaction.query.all():
        return 300000001
    else:
        T = db.session.query(transaction).order_by(transaction.tid.desc()).first()
        t = T.tid + 1
        return t
class transaction(db.Model):                                        #Table for Transaction Data
    tid = db.Column(db.Integer, primary_key=True, default=auto_tid)
    tmsg = db.Column(db.String(30), nullable=False)
    tamt = db.Column(db.Integer, nullable=False)
    tdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tacc = db.Column(db.Integer, nullable=False)

@app.route('/')                                                     #Login for CAE/Cashier
def login():
    if "red" in session:
        return redirect(url_for(session["red"]))
    return render_template("login.html")

@app.route('/check', methods=["GET", "POST"])                       #credentials Checking
def check():
    if "red" in session:
        return redirect(url_for(session["red"]))
    else:
        if request.method == "POST":
            a = request.form.get("un")
            b = request.form.get("pas")
            if credentials.query.filter_by(un=a, pas=b, role="cae").all():
                session["un"] = request.form.get("un")
                session["red"] = "cae"                                  #red = Redirect
                return redirect(url_for("cae"))
            elif credentials.query.filter_by(un=a, pas=b, role="cashier").all():
                session["un"] = request.form.get("un")
                session["red"] = "cashier"                              #red = Redirect
                return redirect(url_for("cashier"))
            else:
                session['err'] = 'Username/Password doesn\'t match!'
                return redirect('/')
        else:
            return redirect('/')

@app.route('/logout')                                               #Logout for CAE/Cashier
def logout():
    if "un" or "red" in session:
        session.pop("un", None)
        session.pop("red", None)
        return render_template("login.html", message="Logged out!")
    else:
        return render_template("login.html", message="Already logged out!")

@app.route('/cae')                                                  #Customer Account Executive Home
def cae():
    if "un" in session:
        return render_template("cae.html")
    else:
        return redirect('/')

@app.route('/c_customer', methods=["GET", "POST"])                  #Create Customer by CAE
def create():
    if "red" in session:
        if request.method == "POST":
            a = request.form.get("cname")
            b = request.form.get("cadr")
            c = request.form.get("cage")
            d = request.form.get("cadd")
            e = "Customer Created"
            f = datetime.utcnow()
            temp = customer(cname=a, cadr=b, cage=c, cadd=d, cmsg=e, cdate=f)
            db.session.add(temp)
            db.session.commit()
            return render_template("cae.html", message="Customer Created Successfully...!")
        else:
            return render_template("c_custom.html")
    else:
        return redirect('/')

@app.route('/r_customer', methods=["GET", "POST"])                  #Read/Search Customer by CAE
def read():
    if "red" in session:
        if request.method == "POST" and "by_cid" in request.form:       #Search Customer by Customer ID
            by_cid = request.form.get("by_cid")
            temp = customer.query.filter_by(cid=by_cid).all()
            return render_template("r_custom.html", temp=temp)
        elif request.method == "POST" and "by_cadr" in request.form:    #Search Customer by AADHAR
            by_cadr = request.form.get("by_cadr")
            temp = customer.query.filter_by(cadr=by_cadr).all()
            return render_template("r_custom.html", temp=temp)
        else:
            return render_template("r_custom.html")
    else:
        return redirect('/')

@app.route('/u_customer/<int:cid>', methods=["GET", "POST"])        #Update Customer by CAE
def update(cid):
    if "red" in session:
        temp = customer.query.get(cid)
        if request.method == "POST":
            temp.cname = request.form.get("cname")
            temp.age = request.form.get("cage")
            temp.cadd = request.form.get("cadd")
            temp.cmsg = "Customer Updated"
            temp.cdate = datetime.utcnow()
            db.session.commit()
            return render_template("cae.html", message="Customer Updated Successfully...!")
        else:
            return render_template("u_custom.html", temp=temp)
    else:
        return redirect('/')

@app.route('/d_customer/<int:cid>')                                 #Delete Customer by CAE
def delete(cid):
    if "red" in session:
        temp = customer.query.get(cid)
        db.session.delete(temp)
        db.session.commit()
        return render_template("cae.html", message="Customer Deleted Successfully...!")
    else:
        return redirect('/')

@app.route('/s_customer')                                           #Status of Customers by CAE
def status():
    if "red" in session:
        temp = customer.query.all()
        return render_template("s_custom.html", temp=temp)
    else:
        return redirect('/')

@app.route('/details_customer/<int:cid>')                           #Customer Details by CAE that will allow to Update and Delete Customer
def details(cid):
    if "red" in session:
        temp = customer.query.get(cid)
        return render_template("details_custom.html", temp=temp)
    else:
        return redirect('/')

@app.route('/c_account', methods=["GET", "POST"])                   #Create Account by CAE
def CREATE():
    if "red" in session:
        if request.method == "POST":
            a = request.form.get("ahol")
            b = request.form.get("atyp")
            c = request.form.get("amt")
            d = "Account Created"
            e = datetime.utcnow()
            if customer.query.filter_by(cid=a).all():
                if not account.query.filter_by(ahol=a, atyp=b).all():
                    temp = account(ahol=a, atyp=b, amt=c, amsg=d, adate=e)
                    db.session.add(temp)
                    db.session.commit()
                    return render_template("cae.html", message="Account Created Successfully...!")
                else:
                    return render_template("c_acc.html", message="This Account Exists Already.")
            else:
                return render_template("c_acc.html", message="No Such Customer.")
        else:
            return render_template("c_acc.html")
    else:
        return redirect('/')

@app.route('/r_account', methods=["GET", "POST"])                    #Read/Search Account by CAE
def READ():
    if "red" in session:
        if request.method == "POST" and "by_cid" in request.form:    #Search Account by Customer ID
            by_cid = request.form.get("by_cid")
            temp = account.query.filter_by(ahol=by_cid).all()
            return render_template("r_acc.html", temp=temp)
        elif request.method == "POST" and "by_aid" in request.form:  #Search Account by Account ID
            by_aid = request.form.get("by_aid")
            temp = account.query.filter_by(aid=by_aid).all()
            return render_template("r_acc.html", temp=temp)
        else:
            return render_template("r_acc.html")
    else:
        return redirect('/')

@app.route('/d_account/<int:aid>')                                  #Delete Account by CAE
def DELETE(aid):
    if "red" in session:
        temp = account.query.get(aid)
        db.session.delete(temp)
        db.session.commit()
        return render_template("cae.html", message="Account Deleted Successfully...!")
    else:
        return redirect('/')

@app.route('/s_account')                                            #Status of Account by CAE
def STATUS():
    if "red" in session:
        temp = account.query.all()
        return render_template("s_acc.html", temp=temp)
    else:
        return redirect('/')

@app.route('/details_account/<int:aid>')                            #Account Details by CAE that will allow to Delete Account
def DETAILS(aid):
    if "red" in session:
        temp = account.query.get(aid)
        return render_template("details_acc.html", temp=temp)
    else:
        return redirect('/')

@app.route('/cashier')                                              #Cashier Home
def cashier():
    if "un" in session:
        return render_template("cashier.html")
    else:
        return redirect('/')

@app.route('/cashier/s/account')                                    #Status of Account by Cashier
def status_acc():
    if "red" in session:
        temp = account.query.all()
        return render_template("cashier_s_account.html", temp=temp)
    else:
        return redirect('/')

@app.route('/cashier/r/account', methods=["GET", "POST"])           #Search Account by Cashier
def read_acc():
    if "red" in session:
        if request.method == "POST" and "by_cid" in request.form:       #Search Account by Customer ID
            by_cid = request.form.get("by_cid")
            temp = account.query.filter_by(ahol=by_cid).all()
            return render_template("cashier_r_account.html", temp=temp)
        elif request.method == "POST" and "by_aid" in request.form:     #Search Account by Account ID
            by_aid = request.form.get("by_aid")
            temp = account.query.filter_by(aid=by_aid).all()
            return render_template("cashier_r_account.html", temp=temp)
        else:
            return render_template("cashier_r_account.html")
    else:
        return redirect('/')

@app.route('/cashier/details_account/<int:aid>')                    #Account Details to Manage (D/W/T)
def acc_details(aid):
    if "red" in session:
        temp = account.query.get(aid)
        return render_template("cashier_details_acc.html", temp=temp)
    else:
        return redirect('/')

@app.route('/cashier/deposit/account/<int:aid>')                    #Deposit
def deposit_acc(aid):
    if "red" in session:
        temp = account.query.get(aid)
        return render_template("cashier_deposit_acc.html", temp=temp)
    else:
        return redirect('/')

@app.route('/cashier/deposit/<int:aid>', methods=['GET', 'POST'])   #Deposit
def deposit(aid):
    if "red" in session:
        temp = account.query.get(aid)
        if request.method == "POST":
            temp.amt += int(request.form.get("depositAmt"))
            temp.amsg = "Amount deposited"
            temp.adate = datetime.utcnow()
            db.session.add(transaction(tacc=aid, tmsg="Deposit", tamt=temp.amt))
            db.session.commit()
            return render_template("cashier_details_acc.html", temp=temp, message="Amount deposited successfully")
    else:
        return redirect('/')

@app.route('/cashier/withdraw/account/<int:aid>')                   #Withdraw
def withdraw_acc(aid):
    if "red" in session:
        temp = account.query.get(aid)
        return render_template("cashier_withdraw_acc.html", temp=temp)
    else:
        return redirect('/')

@app.route('/cashier/withdraw/<int:aid>', methods=['GET', 'POST'])  #Withdraw
def withdraw(aid):
    if "red" in session:
        temp = account.query.get(aid)
        if request.method == "POST":
            if int(request.form.get("withdrawAmt")) > temp.amt:
                return render_template("cashier_details_acc.html", temp=temp, message="Withdraw not allowed, please choose smaller amount")
            temp.amt -= int(request.form.get("withdrawAmt"))
            temp.amsg = "Amount withdrawn"
            temp.adate = datetime.utcnow()
            db.session.add(transaction(tacc=aid, tmsg="Withdraw", tamt=temp.amt))
            db.session.commit()
            return render_template("cashier_details_acc.html", temp=temp, message="Amount withdrawn successfully")
    else:
        return redirect('/')

@app.route('/cashier/transfer/account/<int:aid>')                   #Transfer
def transfer_acc(aid):
    accounts = account.query.get(aid)
    cid = accounts.ahol
    cust_accounts = db.session.query(account).filter(account.ahol == cid).count()
    if cust_accounts > 1:
        cust_accounts = db.session.query(account).filter(account.ahol == cid).all()
        balances = []
        for i in cust_accounts:
            acc = (i.atyp, i.amt)
            balances.append(acc)
        return render_template('cashier_transfer_acc.html', temp=accounts, cid=cid, customers=cust_accounts, balances=balances)
    else:
        return render_template('cashier_details_acc.html', temp=accounts, role=True, error=True, message='You don\'t have enough accounts to transfer!')

@app.route('/cashier/transfer/<int:aid>', methods=['GET', 'POST'])  #Transfer
def transfer(aid):
    accounts = account.query.get(aid)
    if request.method == "POST":
        sourceAccType = request.form['sourceAcc']
        targetAccType = request.form['targetAcc']
        sourceAcc = db.session.query(account).filter(account.atyp == sourceAccType, account.ahol == accounts.ahol).first()
        targetAcc = db.session.query(account).filter(account.atyp == targetAccType, account.ahol == accounts.ahol).first()
        if int(request.form.get("transferAmt")) > sourceAcc.amt:
            return render_template("cashier_details_acc.html", role=True, error=True, temp=accounts, message="Transfer not allowed, please choose smaller amount")
        sourceAcc.amt -= int(request.form.get("transferAmt"))
        targetAcc.amt += int(request.form.get("transferAmt"))
        accounts.amsg = "Amount Transferred"
        accounts.adate = datetime.utcnow()
        db.session.add(transaction(tacc=aid, tmsg="Transferred", tamt=sourceAcc.amt))
        db.session.commit()
        return render_template("cashier_details_acc.html", role=True, temp=accounts, message="Amount transferred successfully")
    else:
        return render_template("cashier_transfer_acc.html", temp=accounts)

@app.route('/cashier/statement', methods=['GET', 'POST'])
def statement():
    if "red" in session:
        if request.method == "POST":
            aid = request.form.get("tacc")
            selectedRadio = request.form.get('selection')
            if(request.form.get('numTrans')):
                numberOfTranscation = request.form.get('numTrans')
                temp = db.session.query(transaction).filter(transaction.tacc == aid)[:5]
                # temp = transaction.query.filter_by(tacc=aid)[:3].all()
                return render_template("cashier_statement.html", temp=temp)
            if(request.form.get('fromDate')):
                print(request.form.get('fromDate'), request.form.get('toDate'))
                if(request.form.get('fromDate') > request.form.get('toDate')):
                    return render_template("cashier_statement.html", err=True, msg='Invalid Dates!')
            # return render_template("cashier_statement.html", temp=temp)
        else:
            return render_template("cashier_statement.html")
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run()


#In routes: c_:create, r_:Read/Search, u_:Update, d_:delete, s_:status
#Staus gives list of all Customers/Accounts
#Details gives individual page, that can redirect to update and delete