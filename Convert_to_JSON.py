import json
import csv
import os


csv_directory = r"\Users\nkasa\PycharmProjects\pythonProject\csv files"
json_directory = r"\Users\nkasa\PycharmProjects\pythonProject\json files"

def convert_to_json(file_name):
    csv_file_path = os.path.join(csv_directory, file_name)

    with open(csv_file_path, "r", newline="", encoding="utf_8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    json_file_path = os.path.join(json_directory, file_name.replace(".csv", ".json"))

    with open(json_file_path, "w", newline="", encoding="utf_8") as json_file:
        json.dump(rows, json_file, indent=4)
def add_to_json(json_file_name, csv_file_name, attribute, attribute_name):
    json_file_path = os.path.join(json_directory, json_file_name)

    with open(json_file_path, "r", newline="", encoding="utf_8") as json_file:
        json_data = json.load(json_file)


    csv_file_path = os.path.join(csv_directory, csv_file_name)
    with open(csv_file_path, "r", newline="", encoding="utf_8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

        for object in json_data:
            for row in rows:
                try:
                    if object[attribute] == row[attribute]:
                        if attribute_name in object and row[attribute_name] not in object[attribute_name]:
                            object[attribute_name].append(row[attribute_name])
                        else:
                            object[attribute_name] = [row[attribute_name]]
                except:
                    if object[attribute] == row['﻿'+attribute]:
                        if attribute_name in object:
                            object[attribute_name].append(row[attribute_name])
                        else:
                            object[attribute_name] = [row[attribute_name]]

    with open(json_file_path, "w", newline="") as json_file:
        json.dump(json_data, json_file, indent=4)

    print("done")
def add_to_json_job_posting(json_file_name, csv_file_name, attribute, attribute_name):
    json_file_path = os.path.join(json_directory, json_file_name)

    with open(json_file_path, "r", newline="", encoding="utf_8") as json_file:
        json_data = json.load(json_file)


    csv_file_path = os.path.join(csv_directory, csv_file_name)
    with open(csv_file_path, "r", newline="", encoding="utf_8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        for object in json_data:
            for row in rows:
                if object["CompanyName"] == row["CompanyName"] and object["Title"] == row["Title"]:
                    if attribute in object:
                        object[attribute].append(row[attribute_name])
                    else:
                        object[attribute] = [row[attribute_name]]

    with open(json_file_path, "w", newline="") as json_file:
        json.dump(json_data, json_file, indent=4)
    print("done")


convert_to_json("Job_Posting.csv")
convert_to_json("Companies.csv")
convert_to_json("Categories.csv")
convert_to_json("Skills.csv")
convert_to_json("Users.csv")
convert_to_json("Applications.csv")

add_to_json_job_posting("Job_Posting.json", "Job_Categories.csv", "Categories", "CategoryName")
add_to_json_job_posting("Job_Posting.json", "Job_Skills.csv", "Skills", "SkillName")
add_to_json_job_posting("Job_Posting.json", "Sectors.csv", "CompanyName", "SectorName")
add_to_json("Job_posting.json", "Sectors.csv", "CompanyName", "SectorName")
add_to_json("Companies.json", "Sectors.csv", "CompanyName", "SectorName")
add_to_json("Companies.json", "Job_Posting.csv", "CompanyName", "Title")
add_to_json("Users.json", "UserSkills.csv", "Email", "SkillName")
add_to_json("Companies.json", "Job_Categories.csv", "CompanyName", "CategoryName")
add_to_json("Companies.json", "Job_Posting.csv", "CompanyName", "NumOfVacancies")
