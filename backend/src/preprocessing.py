import pandas as pd
import re
import os

# loading dataset
df  = pd.read_csv("../data/raw/Job_Postings_US new.csv")

# inspect basic info
# df.shape is the number of rows, columns
print(df.shape)
# df.columns is all the column names
print(df.columns)
# df.head() is the first 10 rows, we use 5 to say we only want first 5
print(df.head(5))

# checking for missing values
print(df.isnull().sum())

# select relevant fields 
df = df[['job_posted_date', 'company_address_locality', 'company_name', 'company_description', 'job_description_text', 'seniority_level', 'job_title']]

# add a new field, visa_sponsorship
df['visa_sponsorship'] = 'Unknown'

# preview new dataframe
print(df.head(5))

# keyword-based filter
# set our keywords_yes and keywords_no
visa_keywords_yes = ['h1-b', 'h1b', 'visa sponsorship',
                     'sponsorship available', 'work visa', 'opt', 'cpt',
                     'stem opt', 'sponsorship']

visa_keywords_no = ['must be authorized to work in the us', 'no sponsorship',
                    'without sposorship', 'not sponsor', 'usc or gc only', 
                    'citizens only', 'green card only']

# combining company description and job description for future use with searching for keywords
df['job_text'] = df[['company_description', 'job_description_text']].astype(str).agg(' '.join, axis=1)

def check_sponsorship(text):
    '''Return Yes/No/Unkown based on keywords in job description'''
    if pd.isnull(text):
        return "Unknown"
    
    # set text to lower to match out keywords
    text = text.lower()

    if any(keyword in text for keyword in visa_keywords_yes):
        return 'Yes'
    elif any(keyword in text for keyword in visa_keywords_no):
        return 'No'
    else:
        'Unknown'

def add_visa_column(df: pd.DataFrame) -> pd.DataFrame:
    df['visa_sponsorship'] = df['job_text'].apply(check_sponsorship)
    print(df[['job_title', 'company_name', 'visa_sponsorship']].head(10))
    df.to_csv("../data/processed/job_postings_us_with_visa.csv", index=False)
    return df

df = add_visa_column(df)
print("Processing done. Check processed folder in data folder.")