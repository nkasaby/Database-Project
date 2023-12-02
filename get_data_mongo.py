import datetime
import time
import dateutil.utils
import re
import os
import pymongo
import json
from tabulate import tabulate
mongo_client = pymongo.MongoClient("mongodb+srv://nkasaby:NurKas369@cluster1.9rik0hu.mongodb.net/")
db = mongo_client["CareerCenter"]

userEmail = ""
def main_menu():
    print("Welcome to the Career Center!")
    print("Please select an option from the menu below:")
    print("1. Create a new user")
    print("2. Log in")
    print("3. Exit")

    choice = input("Enter your choice: ")
    os.system('cls')

    while (choice !="3" and choice != "2" and choice != "1"):
        print("Invalid choice, please enter a valid choice: ")

        print("1. Create a new user")
        print("2. Log in")
        print("3. Exit")

        choice = input("Enter your choice: ")
        os.system('cls')


    if choice == "1":
        print("_________________ Create User_______________________")
        create_user()
        print("Account created successfully!")
        time.sleep(1)
        os.system('cls')
        print("_________________ Filter List _______________________")
        app()
    elif choice == "2":
        print("_________________ Log in _______________________")
        login()
        print("Account logged in successfully!")
        os.system('cls')
        print("_________________ Filter List _______________________")
        app()
    elif choice == "3":
        print("Exiting!")
        time.sleep(2)
        os.system('cls')
        exit()
def checkDateFormat(dob):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, dob))
def isValidDate(Date):
    DateFormat = '%Y-%m-%d'
    validFormat = False
    try:
        dateObject = datetime.datetime.strptime(Date, DateFormat)
        validFormat = True
    except:
        validFormat = False

    if (validFormat):
        if (Date > dateutil.utils.today().strftime('%Y-%m-%d')):
            return False
        else:
            return True
    else:
        return False
