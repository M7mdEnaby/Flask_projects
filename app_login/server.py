from flask import request, Flask
import pandas as pd
import os

app = Flask(__name__)

# Define the file name for storing user data
csv_file = "users.csv"

# Helper function to check if the CSV file exists, and create it if not
def initialize_csv():
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(csv_file, index=False)

# Route to render the login and register form
@app.route('/')
def home():
    return '''
        <h2>Login Form</h2>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <input type="submit" value="Login">
        </form>

        <h2>Register Form</h2>
        <form method="POST" action="/register">
            <input type="text" name="new_username" placeholder="New Username" required><br>
            <input type="password" name="new_password" placeholder="New Password" required><br>
            <input type="submit" value="Register">
        </form>
    '''

# Route to handle login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Validate credentials
    if ((df['username'] == username) & (df['password'] == password)).any():
        return "Login successful!"
    else:
        return "Invalid credentials. Please try again.", 401

# Route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    username = request.form['new_username']
    password = request.form['new_password']

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Check if the username is already registered
    if (df['username'] == username).any():
        return "Username already registered.", 400
    
    # Append the new user data to the DataFrame and save it to the CSV file
    new_user = pd.DataFrame({"username": [username], "password": [password]})
    new_user.to_csv(csv_file, mode='a', header=False, index=False)

    return "User registered successfully!", 200

if __name__ == '__main__':
    # Initialize the CSV file on startup
    initialize_csv()
    app.run(debug=True)
