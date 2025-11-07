from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

path_to_data_dir = BASE_DIR / "data"

path_to_raw_data = path_to_data_dir / "raw_data_players_2023.csv"
path_to_results = path_to_data_dir / "top_players.csv"
