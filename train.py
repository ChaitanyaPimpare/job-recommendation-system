import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Sample job dataset
job_data = pd.DataFrame({
    'job_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'title': [ 'Software Engineer', 'Data Scientist', 'Web Developer', 'AI Engineer', 'Backend Developer',
        'Cybersecurity Analyst', 'Cloud Engineer', 'DevOps Engineer', 'Mobile App Developer', 'UI/UX Designer'],
    'description': [
        'Python, Java, SQL, Cloud Computing, Algorithms, Data Structures',
        'Machine Learning, Python, Deep Learning, Data Analysis, R, Statistics, NLP',
        'HTML, CSS, JavaScript, React, Node.js, Vue.js, Frontend Development',
        'Artificial Intelligence, Neural Networks, TensorFlow, NLP, PyTorch, Computer Vision',
        'Java, Spring Boot, Microservices, SQL, REST API, System Design',
        'Cybersecurity, Ethical Hacking, Network Security, Encryption, Penetration Testing',
        'AWS, Azure, Google Cloud, Kubernetes, Docker, Cloud Security',
        'DevOps, CI/CD, Jenkins, Git, Linux, Automation, Kubernetes',
        'Android, iOS, Flutter, React Native, Swift, Kotlin, Mobile UI/UX',
        'Wireframing, Prototyping, Figma, Adobe XD, User Research, UX Design'
    ]
})

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
job_vectors = vectorizer.fit_transform(job_data['description'])

# Save the trained model
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))
pickle.dump(job_vectors, open('job_vectors.pkl', 'wb'))
pickle.dump(job_data, open('job_data.pkl', 'wb'))

print("✅ Job Recommendation Model Trained and Saved Successfully!")
