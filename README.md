
# FPL Threat & Team Analyzer


#### Video Demo: [Click here](https://youtu.be/VTOkxwiIpOg)
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
## 🧼 Python Synopsis

- Use `fpl_player_id_finder.py` to find IDs for new transfers or scouting, this will help you to develop the Team ID `txt` files
- Run `fpl_threat.py` weekly to catch rising stars and avoid rank threats.
- Use `fpl_team.py` to audit your squad and identify dead weight.
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

### 3. Run the fpl_player_id_finder.py
Before preparing your team files, use the `fpl_player_id_finder.py` script to look up FPL player IDs by name. This helps you build two critical lists:

- `team_players_id.txt`: Players you currently own
- `exclude_players_id.txt`: Players you want to avoid or exclude from threat analysis

#### 🔍 How to use the ID Finder

Run the script:
```bash
python3 fpl_player_id_finder.py
```

```bash
Enter player name to search: Gabriel

Player Name  Player Code  Team Code  Match Score
Gabriel            5          1          100
```
Maybe, Add This `5` as Gabriels Player ID, into your desired section of `txt`. Either in `exclude_players_id.txt` or `team_player_id.txt`

Repeat the porcess, untill you have all your desired team & exculiton list ready.

### 4. Prepare Your Team Files
Once you've identified player IDs - Create `team_players_id.txt` with one ID per line for players you own. Similarly, Create `exclude_players_id.txt` with one ID per line for players you want to ignore

Example: `team_players_id.txt`
```json
11
23
45
666
```

Example: `exclude_players_id.txt`
```json
575
427
21
```
#### ❌ Why exclude players?
FPL has team-based constraints and strategic considerations. You may want to exclude players from threat analysis for reasons like:

> **Team quota limits -** 
FPL only allows 3 players per club. If you already own Salah, Van Dijk, and Gakpo from Liverpool, you must exclude Ekitike even if he's performing well. 

> **Rotation risk-**
Players like Trossard or Alvarez may score well but aren't guaranteed starters.

> **Injury or suspension-**
Temporarily exclude players recovering from injury (e.g., Reece James).

> **Personal strategy-**
You may avoid high-ownership players to chase differential gains.

#### **🧪 Example exclusions**
_Player	Reason for exclusion
Ekitike	Not top 3 from Liverpool; already own Salah, Van Dijk, Gakpo
Alvarez	Rotation risk with Haaland; minutes not guaranteed
Reece James	Injury-prone; unreliable availability
Gyökeres	Owned already; don't want him flagged as a threat 
Use these examples to guide your own exclusion logic._

### 5. Run the Scripts
```python
python3 fpl_threat.py
```

```python
python3 fpl_team.py
```


## 🧠 Scripts Overview

### `fpl_threat.py`

Identifies high-performing players **not in your team** and tags them based on:

- High PPG and PxGLx
- Ownership risk (e.g. >20% = "Rank Killer")
- Recent form (PxGLx > 1.5)
- Position-specific thresholds

Output is copied to clipboard and printed in terminal.
Specially look for the **😈 Rank Killer** who are likely hurting your rank with consistency & high owerneship among other palyers overall.

### `fpl_team.py`

Analyzes your current team (from `team_players_id.txt`) and tags each player as:

- 👑 Star Performer
- 🪦 Fodder
- 🤡 Underperformer
- ☠️ High Ownership
- 🦄 Unclassified

Also includes recent form ratio (`L5GW`) and performance emojis.
Keep and Eye on the **🤡 Underperformer** who are potentially hurting your rank unless they are a **🪦 Fodder**.


#### 🧠 Emoji Guide

| Emoji           | Meaning                                                                 |
|-----------------|-------------------------------------------------------------------------|
| 😈 Rank Killer   | High PxG + High Ownership — dangerous if you don’t own                 |
| 🔪 Rank Threat   | Strong performer with growing ownership                                |
| 👨🏼‍🎤 Rising Star | Low ownership but high recent form — potential differential            |
| 👑 Star Performer| Your own player performing above expectations                          |
| 🪦 Fodder        | Cheap player with low output — may be dead weight                      |
| 🤡 Underperformer| Owned player not delivering returns                                    |
| ☠️ High Ownership| Popular pick with low form — risky to follow crowd                     |
| △ / ▽ / ☠︎       | Recent form trend: hot / steady / cold                                 |


### `fpl_player_id_finder.py`

Search tool to find FPL player IDs by name:

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
```


---

## 📣 Credits

Built by Rifatul Maksud — for CS50 & FPL managers who want data-driven insights, emoji-powered tagging, and clipboard-ready output. Data Driven & Clutter Free.

---
