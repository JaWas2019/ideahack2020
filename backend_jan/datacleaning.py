#%%
import pandas as pd
import numpy as np
import csv
import json

#%%
# load required data and strip unnecessary columns
occupations_df = pd.read_csv("./Data/occupations_en.csv")
occupations_df = occupations_df.drop(["conceptType", "iscoGroup", "altLabels", "hiddenLabels", "status", "modifiedDate", "scopeNote", "definition", "inScheme"], axis=1) 
skills_df = pd.read_csv("./Data/skills_en.csv")
skills_df = skills_df.drop(["conceptType", "skillType", "reuseLevel", "altLabels", "hiddenLabels", "status", "modifiedDate", "scopeNote", "definition", "inScheme"], axis=1) 
relations_df = pd.read_csv("./Data/occupationSkillRelations.csv")
relations_df = relations_df.drop(["relationType", "skillType"], axis=1)

# %%
# extract uris from urls
def clean_url (x):
    return x[-36:]

occupations_df["conceptUri"] = occupations_df["conceptUri"].apply(clean_url)
skills_df["conceptUri"] = skills_df["conceptUri"].apply(clean_url)
relations_df["occupationUri"] = relations_df["occupationUri"].apply(clean_url)
relations_df["skillUri"] = relations_df["skillUri"].apply(clean_url)

# %%
# save pickled DataFrames
pd.to_pickle(occupations_df, "./Data/occupations.pkl")
pd.to_pickle(skills_df, "./Data/skills.pkl")
pd.to_pickle(relations_df, "./Data/relations.pkl")

# %%
# testing only
#occupations_df_test = occupations_df.head(10)
#occupation_codes = occupations_df_test["conceptUri"]

# %%
# extract occupation codes to use as index for matrix
occupation_codes = occupations_df["conceptUri"]

# %%
# initialize new relations matrix
relation_matrix = pd.DataFrame(index=occupation_codes)

# %%
# TESTING ONLY
# Loop over occupations, query for required skills and set key-pair to 1
# TBH, this is inefficient af - if it doesn't finish until tomorrow, I'll rewrite it and
# simply loop over all entries in the relations_df, it is completely useless to filter the entries by occupations
#for occupation_uri, row in relation_matrix.iterrows():
#    matched = relations_df[relations_df.occupationUri.eq(occupation_uri)]
#    for i, r in matched.iterrows():
#        skill_uri = r["skillUri"]
#        relation_matrix.at[occupation_uri, skill_uri] = 1

# %%
# loops through relations to create a matrix (let's pray it doesn't take up way too much space)
for index, row in relations_df.iterrows():
    relation_matrix.at[row["occupationUri"], row["skillUri"]] = 1

# %%
# Hallelujah! It finished! Quick, save it!
relation_matrix = relation_matrix.fillna(0)
pd.to_pickle(relation_matrix, "./Data/relation_matrix.pkl")

#%%
relation_matrix = pd.read_pickle("./Data/relation_matrix.pkl")

#%%
skill_profiles = pd.read_csv("./Data/skill_profiles.csv", error_bad_lines=False, delimiter="\t", index_col=0)

for index, row in skill_profiles.iterrows():
    skills_to_fix = row["skills"]
    skills_to_fix = skills_to_fix.strip('][').split("\", \"")
    fixed_skills = []
    # I am not sure if this is even necessary anymore because I escaped the "" in the split now, but it's fast, so it stays.
    for skill in skills_to_fix:
        fixed_skills.append(skill.strip("\""))
    skill_profiles.iat[index, 1] = fixed_skills
# %%
skill_list = list(relation_matrix.columns)
employee_list = list (skill_profiles["name"])


# %%
skill_matrix = pd.DataFrame(index=employee_list, columns=skill_list)

#%%
skill_lookup = dict(zip(skills_df.preferredLabel, skills_df.conceptUri))
with open ("./Data/skill_lookup.json", "w") as write_file:
    json.dump(skill_lookup, write_file)


# %%
for index, employee_data in skill_profiles.iterrows():
    for skill in employee_data["skills"]:
        skill_matrix.at[employee_data["name"], skill_lookup[skill]] = 1

#%%
# For some reason, the employee skill matrix has more skills then the relation matrix
# There is probably due to faulty data
# To fix this, we can compare the columns and drop all skills which are not present in the skill matrix from the employee one.

to_be_dropped = list(skill_matrix.columns.difference(relation_matrix.columns))
skill_matrix = skill_matrix.drop(to_be_dropped, axis=1)

# %%
skill_matrix = skill_matrix.fillna(0)
pd.to_pickle(skill_matrix, "./Data/employee_skill_matrix.pkl")
# %%
