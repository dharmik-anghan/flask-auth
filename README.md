# Flask-social-media

A detailed description of your project.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
  - [Virtual Environment](#virtual-environment)
  - [.env Configuration](#env-configuration)
  - [Installing Dependencies](#installing-dependencies)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Database Migrations](#database-migrations)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Overview

### Project Overview

Welcome to Flask-auth ! This project is a comprehensive Flask-based web application that incorporates Google Authentication for user sign-in. It serves as a robust foundation for building social networking and content-sharing platforms. The project structure follows a modular approach, ensuring clear organization and maintainability.

### Key Features

- **Google Authentication:** Enables users to sign in securely using their Google accounts, providing a seamless and trusted login experience.

- **RESTful API:** Offers a set of RESTful API endpoints for managing user accounts, posts, likes, comments, and various interactions.

- **Database Integration:** Leverages SQLAlchemy for efficient database management, ensuring data integrity and scalability.

- **Token-based Authentication:** Implements JSON Web Tokens (JWT) for secure user authentication, enhancing the overall security of the application.

- **Email Sending System:** Includes a utility for sending email notifications, facilitating communication and user engagement.

- **Flexible Configuration:** Easily configurable through environment variables and a centralized configuration file (`config.py`), allowing customization to suit specific deployment environments.

## Setup

### Virtual Environment

It is recommended to use a virtual environment to manage project dependencies. Follow these steps to create a virtual environment:

```bash
# Create a virtual environment
python -m venv venv
```
```bash
# Activate the virtual environment
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate      # For Windows
```

## .env Configuration

Create a `.env` file in the root directory of your project and use it to store sensitive configuration information. This file is crucial for security, and it should not be shared or exposed to the public. Below is a template for your `.env` file, and you should fill in the values according to your project requirements:

```ini
FLASK_APP=The name of your Flask application.
FLASK_ENV=The environment in which Flask is running (development or production).
SECRET_KEY=A secret key for session security.
FLASK_DEBUG=Set to 1 for debugging mode.
FLASK_RUN_PORT=Port on which the Flask application will run.
FLASK_RUN_HOST=Hostname for the Flask application.
SQLALCHEMY_DATABASE_URI=Database URI for SQLAlchemy.
JWT_SECRET_KEY=Secret key for JWT (JSON Web Token) encoding and decoding.
JWT_IDENTITY_CLAIM=Claim used to identify the user in the JWT.
EMAIL_PASSWORD=Password for sending emails (if applicable).
OTP_EXPIRES_IN=Expiration time for one-time passwords.
GOOGLE_CLIENT_ID=Google OAuth client ID.
GOOGLE_CLIENT_SECRET=Google OAuth client secret.
CONF_URL=URL for OAuth server metadata (if using OAuth).
```

## Installing Dependencies

Install the project dependencies using pip and the requirements.txt file:

```bash
pip install -r requirements.txt
```

## Project Structure

The project is organized into various folders and files, each serving a specific purpose. Below is an overview of the project structure:

- **`api/`**
  - `helpers/`: Helper functions for resources.
  - `resources/`: Methods for post, post-like, comment-like, comment reply, comment follower, and following are defined here.
  - `schemas/`: Schemas for various entities.
  - `views.py`: API views for handling HTTP requests.

- **`auth/`**
  - `helpers.py`: Token generation, login, token revocation, token refresh, etc.
  - `views.py`: Views related to authentication.

- **`google_auth/`**
  - `views.py`: Implementation of the Google login system.

- **`models/`**
  - Database models.

- **`utils/`**
  - Email sending system.

- **`app.py`**
  - Main application file, configuring Flask, extensions, and registering blueprints.

- **`config.py`**
  - Configuration file for the project, containing environment variables.

- **`extensions.py`**
  - File for Flask extensions.

- **`alembic.ini`**
  - Configuration file for Alembic (database migration tool).

- **`requirements.txt`**
  - List of Python packages required for the project.

## Usage

Explain how to run your project and any additional steps required for proper execution:

```bash
python app.py
```
Visit http://localhost:5000 in your browser.

## Database Migrations
If your project involves database changes, you may need to apply migrations using Alembic. Follow these steps:

1. Ensure your virtual environment is activated.
2. Run the following commands to initialize Alembic:
```bash
alembic init alembic
```
3. After making changes to your database models, generate a new migration using the --autogenerate option:
```bash
alembic revision --autogenerate -m "Your migration message"
```
This command automatically detects changes in your models and generates a new migration script.
4. Apply the migration to update the database schema:
```bash 
alembic upgrade head
```
**Note**: Ensure that your database URL is correctly configured in your .env file and config.py.

**Warning**: The --autogenerate option attempts to automatically detect changes in your models. It is crucial to review the generated migration script to ensure accuracy and make any necessary adjustments.

Note: If you prefer Flask-Migrate, you can use flask db migrate for migration generation.

## Configuration

The project relies on configuration files and environment variables to customize its behavior. Below is a list of configuration options and their purposes:

- **`FLASK_APP`**: The name of your Flask application.

- **`FLASK_ENV`**: The environment in which Flask is running (`development` or `production`).

- **`SECRET_KEY`**: A secret key for session security.

- **`FLASK_DEBUG`**: Set to `1` for debugging mode.

- **`FLASK_RUN_PORT`**: Port on which the Flask application will run.

- **`FLASK_RUN_HOST`**: Hostname for the Flask application.

- **`SQLALCHEMY_DATABASE_URI`**: Database URI for SQLAlchemy.

- **`JWT_SECRET_KEY`**: Secret key for JWT (JSON Web Token) encoding and decoding.

- **`JWT_IDENTITY_CLAIM`**: Claim used to identify the user in the JWT.

- **`EMAIL_PASSWORD`**: This is password you get while setting up your SMTP email.

- **`OTP_EXPIRES_IN`**: Expiration time for one-time passwords.

If you are setting up your Google login 

- **`GOOGLE_CLIENT_ID`**: Google OAuth client ID.

- **`GOOGLE_CLIENT_SECRET`**: Google OAuth client secret.

- **`CONF_URL`**: URL for OAuth server metadata (if using OAuth).

Create a `.env` file in the root directory of your project based on the provided `.env.example`. Fill in the required values for each configuration option.

Example `.env` file:

```ini
FLASK_APP=your_flask_app_name
FLASK_ENV=development
SECRET_KEY=your_secret_key
FLASK_DEBUG=1
FLASK_RUN_PORT=5000
FLASK_RUN_HOST=localhost
SQLALCHEMY_DATABASE_URI=your_database_uri
JWT_SECRET_KEY=your_jwt_secret_key
JWT_IDENTITY_CLAIM=user_id
EMAIL_PASSWORD=your_email_password
OTP_EXPIRES_IN=1
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
CONF_URL=your_oauth_server_url
```

## Contributing

Thank you for considering contributing to this project! Whether it's reporting issues, suggesting features, or contributing code, your help is highly appreciated.

### Reporting Issues

If you encounter any issues with the project, please open a new issue on the [GitHub Issue Tracker](https://github.com/dharmik-anghan/flask-auth/issues). Provide as much detail as possible, including steps to reproduce the issue, your environment, and any relevant error messages.

### Feature Requests

If you have a feature request or an enhancement idea, feel free to create an issue on the [GitHub Issue Tracker](https://github.com/dharmik-anghan/flask-auth/issues) to discuss and share your thoughts.

### Contributing Code

1. Fork the repository on GitHub.

2. Clone your forked repository to your local machine:

   ```bash
   git clone https://github.com/your-username/your-repository.git
   ```
3. Create a new branch for your contribution:

```bash
git checkout -b feature/your-feature
```
4. Make your changes and commit them with descriptive commit messages:

```bash
git add .
git commit -m "Add your feature or fix"
```

5. Push your changes to your forked repository:

```bash
git push origin feature/your-feature
```

6. Open a pull request on the GitHub Pull Requests page.

### Code Style

Follow the established coding style in the project. If there's a specific style guide, linting, or formatting requirements, mention them here.

### Code of Conduct

Please adhere to the Code of Conduct to ensure a positive and inclusive community.

By contributing to this project, you agree that your contributions will be licensed under the project's LICENSE.

Thank you for your contributions!
