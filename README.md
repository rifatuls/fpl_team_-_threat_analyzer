
# FPL Threat & Team Analyzer


#### Video Demo: [Click here](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
This project is for CS50x by Mohd. Rifatul Maksud.
A Python-based toolkit for analyzing Fantasy Premier League (FPL) player performance using public API data. It helps identify high-performing players ("Threats") and track your own team ("MadLads") based on customizable metrics like Points Per Game (PPG), recent form, ownership %, and price.


## 📌 Project Structure

```
FPL/
├── fpl_threat.py              # Identifies top-performing players NOT in your team
├── fpl_team.py                # Evaluates your current team (MadLads)
├── fpl_player_id_finder.py    # Fuzzy search for player IDs by name
├── team_players_id.txt        # List of FPL IDs you currently own
├── exclude_players_id.txt     # List of FPL IDs you want to avoid
├── requirements.txt           # Python dependencies
```

---

## 🔍 FPL Hypotheses & Metrics

This toolkit is built around key performance hypotheses:

| Metric         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `PPG`          | Points Per Game — overall average performance indicator                     |
| `PxGLx`        | Last 5 Gameweeks average — recent form proxy (calculated from GW history)   |
| `Ownership %`  | Popularity among FPL managers — used to assess risk and differential value  |
| `£ Price`      | Current player cost — used to identify value picks or overpriced assets     |
| `Team`         | Label assigned: `Threat`, `YouTeam`, or `Excluded`                          |
| `Excluded`     | The players I Don't Like to Have, Irresepctive of Performance               |
| `Player Profile` | Emoji-based tag based on performance, ownership, and price                |
| `L5GW`         | Ratio of PxGLx to PPG, tagged with △ (hot), ▽ (steady), ☠︎ (cold)            |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/fpl-analyzer.git
cd fpl-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare your team files

Create two text files in the same folder:

#### `team_players_id.txt`
List of FPL player IDs you currently own (one per line):

```
2
3
575
500
```

#### `exclude_players_id.txt`
List of FPL player IDs you want to avoid:

```
5
6
666
```

---

## 🧠 Scripts Overview

### `fpl_threat.py`

Identifies high-performing players **not in your team** and tags them based on:

- High PPG and PxGLx
- Ownership risk (e.g. >20% = "Rank Killer")
- Recent form (PxGLx > 1.5)
- Position-specific thresholds

Output is copied to clipboard and printed in terminal.

### `fpl_team.py`

Analyzes your current team (from `team_players_id.txt`) and tags each player as:

- 👑 Star Performer
- 🪦 Fodder
- 🤡 Underperformer
- ☠️ High Ownership
- 🦄 Unclassified

Also includes recent form ratio (`L5GW`) and performance emojis.

### `fpl_player_id_finder.py`

Fuzzy search tool to find FPL player IDs by name:

```bash
python fpl_player_id_finder.py
🔍 Enter player name to search: gyokeres
```

Returns matching players with ID, team code, and match score.

---

## 📋 Output Columns

| Column          | Meaning                                      |
|-----------------|----------------------------------------------|
| `FPL ID`        | Unique player ID used by FPL API             |
| `Team`          | Label: Threat, MadLads, or Excluded          |
| `Player Name`   | Display name                                 |
| `Position`      | Goalkeeper, Defender, Midfielder, Forward    |
| `PTS`           | Total points this season                     |
| `Ownership %`   | Popularity among managers                    |
| `£ Price`       | Current cost in millions                     |
| `PxG`           | Points per Game                              |
| `PxGLx`         | Avg points over last 4 GWs                   |
| `L5GW`          | PxGLx / PxG ratio with emoji tag             |
| `Player Profile`| Emoji-based performance tag                  |

---

## 🧪 Example Hypothesis Tags

- `PxG > 6` and `Ownership > 20%` → 😈 Rank Killer
- `PxGLx / PxG > 1.0` → △ (Hot streak)
- `PxGLx < 3.0` → ☠︎ (Cold streak)
- `Midfielder` and `£ Price < 5.5` → 🪦 Fodder

---

## 🛠️ Requirements

```txt
pandas
requests
arrow
numpy
pyperclip
fuzzywuzzy
python-Levenshtein
```

---

## 🧼 Tips

- Run `fpl_threat.py` weekly to catch rising stars and avoid rank threats.
- Use `fpl_team.py` to audit your squad and identify dead weight.
- Use `fpl_player_id_finder.py` to find IDs for new transfers or scouting, this will help you to develop the Team ID `txt` files

---

## 📣 Credits

Built by Rifatul Maksud — for CS50 & FPL managers who want data-driven insights, emoji-powered tagging, and clipboard-ready output. Data Driven & Clutter Free.

---
