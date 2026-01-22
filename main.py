import os
import pandas as pd
from utils import load_zip_file, get_hr_files_from_zip, load_athlete_metadata, save_summary, ensure_dir
from pipeline import summarize_session, compute_acwr

# --- Configuration ---
from config.settings import RAW_DATA_DIR
PROCESSED_DATA_DIR = os.path.join("bin", "processed")

def main():
    ensure_dir(PROCESSED_DATA_DIR)
    
    summary_data = []
    
    # Find zip files in raw folder
    if not os.path.exists(RAW_DATA_DIR):
        print(f"Directory {RAW_DATA_DIR} does not exist. Please create it and add zip files.")
        return

    zip_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.zip')]
    if not zip_files:
        print(f"No zip files found in {RAW_DATA_DIR}")
        return

    for zip_filename in zip_files:
        athlete_name = zip_filename.replace('.zip', '')
        zip_path = os.path.join(RAW_DATA_DIR, zip_filename)
        print(f"Processing athlete: {athlete_name}...")
        
        # Load zip file
        zip_obj = load_zip_file(zip_path)
        
        # Load athlete metadata
        athlete_meta = load_athlete_metadata(zip_obj)
        weight = athlete_meta['weight'] if athlete_meta else None
        age = athlete_meta['age'] if athlete_meta else None
        
        if weight:
            print(f"  Using athlete weight: {weight} kg")
        if age:
            print(f"  Using athlete age: {age} years")
        
        # Get HR files
        hr_files = get_hr_files_from_zip(zip_obj)
        
        summary_data = []
        for hr_file in hr_files:
            session_name = os.path.basename(os.path.dirname(hr_file)) or os.path.basename(hr_file).split('.')[0]
            print(f"  Session: {session_name}")
            
            try:
                with zip_obj.open(hr_file) as f:
                    df = pd.read_csv(f)
                
                # Compute metrics
                metrics = summarize_session(df.reset_index(drop=True), session_name, PROCESSED_DATA_DIR, weight, age)
                if metrics:
                    summary_data.append(metrics)
                    
            except Exception as e:
                print(f"    Error processing {session_name}: {e}")

        # Save summary and compute ACWR for this athlete
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            summary_df = summary_df.sort_values('session')
            
            # Compute ACWR
            summary_df = compute_acwr(summary_df)

            # Save summary file named after the athlete
            summary_file = os.path.join(PROCESSED_DATA_DIR, f"hr_summary_{athlete_name}.csv")
            save_summary(summary_df, summary_file)
            print(f"  Successfully saved summary to {summary_file}")
        else:
            print(f"  No valid sessions found for {athlete_name}")

if __name__ == "__main__":
    main()
