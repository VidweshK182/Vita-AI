import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# load and preprocess the
def load_health_logs(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'])
    df.sort_values('date', inplace=True)
    return df

# trainfor mood prediction---1
# rule-based hydration check---2
# rule-based sleep check---3
# rule-based steps check---4
# ml-based mood insight---5

def train_mood_model(df):
    le = LabelEncoder()
    df['mood_encoded'] = le.fit_transform(df['mood'])

    X = df[['sleep_hours', 'hydration_ml', 'steps']]
    y = df['mood_encoded']

    model = LogisticRegression()
    model.fit(X, y)
    return model, le


def analyze_hydration(df):
    if 'hydration_ml' not in df.columns:
        return "⚠️ 'hydration_ml' column missing. Hydration analysis skipped."
    low_hydration_days = df[df['hydration_ml'] < 2200]
    print("****** low hydrate : " , len(low_hydration_days))
    print()
    if len(low_hydration_days) >= 5:
        return "🚱 You've been underhydrated for 5 days straight! Your body needs more fluids urgently."
    elif len(low_hydration_days) == 4:
        return "⚠️ You've had 4 days of low water intake. Time to focus on staying hydrated!"
    elif len(low_hydration_days) == 3:
        return "🚰 Your hydration has been low for 3 or more days. Increase water intake."
    elif len(low_hydration_days) == 2:
        return "💧 You’ve had low hydration for 2 days. Try to drink more water today."
    elif len(low_hydration_days) == 1:
        return "🫗 Yesterday’s water intake was low. Stay hydrated today!"
    else:
        return None


def analyze_sleep(df):
    if 'sleep_hours' not in df.columns:
        return "⚠️ 'sleep_hours' column missing. Sleep analysis skipped."
    low_sleep_days = df[df['sleep_hours'] < 6]
    print("_____************",len(low_sleep_days))
    if len(low_sleep_days) >= 5:
        return "🛌 You've been sleep-deprived for 5 days in a row! Prioritize proper rest to recover."
    elif len(low_sleep_days) == 4:
        return "⚠️ Four days of poor sleep detected. Make time for rest before it impacts your health."
    elif len(low_sleep_days) == 3:
        return "😴 Your sleep has been below 6 hours for multiple days. Aim for 7–8 hours of rest."
    elif len(low_sleep_days) == 2:
        return "⏰ Two days of low sleep logged. Try to wind down earlier tonight."
    elif len(low_sleep_days) == 1:
        return "🫣 You didn’t get enough sleep yesterday. Rest well tonight!"
    else:
        return None


def analyze_steps(df):
    if 'steps' not in df.columns:
        return "⚠️ 'steps' column missing. Steps analysis skipped."
    avg_steps = df['steps'].mean()
    if avg_steps < 3000:
        return f"🛑 Your average steps ({int(avg_steps)}) are very low. Try taking short walks throughout the day to stay active."
    elif avg_steps < 5000:
        return f"🚶‍♂️ Your average steps ({int(avg_steps)}) are lower than the healthy range. Try to stay more active."
    elif avg_steps < 8000:
        return f"🚶‍♀️ You're getting some movement with {int(avg_steps)} steps daily. A little more effort can put you in the optimal range!"
    elif avg_steps < 10000:
        return f"👏 Great job! You're averaging {int(avg_steps)} steps. Keep going to hit the ideal target!"
    else:
        return f"🏃‍♂️ Fantastic! {int(avg_steps)} steps a day puts you in top shape. Stay consistent!"


def analyze_mood_with_ml(df, model, le):
    if model is None or le is None:
        return "⚠️ Mood prediction skipped due to missing required columns."
    features = [col for col in ['sleep_hours', 'hydration_ml', 'steps'] if col in df.columns]
    if not features:
        return "⚠️ Insufficient features for mood prediction."
    df['predicted_mood'] = le.inverse_transform(model.predict(df[features]))
    sad_days = df[df['predicted_mood'] == 'sad']
    if len(sad_days) >= 5:
        return "💔 You’ve reported feeling low for 5 days. It might be time to talk to someone or take a mental health break."
    elif len(sad_days) == 4:
        return "😟 You've had 4 down days recently. Try practicing self-care, connecting with loved ones, or reflecting on stressors."
    elif len(sad_days) == 3:
        return "🧠 Mood patterns suggest fatigue or stress. Consider self-care, better sleep, and hydration."
    elif len(sad_days) == 2:
        return "🙁 Noticing a dip in mood the last 2 days. Take time for yourself and do something that brings you joy."
    elif len(sad_days) == 1:
        return "😕 You logged a sad mood recently. Keep an eye on how you're feeling—it's okay to take a break."
    else:
        return None

# combined engine
def generate_combined_insights(df):
    insights = []

    model, le = train_mood_model(df)

    
    for fn in [analyze_hydration, analyze_sleep, analyze_steps]:
        msg = fn(df)
        if msg:
            insights.append(msg)

    mood_msg = analyze_mood_with_ml(df, model, le)
    if mood_msg:
        insights.append(mood_msg)

    return insights

