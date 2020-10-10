#%%
import pandas as pd
import numpy as np

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
