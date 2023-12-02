import datetime
import time
import dateutil.utils
import mysql.connector
import re
import os
from mysql.connector import IntegrityError
from tabulate import tabulate

# Connect to database
mydb = mysql.connector.connect(
    host="db4free.net",
    user="nkasaby",
    password="NurKas369",
    database="careercenter"
)

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
        email = create_user()
        skills = checkIfSkillExists()
        insert_skills(email, skills)
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
def checkExistingEmail():
    uniqueEmail = []
    mycursor = mydb.cursor()
    sql = "SELECT email FROM users"
    mycursor.execute(sql,)
    myresult = mycursor.fetchall()
    for x in myresult:
        for y in x:
            uniqueEmail.append(y)
    mycursor.close()
    return uniqueEmail
def create_user():

    print("Please enter your email (50 characters max) : ")
    email = input()
    if email in checkExistingEmail():
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

    gender = input("Please enter your gender (M/F/Prefer not to say): ").lower()
    while gender != 'm' and gender != 'f':
        print("Invalid gender type, please enter a valid answer")
        gender = input("Please enter your gender (M/F): ").lower()


    dob = input("Please enter your date of birth (YYYY-MM-DD): ")
    while checkDateFormat(dob) == False or isValidDate(dob) == False:
        print("Invalid date format, please enter a valid date: ")
        dob = input("Please enter your date of birth (YYYY-MM-DD): ")

    gpa = input("Please enter your GPA: ")
    while gpa.isdigit() and (int(gpa) > 0.0 and int(gpa) < 4.00) == False:
        print("Invalid GPA, please enter a valid GPA: ")
        gpa = input("Please enter your GPA: ")
    roundedGPA = round(float(gpa), 2)


    mycursor = mydb.cursor()
    sql = "INSERT INTO users (email,username,gender,birthdate,gpa) VALUES (%s, %s, %s, %s, %s)"
    val = (email,username,gender,dob,roundedGPA)

    try:
        mycursor.execute(sql, val)
        mydb.commit()
    except IntegrityError as e:
        print("user exists in app database")
        mydb.rollback()

    mycursor.close()
    return email
def checkIfSkillExists():
    os.system('cls')
    print("Please enter the skill names (separated by commas): ")
    skills = input().lower()
    skills = skills.replace(" ","").split(",")
    suggestions = []
    suggestionNames= []
    existing = []
    num = 0
    mycursor = mydb.cursor()
    #existingSkills = []
    for skill in skills:
        sql = "SELECT skillname FROM skills where skillname = %s"
        mycursor.execute(sql,(skill,))
        myresult = mycursor.fetchall()

        if len(myresult) == 0:
            os.system('cls')
            print(skill + " does not exist, did you mean? ")
            sql_2 = "SELECT skillname FROM skills WHERE skillname LIKE %s LIMIT 5"
            mycursor.execute(sql_2,(f"{skill[:2]}%",))
            suggestions.append(mycursor.fetchall())
            for i in range(len(suggestions)):
                for y in suggestions[i]:
                    num+=1
                    suggestionNames.append(y[0])
                    print(num, y[0])
            if len(suggestionNames) == 0:
                print("No suggestions found")
                print("Taking List With Skills that Exist...")
            else:
                print("Options: ")
                print("1. Yes, I want to choose from the list")
                print("2. No, I do not mean any of those")
                choice = input()
                if choice == "1":
                    print("Please enter the number of the skill you meant: ")
                    skillChoice = int(input())
                    existing.append(suggestionNames[skillChoice-1])
                    suggestions = []
                    num = 0
                    suggestionNames = []

                if choice == "2":
                    suggestions = []
                    num = 0
                    print("Taking List With Skills that Exist...")
            suggestionNames = []
        else:
            existing.append(skill)
    mycursor.close()
    print("Skills that exist are: ", existing)
    return existing
def insert_skills(email, skills):
    mycursor = mydb.cursor()
    for skill in skills:
        sql = "INSERT INTO userskills (Email, skillName) VALUES (%s, %s)"
        val = (email, skill)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except IntegrityError as e:
            print("skill for this user exists in database")
            mydb.rollback()

def login():
    email = input("Please enter your email: ")
    i = 0
    while (email not in checkExistingEmail() or checkEmailFormat(email) == False) and i < 3:
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
    mycursor = mydb.cursor()
    sql = """SELECT companyname FROM company WHERE companyname = '%s' """ % (company)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mycursor.close()
    if len(myresult) == 0:
        return False
    else:
        return True
