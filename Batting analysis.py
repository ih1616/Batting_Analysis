import datetime
from pybaseball import playerid_lookup, statcast_batter, spraychart
from sportypy.surfaces.baseball import BaseballField

# Function to get player ID
def get_player_id(last_name, first_name):
    players = playerid_lookup(last_name, first_name)
    if players.empty:
        return None
    player_id = players.iloc[0]['key_mlbam']
    return player_id

# Function to get batter data
def get_batter_data(player_id, start_date, end_date):
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    data = statcast_batter(start_date_str, end_date_str, player_id)
    return data

# Function to preprocess data
def preprocess_data(data):
    columns_to_keep = ['pitch_type', 'launch_speed', 'launch_angle', 'hc_x', 'hc_y', 'events', 'game_date']
    data = data[columns_to_keep].copy()  # Use .copy() to avoid SettingWithCopyWarning
    data.dropna(inplace=True)
    return data

def plot_player_spraychart(data, team_stadium, title):
    # Create a baseball field
    field = BaseballField(league_code='MLB')

    # Plot spraychart using pybaseball's spraychart function
    spraychart(data, team_stadium, title=title,)

# Function to analyze hitting effectiveness
def analyze_hitting_effectiveness(data):
    hit_summary = data.groupby('events').agg({
        'launch_speed': ['mean', 'std'],
        'launch_angle': ['mean', 'std']
    }).reset_index()
    hit_summary.columns = ['events', 'avg_launch_speed', 'launch_speed_std', 'avg_launch_angle', 'launch_angle_std']
    return hit_summary

def main():
    last_name = input("Enter player's last name: ").strip().title()
    first_name = input("Enter player's first name: ").strip().title()

    while True:
        try:
            start_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date_str = input("Enter end date (YYYY-MM-DD): ").strip()
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
            continue

    player_id = get_player_id(last_name, first_name)
    if player_id is None:
        print("Player not found. Please check the name and try again.")
        return

    data = get_batter_data(player_id, start_date, end_date)
    cleaned_data = preprocess_data(data)
    print("Batter Data:\n", cleaned_data.head())
    effectiveness = analyze_hitting_effectiveness(cleaned_data)
    print("Hitting Effectiveness:\n", effectiveness)

    # Save the cleaned data to CSV
    cleaned_data_filename = f"{first_name}_{last_name}_cleaned_data.csv"
    cleaned_data.to_csv(cleaned_data_filename, index=False)
    print(f"Cleaned data saved to {cleaned_data_filename}")

    # Save the hitting effectiveness to CSV
    effectiveness_filename = f"{first_name}_{last_name}_hitting_effectiveness.csv"
    effectiveness.to_csv(effectiveness_filename, index=False)
    print(f"Hitting effectiveness data saved to {effectiveness_filename}")


    # Adjust team_stadium based on the player's team, assuming the player is with the Los Angeles Angels
    team_stadium = 'angels'  # Adjust based on actual team if known

    title = f"Spray Chart for {first_name} {last_name} ({start_date_str} to {end_date_str})"
    plot_player_spraychart(data, team_stadium, title)


if __name__ == "__main__":
    main()
