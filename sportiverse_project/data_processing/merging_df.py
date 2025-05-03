import pandas as pd

def merging_dataframe(clean_sb_nation_df, clean_spin_ph_df):
    merged_df = pd.concat([clean_sb_nation_df, clean_spin_ph_df], ignore_index=True)
    # Convert DATE_PUBLISHED to datetime and format as "Month Day, Year"
    merged_df['DATE_PUBLISHED'] = pd.to_datetime(merged_df['DATE_PUBLISHED'], errors='coerce')
    merged_df['DATE_PUBLISHED'] = merged_df['DATE_PUBLISHED'].dt.strftime('%B %d, %Y')
    
    # Drop rows with invalid dates (if any conversion failed)
    merged_df = merged_df.dropna(subset=['DATE_PUBLISHED'])
    
    # Create temporary datetime column for accurate sorting
    merged_df['_SORT_DATE'] = pd.to_datetime(merged_df['DATE_PUBLISHED'], format='%B %d, %Y')
    
    # Sort by the temporary datetime column
    merged_df = merged_df.sort_values('_SORT_DATE', ascending=False)
    
    # Remove the temporary column before saving
    merged_df = merged_df.drop(columns=['_SORT_DATE'])

    return merged_df