#%%
import pandas as pd
import numpy as np

#%%
occupations_df = pd.read_csv("./Data/occupations_en.csv")
occupations_df = occupations_df.drop(["conceptType", "iscoGroup", "altLabels", "hiddenLabels", "status", "modifiedDate", "scopeNote", "definition", "inScheme"], axis=1) 

#%%
skills_df = pd.read_csv("./Data/skills_en.csv")
skills_df = skills_df.drop(["conceptType", "skillType", "reuseLevel", "altLabels", "hiddenLabels", "status", "modifiedDate", "scopeNote", "definition", "inScheme"], axis=1) 

# %%
relations_df = pd.read_csv("./Data/occupationSkillRelations.csv")
relations_df = relations_df.drop(["relationType", "skillType"], axis=1)

# %%
def clean_url (x):
    return x[-36:]

#%%
occupations_df["conceptUri"] = occupations_df["conceptUri"].apply(clean_url)
skills_df["conceptUri"] = skills_df["conceptUri"].apply(clean_url)
relations_df["occupationUri"] = relations_df["occupationUri"].apply(clean_url)
relations_df["skillUri"] = relations_df["skillUri"].apply(clean_url)

# %%
pd.to_pickle(occupations_df, "./Data/occupations.pkl")
pd.to_pickle(skills_df, "./Data/skills.pkl")
pd.to_pickle(relations_df, "./Data/relations.pkl")

# %%
occupation_df_test = occupations_df.head(10)

# %%
