# ML-based Stock Prediction application

### Description

The project was completed in a team of three people and submitted as a final project for COMP5100 Software Engineering class. 

This project involves using long short-term memory (LSTM) recurrent neural networks to predict stock prices and a web application to display the predicted prices interactively. The project team has developed and trained an LSTM model using historical stock price data, which can be used to make predictions about future stock prices. The web application allows users to explore the predicted prices for different stocks and provides visualizations of the predicted prices. The application also includes options for users to customize the prediction parameters and receive alerts for significant changes in the predicted prices. The project is available on GitHub for users to download, modify, and use as they see fit.

### Technologies:
- Flask
- Jinja
- HTML
- CSS
- SQLite

### How to Run:
- Install python virtual environment: pip install virtualenv
- Open the terminal in Stock Prediction folder
- Create a virtual environment: python -m venv venv
- Activate the virtual environment: source venv/bin/activate
- Install flask: pip install Flask
- Set application init folder: export FLASK_APP=flaskr
- Initiate SQLite database: flask init-db
- Run Application: flask run
