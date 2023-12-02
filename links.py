from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import csv
print("Hello")




def get_links():
    options = Options()
    options.add_argument('--headless')
    edge_service = Service(executable_path=r"C:\Users\nkasa\Downloads\edgedriver_win64\msedgedriver.exe")

    driver = webdriver.Edge(service=edge_service, options=options)
    i = 0
    Job_Postings = [0]
    with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Job_Links2.csv", "w", newline="") as Jobs:
        with open(r"C:\Users\nkasa\PycharmProjects\pythonProject\Company_Links2.csv", "w", newline="") as Companies:
            writer_Job = csv.writer(Jobs)
            writer_Org = csv.writer(Companies)
            while (len(Job_Postings) != 0):
                Page = "https://wuzzuf.net/a/IT-Software-Development-Jobs-in-Egypt?start="
                Page += str(i)
                driver.get(Page)
                driver.implicitly_wait(3)
                Job_Postings = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/h2/a")
                Company = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div/a")
                for j in range(len(Job_Postings)):
                    writer_Job.writerow([Job_Postings[j].get_attribute("href")])
                    writer_Org.writerow([Company[j].get_attribute("href")])
                i += 1
    driver.quit()


get_links()