def checkForJobPosting(companyName,jobTitle):
    mycursor = mydb.cursor()
    sql = """SELECT companyname,title FROM jobpostings WHERE companyName= %s AND title = %s"""
    var = (companyName,jobTitle)
    mycursor.execute(sql,var)
    myresult = mycursor.fetchall()
    mycursor.close()
    if len(myresult) == 0:
        return False
    else:
        return True
def checkForSector(sector):
    mycursor = mydb.cursor()
    sql = """SELECT sectorName FROM sectors WHERE sectorName = '%s' """ % (sector)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mycursor.close()
    if len(myresult) == 0:
        return False
    else:
        return True
def fixingCompanyTuple(myresult):
    modified_results = []
    colalign = ["center", "center", "center", "center", "center", "center", "center"]
    for result in myresult:
        modified_result = list(result)
        for i in range(len(modified_result)):
            if (modified_result[i] is None):
                modified_result[i] = "N/A"
        modified_results.append(tuple(modified_result))

    print(tabulate(modified_results,
                   headers=["Company Name", "Foundation Date", "Size", "Company Description", "City", "Country", "URL"],
                   tablefmt='fancy_grid',
                   colalign=colalign,
                   maxcolwidths=[25, 25, 25, 50, 15, 15, 25]))
def fixingJobPostingTuple(myresult):
    modified_results = []
    colalign = ["center", "center", "center", "center", "center", "center", "center", "center", "center", "center",
                "center", "center"]
    for result in myresult:
        modified_result = list(result)
        for i in range(len(modified_result)):
            if (modified_result[i] is None ):
                modified_result[i] = "Confidential"
            if (modified_result[2] == 0.0 and modified_result[3] == 0.0):
                modified_result[2] = "Confidential"
                modified_result[3] = "Confidential"
            modified_result[5] = modified_result[5][:100]+"..."
        modified_results.append(tuple(modified_result))

    print(tabulate(modified_results,
                   headers=["Company", "Position", "Min Salary", "Max Salary", "Education", "Description",
                            "Career Level", "Experience", "Vacancies", "Posting Date", "Address", "City"],
                   tablefmt='fancy_grid',
                   colalign=colalign,
                   maxcolwidths=[15, 15, 15, 15, 15, 30, 15, 15, 15, 15, 15, 15]))
def getSectorJobs(sector):
    mycursor = mydb.cursor()
    sql = "SELECT J.* FROM jobpostings J INNER JOIN company C ON J.companyname = C.companyname INNER JOIN sectors S On C.Companyname = S.companyname WHERE SectorName = %s"
    mycursor.execute(sql,(sector,))
    myresult = mycursor.fetchall()
    mycursor.close()
    fixingJobPostingTuple(myresult)
#NEED TO DO
def getSkillsJobs():
    mycursor = mydb.cursor()
    skills = []
    all_results = []
    skills = checkIfSkillExists()
    if len(skills) == 0:
        print("No skills found")
        print("Please choose another option from main menu")
        time.sleep(1)
        os.system('cls')
        app()
    else:
        for skill in skills:
            sql = (""" SELECT J.* FROM jobpostings J 
                     INNER JOIN jobpostingskills JS 
                     ON J.CompanyName = JS.CompanyName 
                     AND J.Title = JS.Title  
                     WHERE JS.SkillName = %s """)
            mycursor.execute(sql, (skill,))
            myresult = mycursor.fetchall()
            all_results.extend(myresult)
        fixingJobPostingTuple(all_results)
    mycursor.close()
def getTop5Sectors():
    mycursor = mydb.cursor()
    sql = """SELECT DISTINCT(S.SectorName), ROUND(AVG(J.MaxSalary - J.MinSalary),2) AS Avg_Salary 
            FROM sectors S INNER JOIN jobpostings J
            ON S.companyname = J.companyname
            GROUP BY 1
            ORDER BY COUNT(title) DESC
            LIMIT 5"""

    mycursor.execute(sql, )
    myresult = mycursor.fetchall()
    mycursor.close()
    colalign = ["center", "center"]
    print(tabulate(myresult, headers=["Sector Name", "Average Salary Range"], tablefmt='fancy_grid', colalign=colalign))
def getTop5Skills():
    mycursor = mydb.cursor()
    sql = """SELECT skillname FROM jobpostingskills
             GROUP BY 1
             ORDER BY COUNT(*) DESC
             LIMIT 5"""
    mycursor.execute(sql, )
    myresult = mycursor.fetchall()
    mycursor.close()
    colalign = ["center"]
    print(tabulate(myresult, headers=["Skill Name"], tablefmt='fancy_grid', colalign=colalign))
    pass
