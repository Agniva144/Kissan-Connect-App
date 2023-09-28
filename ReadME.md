# Bidding System

This is a web-based bidding system built using Python and Flask. It allows farmers to list vegetables for sale, retailers to place bids on those vegetables, and administrators to manage the bidding process.

## Features

- **User Roles**: The system supports three user roles: farmer, retailer, and administrator.

- **Bidding**: Retailers can place bids on vegetables listed by farmers.

- **Admin Control**: Administrators can set bidding durations and start/stop the bidding process.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python
- Flask
- SQLite (for the database)

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/YourUsername/Bidding-System.git
   cd Bidding-System


# Getting Started

Follow these steps to set up and use the Bidding System:

## Installation

1. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Create the database:

    ```bash
    python create_db.py
    ```

3. Start the Flask application:

    ```bash
    python app.py
    ```

## Usage

1. Access the application in your web browser by visiting [http://localhost:5000/](http://localhost:5000/).

2. Sign up for an account as a farmer, retailer, or administrator.

3. Log in and start using the application based on your role.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix.

3. Make your changes and test them thoroughly.

4. Create a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/en/2.1.x/) - The web framework used
- [SQLite](https://www.sqlite.org/index.html) - The database engine used

## Directory Structure
bidding_project/
├── app.py
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── farmer.html
│   ├── retailer.html
│   ├── admin.html
│   ├── bid_Details.html
│   ├── admin_check.html
│   ├── about.html
├── Bidding2/
│   └── loginCred3.sqlite
└── README.md


## Contact

For any questions or inquiries, please contact agnivashil30@gmail.com.
