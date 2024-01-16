# NFC Contact Webapp

The "NFCContactShare" web application facilitates contact information sharing through NFC (Near Field Communication) technology. Admins generate NFC tags, each associated with a unique UUID. Users receive physical NFC tags and, upon reading, are directed to the application. If the UUID is linked to a user, their contact details are displayed; if not, users are guided to sign up. Admins manage tags through the admin dashboard.

## Setup and Installation

1. Clone the repository to your local machine.
2. Install the required dependencies with `pip install -r requirements.txt`.
3. Set up the database by running `python create_db.py`.
4. Create an admin user by running `python create_admin.py`.
5. Start the application with `python app.py`.

## Usage

1. **Admins generate NFC tags**, on /admin/dashboard
2. **Users read NFC tags**, leading to "/tag/{uuid}" route.
3. **Application checks UUID association**:
   - If associated, redirects to "/user/contact_details/{username}".
   - If not, redirects to user signup.
4. **Users sign up**, associating the NFC tag UUID.
5. **After signup/login**, users manage contact details on "/user/dashboard".

## Tech Stack

- Backend: Flask, Flask-Login, Flask-SQLAlchemy
- Frontend: HTML, CSS (Pico.css framework), JavaScript
- Database: Any of your choosing
- Password Hashing: Werkzeug Security, Flask-Bcrypt
- Other Dependencies: Flask-WTF
- Server: gunicorn (production server)


## Contributing

Contributions are welcome. Please open an issue to discuss your idea or submit a pull request.

## License

This project is licensed under the terms of the GNU General Public License v2.0.