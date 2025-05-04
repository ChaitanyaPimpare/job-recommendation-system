import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Sample job dataset
job_data = pd.DataFrame({
    'job_id': list(range(1, 16)),
    'title': ['Software Engineer', 'Data Scientist', 'Web Developer', 'AI Engineer', 'Backend Developer',
              'Cybersecurity Analyst', 'Cloud Engineer', 'DevOps Engineer', 'Mobile App Developer', 'UI/UX Designer',
              'Full Stack Developer', 'Blockchain Developer', 'Database Administrator', 'System Administrator', 'Game Developer'],
    'company': ['Google', 'Microsoft', 'Amazon', 'Tesla', 'Facebook', 
                'IBM', 'Oracle', 'Adobe', 'Netflix', 'Spotify', 
                'Twitter', 'Coinbase', 'Salesforce', 'Cisco', 'EA Games'],
    'description': [
        'Python, Java, SQL, Cloud Computing, Data Structures, Algorithms, Git, Agile, REST APIs',
        'Machine Learning, Python, Deep Learning, Data Analysis, R, Statistics, NLP, Big Data, TensorFlow',
        'HTML, CSS, JavaScript, React, Node.js, Vue.js, Frontend Development, Bootstrap, UX principles',
        'Artificial Intelligence, Neural Networks, TensorFlow, NLP, PyTorch, Computer Vision, Reinforcement Learning',
        'Java, Spring Boot, Microservices, SQL, REST API, System Design, Scalability, Docker, Kubernetes',
        'Cybersecurity, Ethical Hacking, Network Security, Encryption, Risk Assessment, Penetration Testing, Compliance',
        'AWS, Azure, Google Cloud, Kubernetes, Docker, Cloud Security, DevOps, CI/CD Pipelines',
        'DevOps, CI/CD, Jenkins, Git, Linux, Automation, Kubernetes, Infrastructure as Code, Docker',
        'Android, iOS, Flutter, React Native, Swift, Kotlin, Mobile UI/UX, Firebase, API Integration',
        'Wireframing, Prototyping, Figma, Adobe XD, User Research, UX Design, Visual Design, A/B Testing',
        'Full Stack Development, MERN Stack, MEAN Stack, SQL, NoSQL, GraphQL, API Development, Deployment',
        'Blockchain, Smart Contracts, Solidity, Ethereum, Web3, Cryptography, DeFi, Hyperledger, NFT',
        'Database Management, MySQL, PostgreSQL, NoSQL, MongoDB, Query Optimization, Database Security',
        'Linux, Windows Server, System Administration, Virtualization, Cloud Management, IT Security, Shell Scripting',
        'Unity, Unreal Engine, C#, Game Physics, Animation, AR/VR Development, 3D Modeling, Game Design Patterns'
    ],
    'salary': ['12-15 LPA', '15-18 LPA', '10-14 LPA', '18-22 LPA', '14-17 LPA',
               '13-16 LPA', '16-20 LPA', '15-19 LPA', '11-14 LPA', '12-16 LPA',
               '14-18 LPA', '17-21 LPA', '13-15 LPA', '11-13 LPA', '12-15 LPA']
})


# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
job_vectors = vectorizer.fit_transform(job_data['description''title''company'])

# Save the trained model
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))
pickle.dump(job_vectors, open('job_vectors.pkl', 'wb'))
pickle.dump(job_data, open('job_data.pkl', 'wb'))

print("✅ Job Recommendation Model Trained and Saved Successfully!")