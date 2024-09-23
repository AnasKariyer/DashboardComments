from pathlib import Path
import pandas as pd

# Set the application directory
app_dir = Path(__file__).parent

# Load the Excel file into a pandas DataFrame
file_path = app_dir / "Translated_Negative_Reviews.xlsx"
translated_negative_reviews = pd.read_excel(file_path)