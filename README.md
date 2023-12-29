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
- [License](#license)

## Overview

Provide a detailed overview of your project, its purpose, and key features.

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

- **`auth/`**
  - `helpers.py`: Token generation, login, token revocation, token refresh, etc.
  - `views.py`: Views related to authentication.

- **`google_auth/`**
  - Google login system implementation.

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

