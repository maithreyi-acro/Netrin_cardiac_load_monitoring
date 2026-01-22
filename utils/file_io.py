import os
import zipfile
import pandas as pd
from datetime import datetime

def load_zip_file(zip_path):
    return zipfile.ZipFile(zip_path, 'r')

def get_hr_files_from_zip(zip_obj):
    return [f for f in zip_obj.namelist() if f.lower().endswith("hr.csv")]

def load_athlete_metadata(zip_obj):
    try:
        if 'summary.csv' in zip_obj.namelist():
            with zip_obj.open('summary.csv') as f:
                df = pd.read_csv(f)
                
            # Extract weight and age
            weight = None
            age = None
            
            if 'weight' in df.columns:
                weight = float(df['weight'].iloc[0])
            
            if 'date_of_birth' in df.columns:
                dob_str = str(df['date_of_birth'].iloc[0])
                try:
                    dob = datetime.strptime(dob_str, '%Y-%m-%d')
                    age = (datetime.now() - dob).days // 365
                except:
                    age = None
                    
            return {'weight': weight, 'age': age}
    except Exception as e:
        print(f"Warning: Could not load athlete metadata: {e}")
        return None

def save_summary(summary_df, output_path):
    summary_df.to_csv(output_path, index=False)
    print(f"Summary saved to {output_path}")

def ensure_dir(directory):
    os.makedirs(directory, exist_ok=True)
