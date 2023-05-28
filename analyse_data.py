"""
Open the saved csv file and add "Details" to the column heading above the job details (and any other column headings
required). Save as a xlsx file.
This program will open a selected xlsx file from above and analyze the text in the Details column for words or phrases.
The totals of these are added to a new Excel xlsx file, and it is saved as a new file.
"""

import pandas as pd
import re
from openpyxl import Workbook

# Groupings of attractive words and phrases for Generation Z
diversity = ["diversity", "inclusion", "diverse", "inclusive", "culture", "values", "trust", "equal", "equality"]
innovation = ["innovative mindset", "innovative", "innovation", "development", "training", "growth opportunities",
              "opportunity", "progressive", "progression", "technology"]
flexibility = ["flexible", "flexibility", "work from home", "work-life balance", "work life balance", "work-life",
               "wfh", "remote", "working hours"]
collaboration = ["collaborate", "collaboration", "team", "teamwork", "team-player", "contribute", "contribution",
                 "supportive", "participation", "participate"]
csr = ["csr", "corporate social responsibility", "corporate responsibility", "corporate citizenship",
       "initiative", "volunteer", "volunteering", "giving back", "sustainability", "sustainable", "sustainably",
       "environmental", "environmentally", "society", "carbon footprint", "promoting", "renewable energy",
       "minimizing waste"]

# Load the Excel file
file_name = input("Enter the name of the file: ")
# file_name = "adelaide.xlsx"
output_file_name = input("Enter the name of the export file: ")
# output_file_name = "output.xlsx"
df = pd.read_excel(file_name)

# Analyze each row
for index, row in df.iterrows():
    text = row["Details"]

    # Check for diversity
    diversity_count = 0
    for i in diversity:
        count = len(re.findall(rf"\b{i}\b", text, re.IGNORECASE))
        if count > 0:
            diversity_count += count

    # Check for innovation
    innovation_count = 0
    for i in innovation:
        count = len(re.findall(rf"\b{i}\b", text, re.IGNORECASE))
        if count > 0:
            innovation_count += count

    # Check for flexibility
    flexibility_count = 0
    for i in flexibility:
        count = len(re.findall(rf"\b{i}\b", text, re.IGNORECASE))
        if count > 0:
            flexibility_count += count

    # Check for collaboration
    collaboration_count = 0
    for i in collaboration:
        count = len(re.findall(rf"\b{i}\b", text, re.IGNORECASE))
        if count > 0:
            collaboration_count += count

    # Check for csr
    csr_count = 0
    for i in csr:
        count = len(re.findall(rf"\b{i}\b", text, re.IGNORECASE))
        if count > 0:
            csr_count += count

    # Update the dataframe with analysis results
    df.loc[index, "Diversity Count"] = int(diversity_count)
    df.loc[index, "Innovation Count"] = int(innovation_count)
    df.loc[index, "Flexibility Count"] = int(flexibility_count)
    df.loc[index, "Collaboration Count"] = int(collaboration_count)
    df.loc[index, "CSR Count"] = int(csr_count)
    # df.loc[index, "Total Count"] = diversity_count + innovation_count + flexibility_count + collaboration_count +
    # csr_count

# Write to a new Excel file
writer = pd.ExcelWriter(output_file_name, engine='openpyxl')
book = Workbook()
writer.Workbook = book
df.to_excel(writer, index=False)
# writer.save()
writer.close()  # Close the writer

# Print analysis results
print("Analysis Complete.")
