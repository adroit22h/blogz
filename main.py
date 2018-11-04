from flask import Flask,request,redirect,render_template, session
from flask_sqlalchemy import SQLAlchemy
from server.validate.validate import validation

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:happy@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)



class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(120))
    Body = db.Column(db.Text())
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self, title,body, user):
        self.Title = title
        self.Body = body
        self.user_id=user
        self.owner

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.Text())
    blogs = db.relationship('Blog', backref='owner', lazy=False)

    def __init__(self, username,password):
        self.username = username
        self.password = password
    
    def checkIfUserExist(self):
        self = (self.query.filter_by(username=self.username,password=self.password)).first()
        return self

    
    def setSession(self):
        session['user']=self.id
        print ('The session is', session['user'])

   
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','index']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')    
    

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        user=1
        new_post = Blog(title,body,user)
        db.session.add(new_post)
        db.session.commit()
    

    post = Blog.query.all()
    users= User.query.all()



    return render_template('index.html', posts=post,users=users)

@app.route('/newpost',methods=['POST','GET'])
def newpost():
    
    title=''
    body=''
    errors=[]

    

    if request.method=='POST':
        if validation(request)==True:
            title=request.form['title']
            body=request.form['body']
            user=session['user']
            new_post = Blog(title,body,user)
            db.session.add(new_post)
            db.session.commit()
            postId=(new_post.id)
            return redirect(f'/post?postId={postId}')
        else:
            return render_template('newpost.html',errors=validation(request),title=title,body=body)
    
    
    return render_template('newpost.html',  errors=[], title=title,body=body)

@app.route('/blog',methods=['POST','GET'])
def blog():

   
    if 'user' in request.args :
        posts= Blog.query.filter_by(user_id=request.args.get('user'))
        print('user',posts)
    elif 'post' in request.args:
        posts= Blog.query.filter_by(id=request.args.get('post'))
        print('post',posts)
    else:
        posts = Blog.query.all()
        print('*****none*********',posts)

        

    return render_template('blog.html', posts=posts)



@app.route('/post',methods=['GET'])
def post():
    postId=request.args.get('postId')
    post=Blog.query.filter_by(id=postId).first()
    return render_template('post.html',post=post)    


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        AttemptingUser= User(request.form['username'],request.form['password']).checkIfUserExist()
        
        if AttemptingUser is not None:
            AttemptingUser.setSession()
            return redirect('/newpost')
        else:
            return render_template('login.html',failed=True)

    return render_template('login.html')    
 
    
@app.route('/signup', methods=['GET','POST'])
def signup():
    

    if (request.method =='GET'):
         return render_template('signup.html',validate=[])
    if (request.method)=='POST':
        AttemptingUser= User.query.filter_by(username=request.form['username']).first()
        UserExist= (AttemptingUser) is not None
        validate=validation(request)
        print(validate)
        if validate==True and UserExist is False:
            
            newUser=User(request.form['username'],request.form['password'])
            db.session.add(newUser)
            db.session.commit()
            newUser.setSession()

            print(session)

            return render_template('/newpost.html',errors=[],username=request.form['username'])
        else:
            if  UserExist  is True:
                if type(validate) is dict:
                    validate['userExist']=True
                else:
                    validate={'userExist':True}
                
            return render_template('/signup.html',validate=validate,username=request.form['username'])
        

    
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect('/blog')   

    


if __name__=="__main__":
    app.run()