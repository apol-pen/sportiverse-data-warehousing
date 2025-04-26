import pandas as pd
from datetime import datetime

def standardize_date_format(df, source):
    def convert_sbn_date(date):
        try:
            return datetime.strptime(date, "%B %d").replace(year=datetime.now().year).date()
        except:
            return None

    def convert_spinph_date(date):
        try:
            date = date.strip().upper()
            if "JUST NOW" in date:
                return datetime.now().date()
            elif "MINUTE" in date:
                minutes_ago = int(date.split()[0]) 
                return (datetime.now() - pd.Timedelta(minutes=minutes_ago)).date()
            elif "HOUR" in date:
                hours_ago = int(date.split()[0]) 
                return (datetime.now() - pd.Timedelta(hours=hours_ago)).date()
            elif "DAY" in date:
                if date == "A DAY AGO":
                    days_ago = 1
                else:
                    days_ago = int(date.split()[0]) 
                return (datetime.now() - pd.Timedelta(days=days_ago)).date()
            return datetime.now().date() 
        except Exception as e:
            print(f"Error processing date: {date} - {e}")
            return None
    if source == "SB Nation":
        df['DATE_PUBLISHED'] = df['DATE_PUBLISHED'].apply(convert_sbn_date)
    else:
        df['DATE_PUBLISHED'] = df['DATE_PUBLISHED'].apply(convert_spinph_date)

    return df