def checkEmailFormat(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
def checkExistingEmail(user_email):

    result = db["Users"].find_one({"Email": user_email})
    if result is None:
        return False
    else:
        return True
def checkIfSkillExists():
    print("Please enter the skill names (separated by commas): ")
    skills = input()
    skills = skills.replace(" ","").split(",")
    existing = []
    for skill in skills:
        result = db["Skills"].find_one({"﻿SkillName": skill.strip()})
        if result is None:
            print("Skill does not exist")
        else:
            existing.append(skill)
    print(existing)
    if len(existing)>0:
        print("Taking Skills that exist.")
        print("Skills that exist are: ", existing)
    else:
        print("None of these skills exist")
    return existing
def create_user():

    print("Please enter your email (50 characters max) : ")
    email = input()
    if checkExistingEmail(email) == True:
        print("Email already exists, please log in: ")
        time.sleep(1)
        os.system('cls')
        main_menu()
        #email = input("Please enter your email: ")
    global userEmail
    userEmail = email

    while (checkEmailFormat(email) == False or len(email) > 50):
        print("Invalid email, please enter a valid email: ")
        email = input("Please enter your email: ")

    username = input("Please enter your username (30 characters max): ")
    while len(username) > 30:
        print("Invalid username, please enter a valid username: ")
        username = input("Please enter your username: ")

    gender = input("Please enter your gender (M/F): ").upper()
    while (gender != 'M' and gender != 'F') :
        print("Invalid gender type, please enter a valid answer")
        gender = input("Please enter your gender (M/F): ").upper()


    dob = input("Please enter your date of birth (YYYY-MM-DD): ")
    while checkDateFormat(dob) == False or isValidDate(dob) == False:
        print("Invalid date format, please enter a valid date: ")
        dob = input("Please enter your date of birth (YYYY-MM-DD): ")

    gpa = input("Please enter your GPA: ")
    while gpa.isdigit() and (int(gpa) > 0.0 and int(gpa) < 4.00) == False:
        print("Invalid GPA, please enter a valid GPA: ")
        gpa = input("Please enter your GPA: ")
    roundedGPA = round(float(gpa), 2)

    skills = checkIfSkillExists()

    user_document = {"Email": email, "Username": username, "Gender": gender, "Birthdate": dob, "GPA": roundedGPA, "Skills": skills}
    db["Users"].insert_one(user_document)
    return email

def login():
    email = input("Please enter your email: ")
    i = 0
    while (checkExistingEmail(email) == False or checkEmailFormat(email) == False) and i < 3:
        print("Email does not exist, please enter a valid email: ")
        email = input("Please enter your email: ")
        i += 1
    if i == 3:
        print("You have exceeded the number of tries, please create an account")
        time.sleep(1)
        os.system('cls')
        main_menu()
    else:
        global userEmail
        userEmail = email
def checkForCompany(company):
    result = db["Companies"].find_one({"CompanyName": company})
    print(company)
    if result is None:
        return False
    else:
        return True
def checkForJobPosting(companyName,jobTitle):
    result = db["JobPostings"].find_one({"CompanyName": companyName , "Title": jobTitle})
    if result is None:
        return False
    else:
        return True
def checkForSector(sector):
    result = db["Companies"].find_one({"SectorName": sector})
    if result is None:
        return False
    else:
        return True

def getSectorJobs(sector):
    for result in db["JobPostings"].find({"SectorName": sector}):
        result.pop("_id")
        formatted_object = json.dumps(result, indent=4)
        print(formatted_object)

def getSkillsJobs():
    skills = checkIfSkillExists()
    if len(skills) == 0:
        print("No skills found")
        print("Please choose another option from main menu")
        time.sleep(1)
        os.system('cls')
        app()

    for skill in skills:
        for result in db["JobPostings"].find({"Skills": skill}):
            result.pop("_id")
            formatted_object = json.dumps(result, indent=4)
            print(formatted_object)

def getTop5Sectors():

    for result in db["JobPostings"].aggregate(
        [
            {
                "$unwind": "$SectorName"
            },
            {
                "$group": {
                    "_id": "$SectorName",
                    "count": {"$sum": 1},
                    "AvgSalary": {"$avg": {"$subtract": [ {"$toDouble": "$MaxSalary"}, {"$toDouble":"$MinSalary"} ]}}
                }
            },

            {
                "$sort": {"count": -1}
            },
            {
                "$limit": 5
            },
            {
                "$project": {
                    "_id": 0,
                    "SectorName": "$_id",
                    "AvgSalary": {"$round": ["$AvgSalary", 2]},

                }
            }
        ]
    ):
        formatted_object = json.dumps(result, indent=4)
        print(formatted_object)

def getTop5Skills():

    for result in db["JobPostings"].aggregate(
        [
            {
                "$unwind": "$Skills"
            },
            {
                "$group": {
                    "_id": "$Skills",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            },
            {
                "$limit": 5
            },
            {
                "$project": {
                    "Skills": "$_id",

                }
            }
        ]
    ):
        result.pop("_id")
        formatted_object = json.dumps(result, indent=4)
        print(formatted_object)


def getTop5Startups():
    for result in db["Companies"].aggregate(
        [
            {
                "$group": {
                    "_id": "$CompanyName",
                    "FoundationDate": {"$first": "$FoundationDate"},
                    "Size": {"$first": "$Size"},
                    "CompanyDescription": {"$first": "$CompanyDescription"},
                    "City": {"$first": "$City"},
                    "Country": {"$first": "$Country"},
                    "URL": {"$first": "$URL"},
                    "CategoryName": {"$first": "$CategoryName"}}
            },

            {
                "$limit": 5
            },
            {
                "$project": {
                    "_id": 0,
                    "CompanyName": "$_id",
                    "FoundationDate": 1,
                    "Size": 1,
                    "CompanyDescription": 1,
                    "City": 1,
                    "Country": 1,
                    "URL": 1,
                    "ratio": {
                        "$cond": {
                            "if": {"$eq": ["$FoundationDate", None]},
                            "then": None,
                            "else": {
                                "$divide": [
                                    "$NumOfVacancies",
                                    {"$subtract": [dateutil.utils.today().year,  {"$toInt": "$FoundationDate"} ]}
                                ]
                            }
                        }
                    }
                }
            },
            {
                "$sort": {"ratio": -1}
            },
            {
                "$limit": 5
            }
        ]
    ):
        result.pop("ratio")
        if result["Country"] != "Egypt":
            continue
        formatted_object = json.dumps(result, indent=4)
        print(formatted_object)

    # mycursor = mydb.cursor()
    # sql = """SELECT C.* FROM company C
    #          INNER JOIN jobpostings J
    #          ON C.companyname = J.companyname
    #          WHERE C.Country = "Egypt"
    #          ORDER BY CASE WHEN C.foundationDate IS NOT NULL
    #          THEN J.NumOfVacancies/(year(current_date()) - C.FoundationDate) end DESC
    #          limit 5"""
    # mycursor.execute(sql, )
    # myresult = mycursor.fetchall()
    # mycursor.close()
    # fixingCompanyTuple(myresult)

def getTop5Companies():

    for result in db["Companies"].aggregate(
        [
            {
                "$group": {
                    "_id": "$CompanyName",
                    "MaxSalary": {"$max": {"$toDouble": "$MaxSalary"}},
                    "FoundationDate": {"$first": "$FoundationDate"},
                    "Size": {"$first": "$Size"},
                    "CompanyDescription": {"$first": "$CompanyDescription"},
                    "City": {"$first": "$City"},
                    "Country": {"$first": "$Country"},
                    "URL": {"$first": "$URL"},
                    "CategoryName": {"$first": "$CategoryName"},
                }
            },
            {
                "$sort": {"MaxSalary": -1}
            },
            {
                "$limit": 5
            },
            {
                "$project": {
                    "_id": 0,
                    "CompanyName": "$_id",
                    "FoundationDate": 1,
                    "Size": 1,
                    "CompanyDescription": 1,
                    "City": 1,
                    "Country": 1,
                    "URL": 1,
                    "CategoryName": 1,
                }
            },

        ]
    ):

        if "IT/Software Development" in result["CategoryName"]:
            formatted_object = json.dumps(result, indent=4)
            print(formatted_object)

def getCompanyJobs(company):
    for result in db["JobPostings"].find({"CompanyName": company}):
        result.pop("_id")
        formatted_object = json.dumps(result, indent=4)
        print(formatted_object)
def getTop5Categories():

    for result in db["JobPostings"].aggregate(
        [
            {
                "$unwind": "$Categories"
            },
            {
                "$group": {
                    "_id": "$Categories",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            },
            {
                "$limit": 6
            },
            {
                "$project": {
                    "_id": 0,
                    "Categories": "$_id",

                }
            }
        ]
    ):
        if result["Categories"] == "IT/Software Development":
            continue
        formatted_object = json.dumps(result, indent=4)
        print(formatted_object)

    # mycursor = mydb.cursor()
    # sql = """SELECT categoryname FROM jobpostingcategories jc
    #          WHERE categoryname != "it/software development"
    #          GROUP BY 1
    #          ORDER BY COUNT(title) DESC
    #          LIMIT 5;"""
    # mycursor.execute(sql, )
    # myresult = mycursor.fetchall()
    # mycursor.close()
    # colalign = ["center"]
    # print(tabulate(myresult, headers=["Category Name"],
    #                tablefmt="fancy_grid",
    #                colalign=colalign), "\n")
def appMenu():
    print("Please select an option from the menu below:")
    print("1. All the job postings for a given sector")
    print("2. All the job postings for a given set of skills")
    print("3. Top 5 sectors by number of job posts, and the average salary range for each")
    print("4. The top 5 skills that are in the highest demand")
    print("5. The top 5 growing startups in Egypt by the amount of vacancies they have compared to their foundation date")
    print("6. The top 5 most paying companies in the IT/Software Development field in Egypt")
    print("7. All the postings for a given company")
    print("8. The top 5 categories (other than IT/Software Development) that the postings are cross listed under based on the volume of postings")
    print("9. Apply For a Job")
    print("10. Exit")

def back ():
    print("Would you like to go back to app menu?")
    print("1. Yes")
    print("2. No, Exit Program")
    choice = input("Enter your choice: ")
    while (choice != "1" and choice != "2"):
        print("Invalid choice, please enter a valid choice: ")
        choice = input("Enter your choice: ")
    if choice == "1":
        os.system('cls')
        app()
    else:
        print("Exiting!")
        exit()

def app():
    print("Welcome to Career Center!")
    appMenu()
    choice = input("Enter your choice: ")

    while (choice.isdigit() == False or int(choice) < 1 or int(choice) > 10):
        print("Invalid choice, please enter a valid choice: ")
        appMenu()
        choice = input("Enter your choice: ")
        os.system('cls')

    os.system('cls')

    if choice == "1":
        print("_________________________ Job postings for a given sector _________________________")
        sector = input("Please enter a sector: ")
        i = 0

        while checkForSector(sector) == False and i < 3:
            print("Sector does not exist, please enter a valid sector: ")
            sector = input("Please enter a sector: ")
            i += 1

        os.system('cls')

        if checkForSector(sector) == True:
            print("_________________________" + sector.capitalize() + " Job Postings _________________________", "\n")
            getSectorJobs(sector)
        else:
            print("No sectors with that name :(")

        back()
    elif choice == "2":
        os.system('cls')
        print("______________________ Job postings for a given set of skills _________________________")
        getSkillsJobs()
        back()
    elif choice == "3":
        os.system('cls')
        print("_________________________ Top 5 Sectors _________________________")
        getTop5Sectors()
        back()
    elif choice == "4":
        os.system('cls')
        print("_________________________ Top 5 Skills _________________________")
        getTop5Skills()
        back()
    elif choice == "5":
        os.system('cls')
        print("_________________________ Top 5 Startups _________________________")
        getTop5Startups()
        back()
    elif choice == "6":
        os.system('cls')
        print("________________Top 5 most paying companies in the IT/Sofware Development field in Egypt________________")
        getTop5Companies()
        back()

    elif choice == "7":
        os.system('cls')
        company = input("Please enter a company name: ")
        os.system('cls')
        i = 0

        while checkForCompany(company) == False and i < 3:
            print("Company does not exist, please enter a valid company: ")
            company = input("Please enter a company: ")
            os.system('cls')
            i += 1

        if checkForCompany(company) == True:
            print("_________________________" + company.capitalize() + " Job Postings _________________________")
            getCompanyJobs(company)
        else:
            print("No company with that name :(")

        back()
    elif choice == "8":
        os.system('cls')
        print("_________________________ Top 5 Categories _________________________")
        getTop5Categories()
        back()
    elif choice == "9":
        os.system('cls')
        print("_________________________ Job Application _________________________")
        application()
        print("Application submitted successfully!")
        back()
        pass
    else:
        os.system('cls')
        print("Exiting!")
        exit()

def application():
    print("Your are logged in as: " + userEmail)
    email = userEmail
    companyName = input("Please enter the company name: ")
    i = 0
    while checkForCompany(companyName) == False or (len(companyName) > 100 or len(companyName)<1):
        print("Company does not exist or field is empty, please enter a valid company name: ")
        companyName = input("Please enter the company name: ")

    jobTitle = input("Please enter the job title: ")
    i = 0
    while checkForJobPosting(companyName,jobTitle) == False or (len(jobTitle) > 100 or len(jobTitle)<1):
        print("Job does not exist for company or field is empty, please enter a valid job title: ")
        jobTitle = input("Please enter the job title: ")

    coverLetter = input("Please enter your cover letter: ")
    while len(coverLetter) < 0:
        print("Cover letter cannot be empty, please enter a valid cover letter: ")
        coverLetter = input("Please enter your cover letter: ")

    applicationDate = dateutil.utils.today()

    application_document = {"Email": email, "ApplicationDate": applicationDate, "CoverLetter": coverLetter, "CompanyName": companyName, "Title": jobTitle}
    db["Applications"].insert_one(application_document)

main_menu()