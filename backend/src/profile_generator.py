import pandas as pd
import random
from faker import Faker

fake = Faker()

n_profiles = 500

countries = ["India", "China", "Brazil", "Pakistan", "USA", "Germany", "Nigeria", "South Korea", "Mexico", "Canada"]
industries = [
    "Software Engineering", "Data Science", "Finance", "Electrical Engineering",
    "Marketing", "UX Design", "Cybersecurity", "AI Research", "Product Management", "Mechanical Engineering"
]

skills_by_industry = {
    "Software Engineering": ["Python", "Java", "C++", "AWS", "React", "SQL", "Docker"],
    "Data Science": ["Python", "R", "SQL", "TensorFlow", "Pandas", "Scikit-learn", "Tableau"],
    "Finance": ["Excel", "Python", "R", "Quantitative Analysis", "Bloomberg", "SQL"],
    "Electrical Engineering": ["MATLAB", "C", "Embedded Systems", "PCB Design", "Verilog"],
    "Marketing": ["SEO", "Google Analytics", "Excel", "Content Strategy", "Social Media", "Copywriting"],
    "UX Design": ["Figma", "Adobe XD", "HTML", "CSS", "User Research", "Wireframing"],
    "Cybersecurity": ["Linux", "Network Security", "Python", "Ethical Hacking", "Firewalls"],
    "AI Research": ["Python", "PyTorch", "TensorFlow", "Deep Learning", "Computer Vision", "NLP"],
    "Product Management": ["Agile", "Scrum", "SQL", "Data Analytics", "Roadmapping", "Stakeholder Management"],
    "Mechanical Engineering": ["SolidWorks", "AutoCAD", "Thermodynamics", "MATLAB", "Simulation"]
}

companies = [fake.company() for _ in range(100)]

data = []

for i in range(1, n_profiles + 1):
    industry = random.choice(industries)
    country = random.choice(countries)
    skills = random.sample(skills_by_industry[industry], k = random.randint(3, 5))
    company = random.choice(companies)

    data.append({
            "id": i,
            "name": fake.name(),
            "industry": industry,
            "country": country,
            "skills": ",".join(skills),
            "company": company
        }
    )

df = pd.DataFrame(data)
df.to_csv("../data/raw/fake_profiles.csv", index=False)

print("500 profile generated!")