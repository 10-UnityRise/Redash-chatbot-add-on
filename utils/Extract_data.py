import os
import zipfile

# Path to the folder containing .zip files
folder_path = "../youtube-data"

# Output directory to extract .csv files
output_directory = "../data"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Iterate through each .zip file in the folder
for zip_file_name in os.listdir(folder_path):
    if zip_file_name.endswith(".zip"):
        zip_file_path = os.path.join(folder_path, zip_file_name)

        # Create a subdirectory for each .zip file
        output_subdirectory = os.path.join(output_directory, zip_file_name[:-4])
        os.makedirs(output_subdirectory, exist_ok=True)

        # Extract .csv files from the current .zip file to the subdirectory
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_subdirectory)

print("Extraction completed successfully.")

