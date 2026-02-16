from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# --- Database Configuration ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Vishnu@2022',  # Replace with your MySQL password
    'database': 'rps_game_db'
}

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**db_config)

# --- Single Player Routes (Unchanged) ---

@app.route('/')
def index():
    return render_template('rps-game.html')

@app.route('/submit', methods=['POST'])
def submit():
    # This route for the single-player game remains unchanged.
    name = request.form.get('player_name', '').strip()
    wins = int(request.form.get('wins', 0))
    losses = int(request.form.get('losses', 0))
    draws = int(request.form.get('draws', 0))
    total_attempts = wins + losses + draws

    try:
        if wins > 0 and total_attempts > 0:
            denominator = total_attempts - (draws / 2)
            score = (wins / denominator) * 100 if denominator != 0 else 0

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT score FROM scores WHERE player_name = %s", (name,))
            existing = cursor.fetchone()

            if existing:
                if score >= existing[0]:
                    cursor.execute("""
                        UPDATE scores SET score=%s, total_atempts=%s, wins=%s, losses=%s, draws=%s 
                        WHERE player_name=%s
                    """, (score, total_attempts, wins, losses, draws, name))
            else:
                cursor.execute("""
                    INSERT INTO scores (player_name, score, total_atempts, wins, losses, draws)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (name, score, total_attempts, wins, losses, draws))
            
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('scores'))
        else:
            return "No wins recorded, score cannot be saved."
    except mysql.connector.Error as err:
        return f"Database error: {err}"
    except ZeroDivisionError:
        return "Invalid score calculation due to division by zero."

@app.route('/scores')
def scores():
    # This route for the single-player scores remains unchanged.
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 10")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('scores.html', scores=rows)

# --- NEW: Two-Player Routes ---

@app.route('/double_player')
def double_player():
    """Renders the two-player game page."""
    return render_template('rps-game2.html')

@app.route('/submit_double', methods=['POST'])
def submit_double():
    """Handles the form submission from the two-player game with the correct formula."""
    p1_name = request.form.get('player1_name', 'Player 1').strip()
    p2_name = request.form.get('player2_name', 'Player 2').strip()
    p1_wins = int(request.form.get('p1_wins', 0))
    p2_wins = int(request.form.get('p2_wins', 0))
    draws = int(request.form.get('draws', 0))
    
    total_attempts = p1_wins + p2_wins + draws

    if total_attempts == 0:
        return "Cannot submit a game with no rounds played."

    # Determine winner and their stats
    if p1_wins > p2_wins:
        winner_name = p1_name
        winner_wins = p1_wins
    elif p2_wins > p1_wins:
        winner_name = p2_name
        winner_wins = p2_wins
    else:
        winner_name = "Draw"
        winner_wins = p1_wins

    # --- CORRECTED SCORE CALCULATION ---
    winner_score = 0
    try:
        # Calculate score using your specified formula
        denominator = total_attempts - (draws / 2)
        if winner_name != "Draw" and denominator > 0:
            # Formula: (wins / (total_attempts - (draws / 2))) * 100
            raw_score = (winner_wins / denominator) * 100
            # Convert the final score to an integer
            winner_score = int(raw_score)
            
    except ZeroDivisionError:
        winner_score = 0
    
    # Insert the game session into the table
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO scores_double_player 
            (player1_name, player2_name, total_attempts, winner_name, player1_wins, player2_wins, winner_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (p1_name, p2_name, total_attempts, winner_name, p1_wins, p2_wins, winner_score)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return f"Database error on saving two-player game: {err}"

    return redirect(url_for('scores_double'))

@app.route('/scores_double')
def scores_double():
    """Displays the leaderboard for two-player games."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Order by score, then by date for tie-breaking
    cursor.execute("SELECT * FROM scores_double_player ORDER BY winner_score DESC, game_date DESC LIMIT 10")
    sessions = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('scores2.html', sessions=sessions)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)