"""
Eagles Analytics - Main analytics module.

This module provides functions to analyze Philadelphia Eagles game statistics
from input CSV files and generate analytics reports in the output folder.
"""

import csv
import json
import os
from pathlib import Path


def read_game_stats(input_path: str) -> list[dict]:
    """
    Read game statistics from a CSV file.

    Args:
        input_path: Path to the input CSV file.

    Returns:
        List of dictionaries containing game statistics.
    """
    games = []
    with open(input_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            game = {
                "game_id": int(row["game_id"]),
                "date": row["date"],
                "opponent": row["opponent"],
                "home_away": row["home_away"],
                "points_scored": int(row["points_scored"]),
                "points_allowed": int(row["points_allowed"]),
                "rushing_yards": int(row["rushing_yards"]),
                "passing_yards": int(row["passing_yards"]),
                "turnovers": int(row["turnovers"]),
                "result": row["result"],
            }
            games.append(game)
    return games


def calculate_analytics(games: list[dict]) -> dict:
    """
    Calculate analytics from game statistics.

    Args:
        games: List of game statistics dictionaries.

    Returns:
        Dictionary containing calculated analytics.
    """
    if not games:
        return {}

    total_games = len(games)
    wins = sum(1 for g in games if g["result"] == "W")
    losses = total_games - wins

    total_points_scored = sum(g["points_scored"] for g in games)
    total_points_allowed = sum(g["points_allowed"] for g in games)
    total_rushing_yards = sum(g["rushing_yards"] for g in games)
    total_passing_yards = sum(g["passing_yards"] for g in games)
    total_turnovers = sum(g["turnovers"] for g in games)

    home_games = [g for g in games if g["home_away"] == "home"]
    away_games = [g for g in games if g["home_away"] == "away"]

    home_wins = sum(1 for g in home_games if g["result"] == "W")
    away_wins = sum(1 for g in away_games if g["result"] == "W")

    analytics = {
        "summary": {
            "total_games": total_games,
            "wins": wins,
            "losses": losses,
            "win_percentage": round(wins / total_games * 100, 1) if total_games > 0 else 0,
        },
        "scoring": {
            "total_points_scored": total_points_scored,
            "total_points_allowed": total_points_allowed,
            "avg_points_scored": round(total_points_scored / total_games, 1),
            "avg_points_allowed": round(total_points_allowed / total_games, 1),
            "point_differential": total_points_scored - total_points_allowed,
        },
        "offense": {
            "total_rushing_yards": total_rushing_yards,
            "total_passing_yards": total_passing_yards,
            "total_yards": total_rushing_yards + total_passing_yards,
            "avg_rushing_yards": round(total_rushing_yards / total_games, 1),
            "avg_passing_yards": round(total_passing_yards / total_games, 1),
            "avg_total_yards": round((total_rushing_yards + total_passing_yards) / total_games, 1),
        },
        "turnovers": {
            "total_turnovers": total_turnovers,
            "avg_turnovers_per_game": round(total_turnovers / total_games, 2),
        },
        "home_away": {
            "home_record": f"{home_wins}-{len(home_games) - home_wins}",
            "away_record": f"{away_wins}-{len(away_games) - away_wins}",
        },
    }

    return analytics


def write_analytics(analytics: dict, output_path: str) -> None:
    """
    Write analytics to a JSON file.

    Args:
        analytics: Dictionary containing calculated analytics.
        output_path: Path to the output JSON file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as jsonfile:
        json.dump(analytics, jsonfile, indent=2)


def run_analytics(input_dir: str, output_dir: str) -> dict:
    """
    Run the full analytics pipeline.

    Reads game statistics from the input directory, calculates analytics,
    and writes the results to the output directory.

    Args:
        input_dir: Path to the input directory containing CSV files.
        output_dir: Path to the output directory for analytics results.

    Returns:
        Dictionary containing the calculated analytics.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Find the game stats CSV file
    csv_files = list(input_path.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return {}

    all_games = []
    for csv_file in csv_files:
        games = read_game_stats(str(csv_file))
        all_games.extend(games)

    analytics = calculate_analytics(all_games)

    # Write analytics to output
    output_file = output_path / "eagles_analytics_report.json"
    write_analytics(analytics, str(output_file))

    print(f"Analytics report generated: {output_file}")
    return analytics


def main():
    """Main entry point for the analytics script."""
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    input_dir = project_root / "input"
    output_dir = project_root / "output"

    print("Eagles Analytics")
    print("=" * 40)

    analytics = run_analytics(str(input_dir), str(output_dir))

    if analytics:
        print("\nSeason Summary:")
        print(f"  Record: {analytics['summary']['wins']}-{analytics['summary']['losses']}")
        print(f"  Win Percentage: {analytics['summary']['win_percentage']}%")
        print(f"\nScoring:")
        print(f"  Avg Points Scored: {analytics['scoring']['avg_points_scored']}")
        print(f"  Avg Points Allowed: {analytics['scoring']['avg_points_allowed']}")
        print(f"  Point Differential: {analytics['scoring']['point_differential']}")
        print(f"\nOffense:")
        print(f"  Avg Total Yards: {analytics['offense']['avg_total_yards']}")
        print(f"\nHome/Away:")
        print(f"  Home Record: {analytics['home_away']['home_record']}")
        print(f"  Away Record: {analytics['home_away']['away_record']}")


if __name__ == "__main__":
    main()
