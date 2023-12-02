from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import datetime
from dateutil.relativedelta import relativedelta
import csv


JobPosting= {
    "CompanyName": None,
    "Title": None,
    "MinSalary": None,
    "MaxSalary": None,
    "EducationLevel": None,
    "JobDescription": None,
    "CareerLevel": None,
    "Experience": None,
    "NumOfVacancies": None,
    "PostingDate": None,
    "Address": None,
    "City": None
}

JobCategories = {
    "Title": None,
    "CompanyName": None,
    "CategoryName": None
}

JobSkills = {
    "Title": None,
    "CompanyName": None,
    "SkillName": None
}

JobType= {
    "Title": None,
    "CompanyName": None,
    "JobTypeName": None
}

def get_job_posting_info(start, end):
    options = Options()
    options.add_argument('--headless')
    edge_service = Service(executable_path=r"C:\Users\nkasa\Downloads\edgedriver_win64\msedgedriver.exe")
    driver = webdriver.Edge(service=edge_service, options=options)

    Links = open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Job_Links.csv", "r").read().splitlines()

    # write headers for each file
    with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Job_Postings.csv", "w", newline="", encoding="utf_8") as Job_Postings:
        writer = csv.DictWriter(Job_Postings, fieldnames=JobPosting.keys())
        writer.writeheader()

    with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Job_Skills.csv", "w", newline="", encoding="utf_8") as Job_Skills:
        writer = csv.DictWriter(Job_Skills, fieldnames=JobSkills.keys())
        writer.writeheader()

    with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Job_Type.csv", "w", newline="", encoding="utf_8") as Job_Type:
        writer = csv.DictWriter(Job_Type, fieldnames=JobType.keys())
        writer.writeheader()

    with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Job_Categories.csv", "w", newline="", encoding="utf_8") as Job_Categories:
        writer = csv.DictWriter(Job_Categories, fieldnames=JobCategories.keys())
        writer.writeheader()

    for j in range(start, end):
        print(j)
        link = Links[j]
        driver.get(link)
        driver.implicitly_wait(3)

        # getting stuff and assigning them only 
        Job_Title = driver.find_element(By.CLASS_NAME, "css-f9uh36")
        try:
            Company_Name = driver.find_element(By.CSS_SELECTOR, "#app > div > main > section.css-dy1y6u > div > strong.css-9geu3q > div > a").text 
        except:
            Company_Name = "Confidential"

        closed = driver.find_elements(By.CSS_SELECTOR, "#app > div > main > section.css-1yzinaq > span")
        if closed:
            continue

        Posting_Date = driver.find_element(By.CLASS_NAME, "css-182mrdn")
        Vacancies = driver.find_elements(By.CSS_SELECTOR, "#app > div > main > section.css-dy1y6u > div > div.css-104dl8g > div > span")
        Location = driver.find_element(By.CLASS_NAME, "css-9geu3q")
        details = driver.find_elements(By.CLASS_NAME, "css-4xky9y")
        JobDescription = driver.find_element(By.CSS_SELECTOR,"#app > div > main > section:nth-child(3) > div")
        Categories = driver.find_elements(By.CSS_SELECTOR, "ul.css-h5dsne li.css-tmajg1 a.css-ya9gwj span.css-158icaa")
        Skills = driver.find_elements(By.CSS_SELECTOR, "div.css-s2o0yh span.css-158icaa")
        Type = driver.find_elements(By.CSS_SELECTOR, "#app > div > main > section.css-dy1y6u > div > div.css-11rcwxl > a > span")


        # Company_Name = Company_Name.text if Company_Name is not "Confidential"
        Posting_Date = Posting_Date.text.split(' ')
        if (Posting_Date[2] == 'minutes' or Posting_Date[2] == 'minute'):
            Posting_Date = datetime.datetime.now() - relativedelta(minutes=int(Posting_Date[1]))
        elif (Posting_Date[2] == 'hours' or Posting_Date[2] == 'hour'):
            Posting_Date = datetime.datetime.now() - relativedelta(hours=int(Posting_Date[1]))
        elif (Posting_Date[2] == 'days' or Posting_Date[2] == 'day'):
            Posting_Date = datetime.datetime.now() - relativedelta(days=int(Posting_Date[1]))
        elif (Posting_Date[2] == 'months' or Posting_Date[2] == 'month'):
            Posting_Date = datetime.datetime.now() - relativedelta(months=int(Posting_Date[1]))

        fixed_date = Posting_Date.replace(microsecond=0)

        # fixing vacancies
        if len(Vacancies) > 1:
                Vacancies.pop(0)
                Vacancies = Vacancies[0].text.split(' ')[0]

        elif len(Vacancies) == 1:
            for char in Vacancies[0].text:
             if char.isdigit():
                Vacancies = char
        else:
            Vacancies = Vacancies[0].text.split(' ')[0]

        
        # fixing location
        Location = Location.text.split('\n- \n')
        Location[1] = Location[1].split(', ')
        if Location[1][1].lower() == "egypt":
            address = ""
            city = Location[1][0]
        else:
            address = Location[1][0]
            city = Location[1][1]

        Experience = details[0].text
        CareerLevel = details[1].text
        EducationLevel = details[2].text

        #fixing salary
        salary = details[4].text if len(details) == 5 else details[3].text
        salary_split = salary.split(' ')
        if len(salary_split) == 1:
            min_salary = salary_split[0]
            max_salary = salary_split[0]
        elif len(salary_split) == 0:
            min_salary = 0.0
            max_salary = 0.0
        elif len(salary_split) == 2:
            min_salary = salary_split[0]
            max_salary = salary_split[1]
        else:
            if len(salary_split) == 6 and salary_split[5].lower == "year":
                min_salary = salary_split[0]/12
                max_salary = salary_split[2]/12
            else:
                min_salary = salary_split[0]
                max_salary = salary_split[2]

        if min_salary.isdigit()==0 or max_salary.isdigit()==0:
            min_salary = 0.0
            max_salary = 0.0

        #assigning the data to the dictionary
        JobPosting["Title"] = Job_Title.text
        JobPosting["CompanyName"] = Company_Name
        JobPosting["PostingDate"] = fixed_date
        JobPosting["NumOfVacancies"] = int(Vacancies)
        JobPosting["Address"] = address
        JobPosting["City"] = city
        JobPosting["Experience"] = Experience
        JobPosting["CareerLevel"] = CareerLevel
        JobPosting["EducationLevel"] = EducationLevel
        JobPosting["MinSalary"] = float(min_salary)
        JobPosting["MaxSalary"] = float(max_salary)
        JobPosting["JobDescription"] =JobDescription.text.replace('\n', ' ').replace('\t', ' ')
        
        JobCategories["Title"] = Job_Title.text
        JobCategories["CompanyName"] = Company_Name

        JobSkills["Title"] = Job_Title.text
        JobSkills["CompanyName"] = Company_Name

        JobType["Title"] = Job_Title.text
        JobType["CompanyName"] = Company_Name

        print(JobPosting)

        # write job posting
        with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Job_Postings.csv", "a", newline="", encoding="utf_8") as Job_Postings:
            writer = csv.DictWriter(Job_Postings, fieldnames=JobPosting.keys())
            writer.writerow(JobPosting)

        #write job categories
        with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Job_Categories.csv", "a", newline="", encoding="utf_8") as Job_Categories:
            for i in range(len(Categories)):
                JobCategories["CategoryName"] = Categories[i].text
                writer = csv.DictWriter(Job_Categories, fieldnames=JobCategories.keys())
                writer.writerow(JobCategories)
        
        # write job skills
        with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Job_Skills.csv", "a", newline="", encoding="utf_8") as Job_Skills:
            for i in range(len(Skills)):
                JobSkills["SkillName"] = Skills[i].text.lower()
                writer = csv.DictWriter(Job_Skills, fieldnames=JobSkills.keys())
                writer.writerow(JobSkills)

        # write job type
        with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Job_Type.csv", "a", newline="", encoding="utf_8") as Job_Type:
            for i in range(len(Type)):
                JobType["JobTypeName"] = Type[i].text
                writer = csv.DictWriter(Job_Type, fieldnames=JobType.keys())
                writer.writerow(JobType)

    driver.quit()

get_job_posting_info(0,1374)