def getTop5Startups():
    mycursor = mydb.cursor()
    sql = """SELECT C.* FROM company C
             INNER JOIN jobpostings J
             ON C.companyname = J.companyname
             WHERE C.Country = "Egypt"
             ORDER BY CASE WHEN C.foundationDate IS NOT NULL 
             THEN J.NumOfVacancies/(year(current_date()) - C.FoundationDate) end DESC
             limit 5"""
    mycursor.execute(sql, )
    myresult = mycursor.fetchall()
    mycursor.close()
    fixingCompanyTuple(myresult)
def getTop5Companies():
    mycursor = mydb.cursor()
    sql = """SELECT c.*, max(MaxSalary) FROM company c
            inner join jobpostings J
            on c.companyname = J.companyname
            INNER JOIN jobpostingcategories JC
            ON J.title = JC.title
            AND J.companyname = JC.companyname
            WHERE categoryname = "IT/Software Development"
            AND c.country = "Egypt"
            GROUP BY 1,2,3,4,5,6,7
            ORDER BY max(maxsalary) DESC
            LIMIT 5"""
    mycursor.execute(sql, )
    myresult = mycursor.fetchall()
    mycursor.close()
    myresult = [x[:-1] for x in myresult]

    fixingCompanyTuple(myresult)
def getCompanyJobs(company):
    mycursor = mydb.cursor()
    sql = """SELECT * FROM jobpostings
             WHERE companyname = %s"""
    mycursor.execute(sql, (company,))
    myresult = mycursor.fetchall()
    mycursor.close()
    fixingJobPostingTuple(myresult)
def getTop5Categories():
    mycursor = mydb.cursor()
    sql = """SELECT categoryname FROM jobpostingcategories jc
             WHERE categoryname != "it/software development"
             GROUP BY 1
             ORDER BY COUNT(title) DESC
             LIMIT 5;"""
    mycursor.execute(sql, )
    myresult = mycursor.fetchall()
    mycursor.close()
    colalign = ["center"]
    print(tabulate(myresult, headers=["Category Name"],
                   tablefmt="fancy_grid",
                   colalign=colalign), "\n")
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
        sector = input("Please enter a sector: ").lower()
        i = 0

        while checkForSector(sector) == False and i < 3:
            print("Sector does not exist, please enter a valid sector: ")
            sector = input("Please enter a sector: ").lower()
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
        company = input("Please enter a company name: ").lower()
        os.system('cls')
        i = 0

        while checkForCompany(company) == False and i < 3:
            print("Company does not exist, please enter a valid company: ")
            company = input("Please enter a company: ").lower()
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
    print("Would you like to apply with a different email? (must be registered on the app)")
    print("1. Yes")
    print("2. No")
    choice = input("Enter your choice: ")

    while (choice != "1" and choice != "2"):
        print("Invalid choice, please enter a valid choice: ")
        choice = input("Enter your choice: ")

    if choice == "1":
        email = input("Please enter your email: ")
        i=0
        while email not in checkExistingEmail() or checkEmailFormat(email) == False or (len(email) > 50 or len(email)<1):
            print("Email does not exist or field is empty, please enter a valid email: ")
            email = input("Please enter your email: ")
            i+=1
    else:
        email = userEmail

    companyName = input("Please enter the company name: ").lower()
    i = 0
    while checkForCompany(companyName)==False or (len(companyName) > 100 or len(companyName)<1):
        print("Company does not exist or field is empty, please enter a valid company name: ")
        companyName = input("Please enter the company name: ").lower()

    jobTitle = input("Please enter the job title: ").lower()
    i = 0
    while checkForJobPosting (companyName,jobTitle) == False or (len(jobTitle) > 100 or len(jobTitle)<1):
        print("Job does not exist for company or field is empty, please enter a valid job title: ")
        jobTitle = input("Please enter the job title: ").lower()

    coverLetter = input("Please enter your cover letter: ")
    while len(coverLetter) < 0:
        print("Cover letter cannot be empty, please enter a valid cover letter: ")
        coverLetter = input("Please enter your cover letter: ")

    applicationDate = dateutil.utils.today()

    mycursor = mydb.cursor()
    sql = "INSERT INTO application (Email,ApplicationDate,CoverLetter,CompanyName,Title) VALUES (%s, %s, %s, %s, %s)"
    val = (email,applicationDate,coverLetter,companyName,jobTitle)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
    except IntegrityError as e:
        print("application exists in database")
        mydb.rollback()
    mycursor.close()

# main_menu()

getTop5Startups()