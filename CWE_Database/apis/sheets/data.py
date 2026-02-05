import os
import pandas as pd

def consolidate_titles(directory=".", output_file="all_titles.csv"):
    extensions = ('.csv', '.xlsx', '.xls')
    all_extracted_data = []

    print("Searching for 'Title' columns...")

    for filename in os.listdir(directory):
        if filename.endswith(extensions) and filename != output_file:
            file_path = os.path.join(directory, filename)
            
            try:
                # Load the file
                if filename.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                
                # Normalize column names (removes accidental spaces and capitalization issues)
                df.columns = [str(col).strip().capitalize() for col in df.columns]

                if 'Title' in df.columns:
                    # Extract the Title column and track which file it came from
                    titles = df['Title'].dropna().unique().tolist()
                    for t in titles:
                        all_extracted_data.append({'Source_File': filename, 'Title': t})
                    print(f"✅ Extracted from: {filename}")
                else:
                    print(f"❌ 'Title' column not found in: {filename}")
                
            except Exception as e:
                print(f"⚠️ Error processing {filename}: {e}")

    # Save to a new CSV
    if all_extracted_data:
        output_df = pd.DataFrame(all_extracted_data)
        output_df.to_csv(output_file, index=False)
        print(f"\n✨ Success! All titles saved to: {output_file}")
    else:
        print("\nNo 'Title' columns were found in any files.")

if __name__ == "__main__":
    consolidate_titles()