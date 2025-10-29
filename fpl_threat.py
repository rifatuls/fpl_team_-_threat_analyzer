import requests, pandas as pd, numpy as np, arrow, pyperclip
from datetime import timedelta
import os, warnings

warnings.filterwarnings("ignore", category=UserWarning)


# 📂 Load exclusion lists from TXT files
def load_exclude_ids(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            return [int(line.strip()) for line in f if line.strip().isdigit()]
    except FileNotFoundError:
        print(f"⚠️ File not found: {path}")
        return []

EXCLUDE_IDS_I_HAVE = load_exclude_ids('team_players_id.txt')
EXCLUDE_IDS_I_DONT_WANT = load_exclude_ids('exclude_players_id.txt')
EXCLUDE_IDS = EXCLUDE_IDS_I_HAVE + EXCLUDE_IDS_I_DONT_WANT

# 🔧 Parameters
GAMEWEEKS, LGW, PPG = 8, 5, 3.5
MIN_OWNERSHIP, MIN_PRICE, MAX_PRICE = 7.5, 4.0, 15.0
MIN_POINTS = PPG * GAMEWEEKS
position_map = {1: 'Goalkeeper', 2: 'Defender', 3: 'Midfielder', 4: 'Forward'}

# 📦 Fetch all player data
def fetch_all_players():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json()['elements'])

# 📅 Fetch per-GW history
def fetch_player_history(player_id):
    url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json()['history'])

# 🔥 Last 5 GW average
def get_last_5_gw_avg(player_id):
    df = fetch_player_history(player_id)
    return df.sort_values(by='round', ascending=False).head(LGW)['total_points'].mean()

# 🔍 Filter high performers
def filter_high_performers():
    df = fetch_all_players()
    df['selected_by_percent'] = df['selected_by_percent'].astype(float)
    df['points_per_game'] = df['points_per_game'].astype(float)
    df['now_cost'] = df['now_cost'].astype(float) / 10
    df = df[
        (~df['id'].isin(EXCLUDE_IDS)) &
        (df['selected_by_percent'] >= MIN_OWNERSHIP) &
        (df['total_points'] >= MIN_POINTS) &
        (df['status'] == 'a') &
        (df['points_per_game'] >= PPG) &
        (df['now_cost'].between(MIN_PRICE, MAX_PRICE))
    ]
    return df.sort_values(by='selected_by_percent', ascending=False)

# 🚫 Show excluded players
def show_excluded_names(ids):
    df = fetch_all_players()
    df['now_cost'] = df['now_cost'].astype(float) / 10
    return df[df['id'].isin(ids)]

# 🧩 Combine and label
def prepare_combined_df():
    df_threat = filter_high_performers()
    df_have = show_excluded_names(EXCLUDE_IDS_I_HAVE)
    df_dont = show_excluded_names(EXCLUDE_IDS_I_DONT_WANT)

    for df, label in [(df_threat, 'Threat'), (df_have, 'MadLads'), (df_dont, 'Excluded')]:
        df['label'] = label
        df['position'] = df['element_type'].map(position_map)
        df['Last5GW_PxG'] = df['id'].apply(get_last_5_gw_avg)

    df_all = pd.concat([df_have, df_dont, df_threat], ignore_index=True)
    df_all.rename(columns={
        'id': 'FPL ID', 'label': 'Team', 'web_name': 'Player Name',
        'position': 'Position', 'points_per_game': 'PxG',
        'total_points': 'PTS', 'selected_by_percent': 'Ownership %',
        'now_cost': '£ Price', 'Last5GW_PxG': 'PxGLx'
    }, inplace=True)
    df_all['PxG'] = df_all['PxG'].astype(float)
    df_all['PxGLx'] = df_all['PxGLx'].astype(float)
    df_all['£ Price'] = df_all['£ Price'].astype(float)
    df_all['Ownership %'] = df_all['Ownership %'].astype(float)
    return df_all.sort_values(by='PxG', ascending=False)

# 🏷️ Tagging logic
def tag_player(row):
    if row['Team'] == 'Threat':
        if row['PxG'] > 6 and row['Ownership %'] > 20: return '😈 Rank Killer'
        elif row['PxG'] > 6 and row['Ownership %'] >= 10: return '🔪 Rank Threat'
        elif row['PxG'] > 6 and row['Ownership %'] > 1: return '👨🏼‍🎤 Rising Star'
        elif row['Position'] == 'Goalkeeper' and row['PxG'] > 4.5: return '🥅 Rank Threat'
        elif row['PxG'] >= 5 and row['Ownership %'] >= 10: return '🔪 Rank Threat'
        elif row['Ownership %'] > 25: return '☠️ High Ownership'
        else: return '👨🏼‍🎤 Rising Star'
    elif row['Team'] == 'MadLads':
        if row['PxG'] > 5.5: return '👑 Star Performer'
        elif row['Position'] == 'Goalkeeper' and row['PxG'] > 3.75: return '👑 Star Performer'
        elif row['£ Price'] < 4.7: return '🪦 Fodder'
        elif row['Position'] == 'Midfielder' and row['£ Price'] <= 5.5: return '🪦 Fodder'
        elif row['PxG'] < 4.5: return '🤡 Underperformer'
        elif row['Ownership %'] > 25: return '☠️ High Ownership'
        else: return '🦄 Unclassified'
    else: return '—'

def tag_l5gw_performance(row):
    if row['PxG'] == 0: return '☠︎'
    ratio = row['PxGLx'] / row['PxG']
    if ratio > 1.0: return '△'
    elif row['PxGLx'] < 3.0: return '☠︎'
    elif ratio > 0.70: return '▽'
    else: return '☠︎'

# 🧠 Apply tags and format
def apply_tags(df):
    df['Player Profile'] = df.apply(tag_player, axis=1)
    df['L5GW'] = df.apply(lambda row: f"{row['PxGLx'] / row['PxG']:.2f} {tag_l5gw_performance(row)}" if row['PxG'] != 0 else '0.00 ☠︎', axis=1)
    df['PxG'] = df['PxG'].round(2).astype(str)
    df['PxGLx'] = df['PxGLx'].round(1).astype(str)
    df['£ Price'] = df['£ Price'].map(lambda x: f'£{x:.1f}')
    df['Ownership %'] = df['Ownership %'].map(lambda x: f'{x:.1f}%')
    return df[['FPL ID', 'Team', 'Player Name', 'Position', 'PTS', 'Ownership %', '£ Price', 'PxG', 'PxGLx', 'L5GW', 'Player Profile']]

# 🚀 Run full pipeline
combined_df = prepare_combined_df()
xFPL = combined_df[(combined_df['Team'] == 'Threat') & (combined_df['PxGLx'] >= 4.5)].copy()
xFPL = apply_tags(xFPL)
xFPL.to_clipboard()
print("✅ Threat & MadLads ready for clipboard.")
print(xFPL)