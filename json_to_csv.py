import pandas as pd

# Load the JSON data from a file
json_file_path = 'output/output.jl'

# check that the file exists
try:
    open(json_file_path)
except FileNotFoundError:
    print(f"File {json_file_path} not found.")
    exit()


data = pd.read_json(json_file_path, lines=True)


# Convert the JSON data to a DataFrame
df = pd.DataFrame(data)

# Specify the output CSV file path
csv_file_path = 'output/output.csv'

# Save the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)

print("JSON file converted to CSV successfully!")