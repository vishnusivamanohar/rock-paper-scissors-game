🌑 Rock Paper Scissors AI - Web Application
A sophisticated, full-stack web application that brings the classic "Rock Paper Scissors" game to the digital age. Built with a focus on interactive UI and persistent data tracking, this project allows users to compete against an AI or a local second player.

📖 About the Project
This application is designed to be more than just a simple script. It features a complete ecosystem including:

Single Player Mode: Test your luck against a randomized AI opponent.

Double Player Mode: A local competitive mode for two players to battle on the same device.Both players should attempt at same time.

Persistent Scoring: Unlike basic versions, this uses a database to track Wins, Losses, and Draws.

Interactive UI: A dark-themed, responsive interface designed for both desktop and mobile play.

Detailed Documentation: For a full walkthrough of the features and screenshots, visit the About Page( https://vishnusivamanohar.github.io/rock-paper-scissors-game/static/about.html).

🛠️ Technical Stack
Frontend: HTML5, CSS3 (Modern Dark Theme), and JavaScript for real-time game logic.

Backend: Flask (Python) - Handles routing, game rules, and database communication.

Database: MySQL - Stores player scores and game history for the leaderboard.

📂 Project Structure
Based on the development environment, the project is organized as follows:

app.py - The main Flask server file.

/templates - Contains the HTML files (index.html, about.html, etc.).

/static - Stores assets including:

game_page.png / double_player_page.png - UI Screenshots.

bg-music(plsent) - Background audio files.

rpc.png - Game icons and assets.

🕹️ How to Play

Select Your Move: Click on one of the three buttons (Rock, Paper, or Scissors).

Computer Turn: The computer will randomly select its move.(if single player)

Result: The winner is decided based on standard rules:

Rock beats Scissors.

Scissors beats Paper.

paper beats rock.

Paper beats Rock.

Keep Score: Your wins, losses, and draws are updated immediately at the bottom of the screen.
