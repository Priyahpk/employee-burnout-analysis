import pandas as pd

def load_data():
    df = pd.read_csv(r"C:\Users\Haripriya Kumaresh\Downloads\Palo Alto Networks.csv")
    return df

def preprocess(df):
    df['OverTime'] = df['OverTime'].map({'Yes': 1, 'No': 0})
    return df

def create_engagement_index(df):
    df['EngagementIndex'] = (
        df['JobInvolvement'] +
        df['JobSatisfaction'] +
        df['EnvironmentSatisfaction'] +
        df['RelationshipSatisfaction']
    ) / 4
    return df

def create_burnout_risk(df):
    def risk(row):
        if row['OverTime'] == 1 and row['WorkLifeBalance'] <= 2:
            return 'High'
        elif row['OverTime'] == 1 or row['WorkLifeBalance'] <= 2:
            return 'Medium'
        else:
            return 'Low'

    df['BurnoutRisk'] = df.apply(risk, axis=1)
    return df