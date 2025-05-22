from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField, EmailField
from wtforms.validators import InputRequired, Length , ValidationError, Email
from flask_bcrypt import Bcrypt



app= Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True
app.jinja_env.auto_reload =True

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
app.config['SECRET_KEY']= 'dev'

bcrypt = Bcrypt(app)
db =SQLAlchemy(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ="login"


class User (db.Model, UserMixin):
    id = db.Column (db.Integer, primary_key=True )
    username = db.Column(db.String(20), nullable =False, unique=True )
    email= db.Column (db.String(200), nullable =False ,unique=True)
    password = db.Column (db.String , nullable = False)

    def __repr__(self):
        return f'User({self.username}, {self.email})'
    

class blogpost(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column (db.String(100), nullable =False)
    author = db.Column(db.String)
    time = db.Column(db.DateTime)
    niche= db.Column(db.String())
    content = db.Column(db.Text)

class RegisterForm(FlaskForm):
    username = StringField (validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    email= EmailField(validators=[InputRequired(),Email(message='Invalid Email address')], render_kw={"placeholder":"Email"})
    password = PasswordField(validators=[InputRequired(),Length(min=4, max =20)], render_kw={"placeholder":"Password"})
    submit= SubmitField('Register')

    def validate_username(self, username):
        existing_User_username = User.query.filter_by(username=username.data).first()

        if existing_User_username:
            raise ValidationError("This username exists, choose a different one")
        
    def validate_email (self, email):
        existing_email =  User.query.filter_by(email=email.data).first()

        if existing_email:
            raise ValidationError("This email esxists, choose a differnet one")


class LoginForm(FlaskForm):
    #username = StringField (validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    email= EmailField(validators=[InputRequired(),Email(message='Invalid Email address')], render_kw={"placeholder":"Email"})
    password = PasswordField(validators=[InputRequired(),Length(min=4, max =20)], render_kw={"placeholder":"Password"})
    submit= SubmitField('Login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
def home():
    return render_template ('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user=User(username = form.username.data, email= form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect (url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email =form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template ('login.html', form =form)




@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug =True )


