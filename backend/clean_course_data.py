import pandas as pd

# Read the CSV file
data = pd.read_csv('../database/university_of_michigan/fall2023.csv')
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# Remove irrelevant columns
data = data.drop(['Term', 'Session', 'Codes', 'S', 'SU'], axis=1)
print('\nRemoved Irrelevant Columns')

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
