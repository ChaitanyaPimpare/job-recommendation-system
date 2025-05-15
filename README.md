<<<<<<< HEAD
# job-recommendation-system
=======
# Job Recommendation System

This is a **Job Recommendation System** that suggests jobs based on user skills using **Machine Learning**. It is built with **Flask, SQLite, and Scikit-Learn**.
A Machine Learning-based web application that recommends jobs to users based on their skills.Built with 
Flask,SQLite, and Scikit-Learn, this system leverages data to provide personalized job suggestions. It is deployed on 
Render for easy access.
LiveLink:https://job-recommendation-system-n7wq.onrender.com

##  Features
- User authentication (Register, Login, Logout)
- Job recommendation using **cosine similarity**
- Secure password storage with hashing
- Web-based UI using Flask templates
- Job dataset stored as a pickle file (`job_data.pkl`)

## 🛠 Technologies Used
- **Python** (Flask, Scikit-Learn, Pandas)
- **SQLite** (Database for authentication)
- **HTML, CSS** (Frontend)
- **Pickle** (For storing ML models)
- **Git & GitHub** (Version control)

##  Installation Guide

### 1️⃣ Clone the Repository

git clone https://github.com/ChaitanyaPimpare/job-recommendation-system.git
cd job-recommendation
```sh
2️⃣ Create & Activate Virtual Environment

python -m venv venv  # Create virtual environment

source venv/bin/activate  # Activate on Mac/Linux

venv\Scripts\activate  # Activate on Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up the Database

python create_db.py

#Train the model
 python train.py

5️⃣ Run the Application
python app.py

Now, open your browser and go to http://127.0.0.1:5000/.
