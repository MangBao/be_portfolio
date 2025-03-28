# be_portfolio

## Introduction

`be_portfolio` is a backend API project designed to manage personal information and projects for a portfolio. The project is built using Python and Shell Script, making it easy to deploy and use.

## Features

- Manage personal information
- Manage project categories
- RESTful API for data retrieval

## System Requirements

- Python 3.8+
- Pip
- Virtualenv (optional)
- Required Python libraries (listed in `requirements.txt`)

## Installation Guide

### 1. Clone the repository

```sh
git clone https://github.com/MangBao/be_portfolio.git
cd be_portfolio
```

### 2. Create and activate a virtual environment (optional)

```sh
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project's root directory and add the necessary environment variables:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

### 5. Run the project

```sh
python main.py
```

## API Endpoints

- `GET /projects` - Retrieve a list of projects
- `POST /projects` - Add a new project
- `GET /profile` - Retrieve personal information

## Contribution

If you would like to contribute, please create a Pull Request or open an Issue on GitHub.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.

