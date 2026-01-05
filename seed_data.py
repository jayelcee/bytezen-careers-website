#!/usr/bin/env python3
"""
Seed script to populate the database with sample data.
Run this script to add sample jobs and applicants to your database.
"""

from dotenv import load_dotenv
load_dotenv()

from database import db_session, Job, JobApplicant, init_db
from decimal import Decimal

def seed_jobs():
    """Add sample jobs to the database"""
    
    sample_jobs = [
        {
            "title": "Senior Software Engineer",
            "location": "Singapore",
            "salary": Decimal("150000"),
            "currency": "SGD",
            "responsibilities": "Design and develop scalable backend systems\nLead technical architecture decisions\nMentor junior developers\nCollaborate with cross-functional teams",
            "requirements": "5+ years of software development experience\nProficiency in Python, Java, or Go\nExperience with microservices architecture\nStrong problem-solving skills\nBachelor's degree in Computer Science or related field"
        },
        {
            "title": "Frontend Developer",
            "location": "Singapore",
            "salary": Decimal("95000"),
            "currency": "SGD",
            "responsibilities": "Build responsive and interactive user interfaces\nImplement modern web design patterns\nOptimize application performance\nCollaborate with UX/UI designers",
            "requirements": "3+ years of frontend development experience\nProficiency in React, Vue, or Angular\nStrong CSS and HTML skills\nExperience with REST APIs\nKnowledge of modern build tools"
        },
        {
            "title": "Data Scientist",
            "location": "Singapore",
            "salary": Decimal("120000"),
            "currency": "SGD",
            "responsibilities": "Develop machine learning models\nAnalyze large datasets for insights\nCreate data visualizations\nOptimize model performance",
            "requirements": "3+ years of data science experience\nProficiency in Python and SQL\nExperience with ML frameworks (TensorFlow, scikit-learn)\nStrong statistical knowledge\nMaster's degree in related field preferred"
        },
        {
            "title": "DevOps Engineer",
            "location": "Singapore",
            "salary": Decimal("110000"),
            "currency": "SGD",
            "responsibilities": "Design and maintain CI/CD pipelines\nManage cloud infrastructure\nEnsure system reliability and security\nMonitor and optimize performance",
            "requirements": "4+ years of DevOps experience\nProficiency with Docker and Kubernetes\nExperience with AWS, GCP, or Azure\nStrong scripting skills (Bash, Python)\nKnowledge of Infrastructure as Code"
        },
        {
            "title": "Product Manager",
            "location": "Singapore",
            "salary": Decimal("105000"),
            "currency": "SGD",
            "responsibilities": "Define product roadmap and strategy\nGather and analyze user requirements\nWork with engineering and design teams\nManage product launches and iterations",
            "requirements": "4+ years of product management experience\nStrong communication skills\nData-driven decision making\nExperience with product analytics tools\nKnowledge of agile methodologies"
        },
        {
            "title": "QA Automation Engineer",
            "location": "Singapore",
            "salary": Decimal("85000"),
            "currency": "SGD",
            "responsibilities": "Design and implement automated test frameworks\nWrite and maintain test cases\nIdentify and report bugs\nWork with development team on quality improvements",
            "requirements": "2+ years of QA automation experience\nProficiency in Selenium or similar tools\nExperience with Python or Java\nKnowledge of testing methodologies\nStrong analytical skills"
        }
    ]
    
    for job_data in sample_jobs:
        existing_job = db_session.query(Job).filter_by(title=job_data["title"]).first()
        if not existing_job:
            job = Job(
                title=job_data["title"],
                location=job_data["location"],
                salary=job_data["salary"],
                currency=job_data["currency"],
                responsibilities=job_data["responsibilities"],
                requirements=job_data["requirements"]
            )
            db_session.add(job)
            print(f"✓ Added job: {job_data['title']}")
        else:
            print(f"⊘ Job already exists: {job_data['title']}")
    
    db_session.commit()

