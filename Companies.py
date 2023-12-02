from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import csv

Company = {
    "CompanyName" : None,
    "FoundationDate" : None,
    "Size" : None,
    "CompanyDescription" : None,
    "Address" : None,
    "City" : None,
    "Country" : None,
    "URL": None
}

Sectors = {
    "SectorName": None,
    "CompanyName": None
}

def get_company_info(start, end):
    options = Options()
    options.add_argument('--headless')
    edge_service = Service(executable_path=r"C:\Users\nkasa\Downloads\edgedriver_win64\msedgedriver.exe")
    driver = webdriver.Edge(service=edge_service, options=options)

    Links = open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Company_Links.csv", "r").read().splitlines()
   
    #write headers for each file
    with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Companies.csv", "w", newline="", encoding="utf_8") as Companies:
        writer = csv.DictWriter(Companies, fieldnames=Company.keys())
        writer.writeheader()

    with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Sectors.csv", "w", newline="", encoding="utf_8") as Company_ectors:
        writer = csv.DictWriter(Company_ectors, fieldnames= Sectors.keys())
        writer.writeheader()

    for j in range(start, end):
        link = Links[j]
        while (link[0] != 'h'):
            link = link[1:]
        driver.get(link)
        driver.implicitly_wait(3)

        # getting stuff and assigning them only 
        Name = driver.find_element(By.CLASS_NAME, "css-12s37jy")
        try:
            profile = driver.find_elements(By.CSS_SELECTOR, "#profile-section > div")
        except:
            profile = None
        try:
            Description = driver.find_element(By.CSS_SELECTOR, "#profile-section > p").text.replace("\n", "").replace("\t", "")
        except:
            Description = None
        try:
            website = driver.find_element(By.CSS_SELECTOR, "#app > div > div:nth-child(3) > div > div > div.css-12e2e2p > div.css-aqnjlk > div.css-1517rho > a").get_attribute("href")
        except:
            website = None
  

        # handling company name
        CompanyName = Name.text
        CompanyName.replace("Verified","").replace("New Company", "")

        #handling company foundation date, size, industry, location
        profile_split = profile[0].text.split("\n")
        for i in range(len(profile_split)):
            if profile_split[i].lower() == "founded:":
                FoundationDate = profile_split[i+1]
            elif profile_split[i].lower() == "company size:":
                Size = profile_split[i+1]
            elif profile_split[i].lower() == "industry:":
                Industry = profile_split[i+1]
            elif profile_split[i].lower() == "location:":
                Location = profile_split[i+1]

        try:
            FoundationDate is None
        except:
            FoundationDate = 0

        # fixing location
        location_split= Location.split(', ')
        if len(location_split) == 2 and (location_split[1].lower != "egypt" or location_split[1].lower == "egypt"):
            Address = None
            City = location_split[0]
            Country = location_split[1]
        elif len(location_split) == 3:
            Address = location_split[0]
            City = location_split[1]
            Country = location_split[2]
        elif len(location_split) == 1:
            Address = None
            City = None
            Country = location_split[0]

        # handling sector
        Sector_list = Industry.split(" . ")

        # handling company description to accomodate 'see more' button
        try:
            see_more = driver.find_element(By.CSS_SELECTOR, "#profile-section > p > span") 
            if see_more.text:
                see_more.click()
                Description = driver.find_element(By.CSS_SELECTOR,"#profile-section > p").text.replace("\n", "").replace("\t", "").replace("See Less","")
        except:
            pass

        # assigning values to the dictionary
        Company["CompanyName"] = CompanyName
        Company["FoundationDate"] = int(FoundationDate)
        Company["Size"] = Size
        Company["CompanyDescription"] = Description
        Company["Address"] = Address
        Company["City"] = City
        Company["Country"] = Country
        Company["URL"] = website

        Sectors["CompanyName"] = CompanyName

        with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\sth.csv", "a", newline="", encoding="utf_8") as Companies:
            writer = csv.DictWriter(Companies, fieldnames=Company.keys())
            writer.writerow(Company)
      #writing to the csv file
        with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Companies.csv", "a", newline="", encoding="utf_8") as Companies:
            writer = csv.DictWriter(Companies, fieldnames=Company.keys())
            writer.writerow(Company)

        with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Sectors.csv", "a", newline="", encoding="utf_8") as Company_ectors:
            for i in range(len(Sector_list)):
                Sectors["SectorName"] = Sector_list[i]
                writer = csv.DictWriter(Company_ectors, fieldnames= Sectors.keys())
                writer.writerow(Sectors)
    driver.quit()
       


get_company_info(0,534)
