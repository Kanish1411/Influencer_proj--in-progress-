from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask import Flask, make_response, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_current_user
from werkzeug.security import generate_password_hash,check_password_hash
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:/MAD/Proj1/backend/Database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'qwertyuiop' 
db = SQLAlchemy(app)
CORS(app)
jwt = JWTManager(app)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(10), nullable=False)
    pwd=db.Column(db.String(20),nullable=False)
    approved=db.Column(db.Boolean,default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    def has_role(self, role):
        user_role = Role.query.filter_by(id=self.role_id).first()
        return user_role is not None and user_role.name == role

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    budget=db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(10), nullable=False)
    details = db.Column(db.String(50))
    sp_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camp_id=db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    name = db.Column(db.String(10), nullable=False)
    req = db.Column(db.String(50))
    price=db.Column(db.Integer,nullable=False)

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sp_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    inf_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ad_id=db.Column(db.Integer, db.ForeignKey('ad.id'), nullable=False)
    state = db.Column(db.String(10), nullable=False)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    req_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    req_from_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    camp_id=db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    ad_id=db.Column(db.Integer, db.ForeignKey('ad.id'), nullable=False)
    accepted=db.Column(db.Boolean, nullable=False)

class Additional(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating=db.Column(db.Integer, nullable=False)
    platform=db.Column(db.String(10), nullable=False)

# Decorator to check user roles
def auth_role(role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()
            current_user = db.session.get(User, user_id)
            roles = role if isinstance(role, list) else [role]
            if not current_user:
                return make_response({"msg": "User not found"}, 404)
            if all(not current_user.has_role(r) for r in roles):
                return make_response({"msg": "missing roles"}, 403)
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    users=User.query.filter_by(name=username).all()
    for u in users:
        if u.name == username and check_password_hash(u.pwd,password):
            if u.role_id==1:
                access_token = create_access_token(identity=u.id, additional_claims={"role": "admin"})
                return jsonify({'message': 'Admin login successful', 'access_token': access_token}), 200
            elif u.role_id == 2:
                    if u.approved:
                        access_token = create_access_token(identity=u.id, additional_claims={"role": "Sponsor"})
                        return jsonify({'message': 'Sponsor login successful', 'access_token': access_token,"id":u.id}), 200
                    else:
                        return jsonify({'message': 'Please Wait for Admin Approval'}),200
            elif u.role_id==3:
               access_token = create_access_token(identity=u.id, additional_claims={"role": "Influencer"})
               return jsonify({'message': 'Influencer login successful', 'access_token': access_token,"id":u.id}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    em = data.get('email')
    additional= data.get('addon')
    r=data.get('role')
    users=User.query.filter_by(role_id=Role.query.filter_by(name=r).first().id).all()
    if users and any(u.name == username for u in users):
        return jsonify({'error': 'Username already exists'}), 400
    if users and any(u.email == em for u in users):
        return jsonify({'error': 'Email already exists'}), 400
    if r=="Influencer":
        u=User(email=em,pwd=generate_password_hash(password),name=username,role_id=3)
        db.session.add(u)
        db.session.commit()
        inf=Additional(user_id=u.id,rating=5,platform=additional)
        db.session.add(inf)
        db.session.commit()
    if r=="Sponsor":
        u=User(email=em,pwd=generate_password_hash(password),name=username,role_id=2,approved=False)
        spn=Additional(user_id=u.id,rating=5,platform=additional)
        db.session.add(spn)
        db.session.add(u)
        db.session.commit()
        return jsonify({'message': 'Registration successful Wait for Admin Approval'}), 200
    return jsonify({'message': 'Registration successful'}), 200

@app.route("/admin",methods=["GET"])
@auth_role("Admin")
def admin():
    camp=[]
    u=Campaign.query.all()
    for i in u:
        add=[]
        a=Ad.query.filter_by(camp_id=i.id).all()
        for j in a:
            var="Unassigned"
            w=Work.query.filter_by(ad_id=j.id).first()
            if w:
                inf=w.inf_id
                var=User.query.filter_by(id=inf).first().name
            add.append({"Ad_id":j.id,"Name":j.name,"Req":j.req,"Worker":var})
        camp.append({"camp_id":i.id,"Camp_name":i.name,"Camp_vis":i.status,"ads":add})
    return {"camp":camp}

@app.route('/check_login', methods=['GET'])
@jwt_required()
def check_login():
    print("login works fine here")
    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    u=User.query.filter_by(id=get_jwt_identity()).all()
    for i in u:
        if i.role_id in [3,2,1]:
            return {"message":"success"}
    return {"message" : "Fail"}

@app.route("/check_inf", methods=["GET"])
@jwt_required()
def check_inf():
    print("inf works fine here")
    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    u=User.query.filter_by(id=get_jwt_identity()).all()
    for i in u:
        if i.role_id ==3:
            return {"message":"success"}
    return {"message" : "Fail"}

@app.route("/check_spn", methods=["GET"])
@jwt_required()
def check_spn(): 
    print("spn works fine here")
    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    u=User.query.filter_by(id=get_jwt_identity()).all()
    for i in u:
        if i.role_id ==2:
            return {"message":"success"}
    return {"message" : "Fail"}

@app.route("/check_ad", methods=["GET"])
@jwt_required()
def check_ad():
    print("ad works fine here")
    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    u=User.query.filter_by(id=get_jwt_identity()).all()
    for i in u:
        if i.role_id ==1:
            return {"message":"success"}
    return {"message" : "Fail"}

@app.route("/Influencer", methods=['GET','POST'])
@auth_role("Influencer")
def Influencer():
    v=request.get_json()
    id=v.get("id")
    active=[]
    u=Work.query.filter_by(inf_id=id).all()
    for i in u:
        a=Ad.query.filter_by(id=i.ad_id).first()
        if i.state!= "Finished":
            active.append({"Campaign_id":a.camp_id,"Sponser":i.sp_id,"ad_name":a.name})
    req=[]
    r=Request.query.filter_by(req_id=id).all()
    for i in r:
        if i.accepted==False:
            a=Ad.query.filter_by(id=i.ad_id).first()
            c=Campaign.query.filter_by(id=a.camp_id).first()
            req.append({"id":i.id,"name":a.name,"req":a.req,"camp":c.name})
        print(active,req)
    return {"camp":active,"req":req}

@app.route("/Sponsor", methods=["GET",'POST'])
@auth_role("Sponsor")
def Sponsor():
    v=request.get_json()
    id=v.get("id")
    camp=[]
    add=[]
    u=Campaign.query.filter_by(sp_id=id).all()
    for i in u:
        a=Ad.query.filter_by(camp_id=i.id).all()
        for j in a:
            var="Unassigned"
            w=Work.query.filter_by(ad_id=j.id).first()
            if w:
                inf=w.inf_id
                var=User.query.filter_by(id=inf).first().name
            add.append({"Ad_id":j.id,"Name":j.name,"Req":j.req,"Worker":var})
        camp.append({"camp_id":i.id,"Camp_name":i.name,"Camp_vis":i.status,"ads":add})
        add
    req=[]
    r=Request.query.filter_by(req_id=id).all()
    for i in r:
        if i.accepted==False:
            a=Ad.query.filter_by(id=i.ad_id).first()
            req.append({"req_id":i.id,"ad_name":a.name})
    print(camp,req)
    return {"camp":camp,"req":req}

@app.route("/Sponsor_req",methods=["GET"])
@auth_role("Sponsor")
def sponsor_req():
    u=User.query.filter_by(approved=False).all()
    l=[]
    for i in u:
        l.append({"id":i.id,"name":i.name})
    return l

@app.route("/accept",methods=["POST"])
def Accept():
    v=request.get_json()
    u=User.query.filter_by(id=v.get("id")).first()
    u.approved=True
    db.session.commit()
    return {"message":"success"}

@app.route("/add_camp",methods=["GET","POST"]) 
@auth_role("Sponsor")
def add_camp():
    v=request.get_json()
    c=Campaign(name=v.get("camp_name"),budget=v.get("camp_bud"),
               status=v.get("camp_vis"),details=v.get("camp_det"),
               sp_id=v.get("sp_id"))
    db.session.add(c)
    db.session.commit()
    return {"message":"success"}

@app.route("/update_camp",methods=["GET","POST"])
@auth_role("Sponsor")
def Update_camp():
    v=request.get_json()
    c=Campaign.query.filter_by(id=v.get("id")).first()
    if c:
        c.name=v.get("camp_name")
        c.budget=v.get("camp_bud")
        c.status=v.get("camp_vis")
        c.details=v.get("camp_det")
        db.session.commit()
        return {"message":"success"}
    return {"message":"Failed"}

@app.route("/delete_camp",methods=['GET','POST'])
@auth_role("Sponsor")
def delete_camp():
    v = request.get_json()
    c=Campaign.query.filter_by(id=v.get("id")).first()
    ad=Ad.query.filter_by(camp_id=c.id).all()
    for i in ad:
        db.session.delete(i)
    db.session.delete(c)
    db.session.commit()
    return {"message":"success"}

@app.route("/add_ad",methods=["GET","POST"]) 
@auth_role("Sponsor")
def add_ad():
    v=request.get_json()
    a=Ad(name=v.get("ad_name"),price=v.get("ad_bud"),
              req=v.get("ad_req"),camp_id=v.get("id"))
    db.session.add(a)
    db.session.commit()
    return {"message":"success"}

@app.route("/update_ad",methods=["GET","POST"]) 
@auth_role("Sponsor")
def Update_ad():
    v=request.get_json()
    a=Ad.query.filter_by(id=v.get("id")).first()
    print(a)
    if a:
        a.name=v.get("ad_name")
        a.price=v.get("ad_bud")
        a.req=v.get("ad_req")
        db.session.commit()
        return {"message":"success"}
    return {"message":"Failed"}

@app.route("/delete_ad",methods=['GET','POST'])
@auth_role("Sponsor")
def delete_ad():
    v = request.get_json()
    a=Ad.query.filter_by(id=v.get("id")).first()
    db.session.delete(a)
    db.session.commit()
    return {"message":"success"}

##
##
## Searching feature 
@app.route("/find_inf",methods=['GET','POST'])
@auth_role("Sponsor")
def Find_inf():
    v = request.get_json()
    key=v.get("keyword")
    print(key)
    inf=0
    if key=="" or key==None:
        inf=User.query.filter_by(role_id=3).all()
    else:
        # if "rating" in key:
        inf=User.query.filter_by(role_id=3,name=key).all()
    l=[]
    for i in inf:
        inf_add=Additional.query.filter_by(inf_id=i.id).first()
        l.append({"name":i.name,"Rating":inf_add.rating,"platform":inf_add.platform,"id":i.id})
    return {"inf":l}

@app.route("/inf_details", methods=["GET"])
def inf_fetch():
    user_id = request.args.get('id')
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({"name": user.name,"email": user.email})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/camp_fetch", methods=["GET"])
def camp_fetch():
    user_id = request.args.get('id')
    camp = Campaign.query.filter_by(sp_id=user_id).all()
    print(camp)
    l=[]
    if camp:
        for i in camp:
            l.append({"name": i.name,"id": i.id,})
    else:
        return jsonify({"error": "User not found"}), 404
    return jsonify(l)

@app.route("/ad_fetch", methods=["GET"])
def ads_fetch():
    id = request.args.get('id')
    ad = Ad.query.filter_by(camp_id=id).all()
    l=[]
    if ad:
        for i in ad:
                v=Request.query.filter_by(ad_id=i.id,camp_id=id).first()
                if v==None:
                    l.append({"name": i.name,"id": i.id})
                elif v.accepted==False:
                    l.append({"name": i.name,"id": i.id,"inf_id":v.req_id})     
    else:
        return jsonify({"error": "User not found"}), 404
    return jsonify(l)

@app.route("/request_inf",methods=["POST"])
def request_inf():
    v=request.get_json()
    inf_id=int(v.get("inf_id"))
    camp_id=v.get("camp_id")
    ad_id=v.get("ad_id")
    sp_id=v.get("ad_id")
    r1=None
    if(ad_id==None or camp_id==None):
        return jsonify({"message":"Fields not selected"})
    if(ad_id !=None):
        r1=Request.query.filter_by(ad_id=ad_id,camp_id=camp_id).first()
    if(r1!=None and r1.accepted==True):
        r=Request(req_id=inf_id,req_from_id=sp_id,camp_id=camp_id,ad_id=ad_id,accepted=False)
        db.session.add(r)
        db.session.commit()
        return jsonify({"message":"success"})
    elif(r1==None):
        r=Request(req_id=inf_id,camp_id=camp_id,req_from_id=sp_id,ad_id=ad_id,accepted=False)
        db.session.add(r)
        db.session.commit()
        return jsonify({"message":"success"})
    return jsonify({"message":"Failed"})

@app.route("/accept_req",methods=["POST"])
def accept_req():
    v=request.get_json()
    id=v.get("id")
    print(id)
    r=Request.query.filter_by(id=id).first()
    r.accepted=True
    c=Campaign.query.filter_by(id=r.camp_id).first()
    w=Work(sp_id=c.sp_id,inf_id=r.req_id,ad_id=r.ad_id,state="Accepted")
    db.session.add(w)
    db.session.commit()
    return jsonify({"msg":"success"})

@app.route("/reject_req",methods=["POST"])
def reject_req():
    v=request.get_json()
    id=v.get("id")
    r=Request.query.filter_by(id=id).first()
    if r:
        db.session.delete(r)
    db.session.commit()
    return jsonify({"msg":"success"}) 

@app.route("/find_spn", methods=["POST"])
@auth_role("Influencer")
def sp_fetch():
    v=request.get_json()
    idu=v.get("id")
    key=v.get("keyword")
    camp=[]
    if key!="" or key!=None:
        key = f"%{key}%"
        camp=Campaign.query.filter_by(name=key).all()
    else:
        camp=Campaign.query.all()
    l=[]
    for i in camp:
        ad=Ad.query.filter(Campaign.name.like(key)).all()
        if ad:
            for j in ad:
                w=Work.query.filter_by(ad_id=j.id).first()
                r=Request.query.filter_by(ad_id=j.id,req_from_id=idu).first()
                add=Additional.query.filter_by(user_id=i.id).first()
                if r or w:
                    continue
                if w==None and  i.status=="public":
                    l.append({"id":j.id,"ad_name":j.name,"camp_name":i.name,"task":j.req,"price":j.price,"rating":add.rating})
    return jsonify(l)

@app.route("/request_ad",methods=["POST"])
def request_ad():
    v=request.get_json()
    aid=v.get("id")
    idu=v.get("idu")
    camp=Campaign.query.filter_by(id=(Ad.query.filter_by(id=aid).first().camp_id)).first()
    r1=Request.query.filter_by(ad_id=aid,req_from_id=idu).first()
    if r1:
        return jsonify("error")
    r=Request(req_id=camp.sp_id,req_from_id=idu,camp_id=camp.id,ad_id=aid,accepted=False)
    db.session.add(r)
    db.session.commit()
    return jsonify("Success")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if Role.query.first() is None:
            db.session.add(Role(name='Admin'))
            db.session.add(Role(name='Sponsor'))
            db.session.add(Role(name='Influencer'))
            db.session.add(User(name="admin",email="admin@123",pwd=generate_password_hash("pass"),role_id=1))
            db.session.commit()
    app.run(debug=True)