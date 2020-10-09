For the project we give you 4 UFT-8 encoded text files containing data in a structured format.
All files are in tab separated format (but we chose the .csv ending, since it is well known compared to .tsv)
Fields that contain comma separated lists are wrapped in quoted brackets and with doublequotes around each element, for example "[""X"",""Y"",""Z""]"

Content:
An ontology containing thousands of skills, occupations and the relationships between them. Specifically, you will find the following files from the ESCO classification of the European Commission. You find addional info on their website https://ec.europa.eu/esco/portal/skill
“skills_en.csv”: list of all skills available in the English dataset.
--> conceptType: (can be ignored)
--> conceptUri: Skill URI to the ESCO dataset used as unique identifier.
--> skillType: (can be ignored)
--> reuseLevel: (can be ignored)
--> preferredLabel: Preferred label of the skill.
--> altLabels: (can be ignored)
--> hiddenLabels: (can be ignored)
--> status: (can be ignored)
--> modifiedDate: (can be ignored)
--> scopeNote: (can be ignored)
--> definition: (can be ignored)
--> inScheme: (can be ignored)
--> description: (can be ignored)


“occupations_en.csv”:  list of all occupations available in the English dataset.
--> conceptType: (can be ignored)
--> conceptUri: Occupation URI to the ESCO dataset used as unique identifier.
--> iscoGroup: (can be ignored)
--> preferredLabel:Preferred label of the occupation.
--> altLabels: (can be ignored)
--> hiddenLabels: (can be ignored)
--> status: (can be ignored)
--> modifiedDate: (can be ignored)
--> regulatedProfessionNote: (can be ignored)
--> scopeNote: (can be ignored)
--> definition: (can be ignored)
--> inScheme: (can be ignored)
--> description: (can be ignored)

“occupationSkillRelations.csv”: each entry in this file corresponds to an association between an occupation and a skill, which is important to have for the occupation.
--> occupationUri: Occupation URI to the ESCO dataset.
--> relationType: (can be ignored)
--> skillType: (can be ignored)
--> skillUri: Skill URI to the ESCO dataset.


A file containing the persons and their skills/knowledge/competence, for which you will recommend positions.
“skill_profiles.csv”: this file contains a list of people and their top 15 skills. It has an id field, the person's name, and a list of their top skills.
the skills correspond to the preferredLabel from the skills_en.csv



