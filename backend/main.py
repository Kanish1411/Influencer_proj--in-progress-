
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

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    budget=db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(10), nullable=False)
    details = db.Column(db.String(50))

class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camp_id=db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    name = db.Column(db.String(10), nullable=False)
    details = db.Column(db.String(50))
    price=db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(10), nullable=False)

class work(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sp_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    inf_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ad_id=db.Column(db.Integer, db.ForeignKey('ad.id'), nullable=False)
    state = db.Column(db.String(10), nullable=False)


# Decorator to check user roles
def auth_role(role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            current_user = User.query.get(get_jwt_identity())
            roles = role if isinstance(role, list) else [role]
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
    print(username)
    users=User.query.filter_by(name=username).all()
    print(users)
    for u in users:
        if u.name == username and check_password_hash(u.pwd,password):
            if u.role_id==1:
                access_token = create_access_token(identity=username, additional_claims={"role": "admin"})
                return jsonify({'message': 'Admin login successful', 'access_token': access_token}), 200
            elif u.role_id == 2:
                    if u.approved:
                        access_token = create_access_token(identity=username, additional_claims={"role": "Sponsor"})
                        return jsonify({'message': 'Sponsor login successful', 'access_token': access_token,"id":u.id}), 200
                    else:
                        return jsonify({'message': 'Please Wait for Admin Approval'}),200
            elif u.role_id==3:
               access_token = create_access_token(identity=username, additional_claims={"role": "Influencer"})
               return jsonify({'message': 'Influencer login successful', 'access_token': access_token,"id":u.id}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# @app.route('/inf_register', methods=['POST'])
# def Influencer_register():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#     em = data.get('email')
#     p=data.get('platform')
#     users=User.query.filter_by(rid=Role.query.filter_by(name="Influencer").first().id)
#     if any(u.name == username for u in users):
#         return jsonify({'error': 'Username already exists'}), 400
#     if any(u.email == em for u in users):
#         return jsonify({'error': 'Email already exists'}), 400
#     u=User(email=em,password=generate_password_hash(password),name=username,role_id=3)
#     db.session.add(u)
#     db.session.commit()
#     return jsonify({'message': 'Registration successful'}), 200
# @app.route('/spn_register', methods=['POST'])
# def sponser_register():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#     em = data.get('email')
#     i=data.get('industry')
#     users=User.query.filter_by(rid=Role.query.filter_by(name="Sponsor").first().id)
#     if any(u.name == username for u in users):
#         return jsonify({'error': 'Username already exists'}), 400
#     if any(u.email == em for u in users):
#         return jsonify({'error': 'Email already exists'}), 400
  
#     u=User(email=em,password=generate_password_hash(password),name=username,role_id=2,approved=False)
#     db.session.add(u)
#     db.session.commit()
#     return jsonify({'message': 'Registration successful'}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    em = data.get('email')
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
    if r=="Sponsor":
        u=User(email=em,pwd=generate_password_hash(password),name=username,role_id=2,approved=False)
        db.session.add(u)
        db.session.commit()
        return jsonify({'message': 'Registration successful Wait for Admin Approval'}), 200
    return jsonify({'message': 'Registration successful'}), 200


@app.route('/check_login', methods=['GET'])
@jwt_required()
def check_login():
    print("login works fine here")
    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    u=User.query.filter_by(name=get_jwt_identity()).all()
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
    u=User.query.filter_by(name=get_jwt_identity()).all()
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
    u=User.query.filter_by(name=get_jwt_identity()).all()
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
    u=User.query.filter_by(name=get_jwt_identity()).all()
    for i in u:
        if i.role_id ==1:
            return {"message":"success"}
    return {"message" : "Fail"}

@app.route("/Influencer", methods=["GET",'POST'])
def  Influencer():
    v=request.get_json()
    print(v)
    
    cl=[]

    return {"camp":cl}

@app.route("/Sponsor", methods=["GET",'POST'])
@jwt_required()
def Sponsor():
    v=request.get_json()
    if v=={}:
        camp=Campaign.query.filter_by(status="Public").all()
    # else:
    #     c=Category.query.filter_by(name=v['key']).all()
    #     if c==[]:
    #         it=Item.query.filter_by(name=v['key']).all()
    #         for j in it:
    #             c.append(Category.query.filter_by(id=j.cat_id).first())
    #     else:
    #         for i in c:
    #             it.extend(Item.query.filter_by(cat_id=i.id).all())
    cl=[]
    for i in camp:
        cl.append({"id":i.id,"name":i.name})
    return {"camp":cl}

@app.route("/Sponsor_req",methods=["GET"])
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
