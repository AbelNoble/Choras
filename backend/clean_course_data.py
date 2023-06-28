import pandas as pd

# Read the CSV file
data = pd.read_csv('class_information.csv')

# Remove irrelevant columns
data = data.drop(['code'], axis=1)

# Map abbreviated days to full names
days_mapping = {
    'M': 'Monday',
    'T': 'Tuesday',
    'W': 'Wednesday',
    'TH': 'Thursday',
    'F': 'Friday'
}

# Create 'days_of_week' column
day_columns = ['M', 'T', 'W', 'TH', 'F']
data['days_of_week'] = data[day_columns].apply(
    lambda x: ', '.join(days_mapping[day] for day in x.dropna()), axis=1
)

# Drop the individual day columns
data = data.drop(day_columns, axis=1)

# Extract catalog number
data['catalog_number'] = data['class_number'].apply(lambda x: x.split('-')[0])

# Move catalog number to the beginning
cols = list(data.columns)
cols = ['catalog_number'] + [col for col in cols if col != 'catalog_number']
data = data[cols]

# Write cleaned data to a new CSV file
data.to_csv('cleaned_class_information.csv', index=False)
