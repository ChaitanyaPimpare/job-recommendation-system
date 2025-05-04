import os
import pickle
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.metrics.pairwise import cosine_similarity
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'username@gmail.com'     
app.config['MAIL_PASSWORD'] = 'apppassword'        
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    job_id = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This email is already registered. Please login or use another email.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

       
        try:
            msg = Message(
                subject="Welcome to Job Recommendation System",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email],
                body=f"Hello {username},\n\nWelcome to our platform! We're excited to have you onboard.\n\nBest Regards,\nJob Portal Team"
            )
            mail.send(msg)
            flash('Account created successfully! A welcome email has been sent.', 'success')
        except Exception as e:
            print(f"Email sending failed: {e}")
            flash('Account created successfully! (Email could not be sent)', 'warning')

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('recommend_jobs'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend_jobs():
    if request.method == 'POST':
        user_skills = request.form.get('skills', '').strip()
        
        if not user_skills:
            return render_template('index.html', error='No skills provided')
        
        
        vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
        job_vectors = pickle.load(open('job_vectors.pkl', 'rb'))
        job_data = pickle.load(open('job_data.pkl', 'rb'))
        
        user_vector = vectorizer.transform([user_skills])
        similarities = cosine_similarity(user_vector, job_vectors)
        recommended_indices = similarities.argsort()[0][-15:][::-1]
        
        recommendations = job_data.iloc[recommended_indices][['job_id', 'title','company','salary','description']].to_dict(orient='records')
        return render_template('recommendations.html', recommendations=recommendations)
    
    return render_template('index.html')

@app.route('/jobs', methods=['GET', 'POST'])
def job_listings():
    job_data = pickle.load(open('job_data.pkl', 'rb'))
    jobs = job_data[['job_id', 'title', 'company', 'salary', 'description']]

    if request.method == 'POST':
        search_input = request.form.get('search_query', '').strip().lower()

        if not search_input:
            return render_template('jobs.html', jobs=jobs.to_dict(orient='records'))

        # Load vectorizer and job vectors trained on combined data
        vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
        job_vectors = pickle.load(open('job_vectors.pkl', 'rb'))

        # Transform user input into vector
        input_vector = vectorizer.transform([search_input])
        similarities = cosine_similarity(input_vector, job_vectors)
        top_indices = similarities.argsort()[0][-15:][::-1]

        filtered_jobs = jobs.iloc[top_indices].to_dict(orient='records')
        return render_template('jobs.html', jobs=filtered_jobs)

    return render_template('index.html', jobs=jobs.to_dict(orient='records'))

@app.route('/job')
def job_list():  
    job_data = pickle.load(open('job_data.pkl', 'rb'))
    jobs = job_data[['job_id', 'title','company','salary', 'description']].to_dict(orient='records')
    return render_template('jobs.html', jobs=jobs) 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/apply', methods=['POST'])
@login_required
def apply_job():
    job_id = request.form.get('job_id')
    application = JobApplication(user_id=current_user.id, job_id=job_id)
    db.session.add(application)
    db.session.commit()
    flash("You have successfully applied for the job!", "success")
    return render_template('recommendations.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.after_request
def add_cache_control_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  

    port = int(os.environ.get("PORT", 8080)) 
    app.run(host="0.0.0.0", port=port, debug=True)