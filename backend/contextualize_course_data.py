import pandas as pd

# Read the cleaned CSV file
data = pd.read_csv('../database/university_of_michigan/cleaned_fall2023.csv')

# Open the output Python file for writing
output_path = '../database/university_of_michigan/text_fall2023.txt'
with open(output_path, 'w') as file:
    # Iterate over each row in the DataFrame
    for _, row in data.iterrows():
        # Generate the prompt sentence for the current row
        prompt = f'This class is a {row["Component"]} component of the course{row["Catalog Nbr"]} with a class number {row["Class Nbr"]}. It is section {row["Section"]} of the class titled "{row["Course Title"]}" ' \
                 f'belonging to the {row["Acad Group"]} academic group about the subject of {row["Subject"]}. The class is scheduled on the day(s) {row["Days"]} at the time {row["Time"]} and will be held in room {row["Location"]}. ' \
                 f'The instructor for this class is {row["Instructor"]}. It is a {row["Units"]} unit course and will run for the duration of the {row["Class Duration"]}.\n'

        # Write the prompt to the Python file
        file.write(prompt)

print("Prompts created and saved")
