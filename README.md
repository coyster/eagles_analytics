# Eagles Analytics

A Python analytics tool for analyzing Philadelphia Eagles game statistics.

## Project Structure

```
eagles_analytics/
├── input/                 # Input data files (CSV)
│   └── eagles_game_stats.csv
├── output/                # Generated analytics reports (JSON)
│   └── eagles_analytics_report.json
├── src/                   # Source code
│   ├── __init__.py
│   └── analytics.py       # Main analytics module
└── README.md
```

## Usage

Run the analytics from the project root:

```bash
python src/analytics.py
```

This will:
1. Read game statistics from CSV files in the `input/` folder
2. Calculate various analytics (win/loss record, scoring, offense stats, etc.)
3. Generate a JSON report in the `output/` folder

## Input Format

The input CSV file should contain the following columns:
- `game_id`: Unique game identifier
- `date`: Game date (YYYY-MM-DD)
- `opponent`: Opponent team name
- `home_away`: "home" or "away"
- `points_scored`: Points scored by Eagles
- `points_allowed`: Points allowed
- `rushing_yards`: Total rushing yards
- `passing_yards`: Total passing yards
- `turnovers`: Number of turnovers
- `result`: "W" for win, "L" for loss

## Output

The analytics report includes:
- **Summary**: Win/loss record and win percentage
- **Scoring**: Points scored/allowed averages and point differential
- **Offense**: Rushing, passing, and total yards
- **Turnovers**: Turnover statistics
- **Home/Away**: Home and away records