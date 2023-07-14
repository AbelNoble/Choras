import pandas as pd
import re

# Read the CSV file
data = pd.read_csv('../database/university_of_michigan/fall2023.csv')
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# Remove irrelevant columns
data = data.drop(['Term', 'Session', 'Codes', 'S', 'SU'], axis=1)
print('\nRemoved Irrelevant Columns')

# Change the Session and Date so that to determine regular or partial semester
data['Class Duration'] = data.apply(
    lambda row: 'Full Term' if row['Start Date'] == '08/28/2023' and row['End Date'] == '12/06/2023' else 'Partial Term',
    axis=1
)
data = data.drop(['Start Date', 'End Date'], axis=1)
print('\nChanged Duration to Full or Partial')

# Create new days column
days_mapping = {
    'M': 'Monday',
    'T': 'Tuesday',
    'W': 'Wednesday',
    'TH': 'Thursday',
    'F': 'Friday'
}
day_columns = ['M', 'T', 'W', 'TH', 'F']
data.insert(12, 'Days', data[day_columns].apply(
    lambda x: ', '.join(days_mapping[day] for day in x.dropna()), axis=1
))
data = data.drop(day_columns, axis=1)
print('\nInserted New Days Column')

# Substitute "not available" for null values in the Days column
data['Days'] = data['Days'].replace('', 'not available')
print('\nUpdated Days Info')

# Expanded components and removed clinical experience classes
component_mapping = {
    'LAB': 'Lab',
    'LEC': 'Lecture',
    'SEM': 'Seminar',
    'DIS': 'Discussion',
    'REC': 'Recitation',
    'IND': 'Individual Instruction'
}
data['Component'] = data['Component'].map(component_mapping)
data = data[data['Component'] != 'CLN']
data = data[data['Component'].notna()]
print('\nInserted New Component Column')

# Change location if it is "ARR" to "To be determined"
data.loc[data['Location'] == 'ARR', 'Location'] = 'to be determined'
print('\nChanged Location for ARR classes')

# Change subject so that it does not contain shortened version
data['Subject'] = data['Subject'].apply(lambda x: re.sub(r'\(.*\)', '', x).strip())
print('\nRemoved shortened subject form')

# Substitute "not available" for null values in the "Instructor" column
data['Instructor'] = data['Instructor'].fillna('not available')
data['Instructor'] = data['Instructor'].apply(lambda x: ', '.join(['Professor ' + name.strip() for name in x.split(',')]) if x != 'not available' else x)
print('\nUpdated Instructor Info')

# Change time if it is "ARR" to "unknown"
data.loc[data['Time'] == 'ARR', 'Time'] = 'unknown'
print('\nChanged Time for ARR classes')

# Move section to 2nd row
cols = list(data.columns)
cols.remove('Section')
cols.insert(0, 'Section')
data = data.reindex(columns=cols)
print('\nMoved Section Column')

# Move catalog number to the beginning
cols = list(data.columns)
cols = ['Catalog Nbr'] + [col for col in cols if col != 'Catalog Nbr']
data = data[cols]
print('\nMoved Catalog Column')

# Write cleaned data to a new CSV file
output_path = '../database/university_of_michigan/cleaned_fall2023.csv'
data.to_csv(output_path, index=False)
print('\nSaved File')
