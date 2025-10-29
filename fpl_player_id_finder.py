import requests
import pandas as pd
from fuzzywuzzy import process

# 📦 Fetch all player data from FPL API
def fetch_all_players():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json()['elements'])

# 🔍 Find player ID by approximate name
def find_player_ids_by_name(search_name, threshold=80, limit=10):
    df_players = fetch_all_players()
    df_players['web_name_lower'] = df_players['web_name'].str.lower()
    player_names = df_players['web_name_lower'].dropna().tolist()

    matches = process.extract(search_name.lower(), player_names, limit=limit)
    filtered_matches = [match for match in matches if match[1] >= threshold]

    results = []
    for name, score in filtered_matches:
        matched_rows = df_players[df_players['web_name_lower'] == name]
        for _, row in matched_rows.iterrows():
            results.append({
                'Player Name': row['web_name'],
                'Player Code': row['id'],
                'Team Code': row['team'],
                'Match Score': score
            })

    return pd.DataFrame(results)

# 🚀 Prompt user for input
if __name__ == "__main__":
    search_term = input("🔍 Enter player name to search: ").strip()
    if search_term:
        matched_players = find_player_ids_by_name(search_term)
        if not matched_players.empty:
            print("\n✅ Matched Players:")
            print(matched_players)
        else:
            print("⚠️ No matches found above threshold.")
    else:
        print("⚠️ No input provided.")