def seed_applicants():
    """Add sample applicants to the database"""
    
    sample_applicants = [
        {
            "job_id": 1,
            "job_title": "Senior Software Engineer",
            "name": "John Doe",
            "age": 28,
            "birthday": "1997-05-15",
            "phone_number": "+65 9123 4567",
            "email": "john.doe@email.com",
            "address": "123 Marina Bay, Singapore 018972",
            "linkedin": "https://linkedin.com/in/johndoe",
            "education": "Bachelor's in Computer Science from NUS\nMaster's in Software Engineering from NTU",
            "experience": "5 years at Tech Corp as Software Engineer\n2 years at StartupXYZ as Senior Engineer\nLed development of 3 major products",
            "gender": "Male",
            "nationality": "Singaporean",
            "status": "Accepted",
            "username": "johndoe123",
            "password": "password123"
        },
        {
            "job_id": 2,
            "job_title": "Frontend Developer",
            "name": "Jane Smith",
            "age": 26,
            "birthday": "1999-03-20",
            "phone_number": "+65 9876 5432",
            "email": "jane.smith@email.com",
            "address": "456 Orchard Road, Singapore 238824",
            "linkedin": "https://linkedin.com/in/janesmith",
            "education": "Bachelor's in Information Technology from Nanyang Poly",
            "experience": "3 years at WebCorp as Frontend Developer\n1 year at DesignStudio as UI Developer",
            "gender": "Female",
            "nationality": "Singaporean",
            "status": "Accepted",
            "username": "janesmith456",
            "password": "password456"
        },
        {
            "job_id": 1,
            "job_title": "Senior Software Engineer",
            "name": "Michael Chen",
            "age": 32,
            "birthday": "1993-08-10",
            "phone_number": "+65 8765 4321",
            "email": "michael.chen@email.com",
            "address": "789 Clementi Avenue, Singapore 129915",
            "linkedin": "https://linkedin.com/in/michaelchen",
            "education": "Bachelor's in Computer Science from IIT",
            "experience": "6 years at CloudTech as Backend Engineer\n3 years at DataCorp as Senior Engineer\nExpertise in distributed systems",
            "gender": "Male",
            "nationality": "Indian",
            "status": "Accepted",
            "username": "michaelchen789",
            "password": "password789"
        },
        {
            "job_id": 3,
            "job_title": "Data Scientist",
            "name": "Sarah Johnson",
            "age": 29,
            "birthday": "1996-11-25",
            "phone_number": "+65 9234 5678",
            "email": "sarah.johnson@email.com",
            "address": "321 Bukit Timah, Singapore 259759",
            "linkedin": "https://linkedin.com/in/sarahjohnson",
            "education": "Master's in Data Science from Stanford\nBachelor's in Mathematics from Cambridge",
            "experience": "4 years at Analytics Inc as Data Scientist\n2 years at FinTech Co as ML Engineer\nPublished 5 research papers on ML",
            "gender": "Female",
            "nationality": "British",
            "status": "Accepted",
            "username": "sarahjohnson234",
            "password": "password234"
        }
    ]
    
    for applicant_data in sample_applicants:
        existing_applicant = db_session.query(JobApplicant).filter_by(username=applicant_data["username"]).first()
        if not existing_applicant:
            applicant = JobApplicant(
                job_id=applicant_data["job_id"],
                job_title=applicant_data["job_title"],
                name=applicant_data["name"],
                age=applicant_data["age"],
                birthday=applicant_data["birthday"],
                phone_number=applicant_data["phone_number"],
                email=applicant_data["email"],
                address=applicant_data["address"],
                linkedin=applicant_data["linkedin"],
                education=applicant_data["education"],
                experience=applicant_data["experience"],
                gender=applicant_data["gender"],
                nationality=applicant_data["nationality"],
                status=applicant_data["status"],
                username=applicant_data["username"],
                password=applicant_data["password"]
            )
            db_session.add(applicant)
            print(f"✓ Added applicant: {applicant_data['name']}")
        else:
            print(f"⊘ Applicant already exists: {applicant_data['name']}")
    
    db_session.commit()

def main():
    """Run all seed functions"""
    print("=" * 50)
    print("ByteZen Careers Website - Database Seeding")
    print("=" * 50)
    
    print("\n📊 Initializing database tables...")
    init_db()
    print("✓ Database tables ready")
    
    print("\n📝 Seeding jobs...")
    seed_jobs()
    
    print("\n👥 Seeding applicants...")
    seed_applicants()
    
    print("\n" + "=" * 50)
    print("✅ Database seeding completed!")
    print("=" * 50)
    print("\n📌 Sample Admin Credentials:")
    print("   Username: admin")
    print("   Password: admin@bytezen!")
    print("\n📌 Sample Applicant Credentials:")
    print("   Username: johndoe123")
    print("   Password: password123")
    print("\n✨ Your website is ready to use!")
    print("   Run: python3 app.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
