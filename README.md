# Parallel Chatbot Backend
Welcome to the Parallel Chatbot Backend repository! This backend is designed to support the Parallel trading card game, set in a post-apocalyptic future. The game has rich lore, intricate gameplay mechanics, and a variety of card types.

## Overview
Lore: The world of Parallel is set after a cataclysmic event known as "The Priming." Humanity has split into five distinct factions, each known as a Parallel. Learn more about these factions and their unique characteristics in the main.md document.

Gameplay Mechanics: Players construct decks representing one of the Parallels and engage in 1v1 turn-based battles. The game involves various card types like Units, Effects, Relics, and Upgrades. The primary objective is to reduce the opponent's Health Points (HP) to zero.

Backend Features: This backend is designed to handle user queries related to the game, using the Flask framework and other utilities. It uses embeddings to fetch relevant information from documents and provides endpoints for querying the bot.

## Installation and Setup
Requirements: Ensure you have the necessary packages installed. Check the requirements.txt for a list of required packages.

Configuration: The backend uses gunicorn for serving the application. The configuration can be found in gunicorn_config.py.

Running the App: Use the Flask app defined in app.py to run the backend server.

Endpoints: The main endpoint for querying the bot can be found in endpoints.py.

Utilities: Various utility functions and initializations are present in utilities.py.

Embedding Generator: To generate embeddings for the documents, refer to embedding_generator.py.

## Contribution
Feel free to fork this repository, make changes, and submit pull requests. Any contributions, whether it's refining the code or enhancing the features, are highly appreciated!
