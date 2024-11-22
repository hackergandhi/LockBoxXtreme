# LockBoxXtreme

![LockBoxXtreme Logo](https://via.placeholder.com/728x90.png?text=LockBoxXtreme)

## Overview

**LockBoxXtreme** is a robust and engaging tool for managing passwords, now entirely based on a web interface. With strong encryption and a user-friendly design, it makes password management both secure and accessible.

## Features

- 🔑 **Master Password Setup:** Secure your data with a master password.
- 🌐 **Web Interface**: Access and manage passwords using your browser.
- 📂 **Database Storage:** Passwords are securely stored in a SQLite database.
- 🔄 **Password Management:** Store, retrieve, update, and delete passwords with ease.
- ⚡ **Password Generation:** Instantly generate strong passwords through the web app.

## Installation

### Prerequisites

- Python 3.7 or higher
- `pip` (Python package installer)

### Steps to Install

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/GumnaamSaaya/LockBoxXtreme.git
   cd LockBoxXtreme
   ```

### Install Dependencies

Install the required Python packages:

```bash
pip3 install -r requirements.txt
```

### Run the Application

- Run the Application:

```bash
python3 app.py
```

- Access the Web Interface Open your browser and go to:

```arduino
  http://127.0.0.1:5000
```

### Usage

**Storing a Password**

1) Navigate to the "Store Password" page.
2) Provide the service name and the password you want to store.
3) The password is encrypted before storage using the Fernet method:

```python
encrypted_password = fernet.encrypt(password.encode()).decode()
```
4) The encrypted password is stored securely in the SQLite database.

### Retrieving a Password

1) Navigate to the "Retrieve Password" page.
2) Search for the service name.
3) If the service exists, the encrypted password is retrieved and decrypted:

```python
decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
```
4) The decrypted password is displayed on the web interface.

**Updating the Master Password**

1) Navigate to the "Update Master Password" page.
2) Provide the current master password and the new password.
3) The new password is hashed using bcrypt and securely stored in the database:

```python
hashed_pw = hashpw(new_password.encode(), gensalt())
```
**Password Deletion**

1) Navigate to the "Delete Password" page.
2) Provide the service name and master password.
3) The corresponding entry is removed from the database if authentication succeeds.

### Contributing
We welcome contributions to LockBoxXtreme! If you have suggestions, bug reports, or improvements, please submit an issue or pull request on our [GitHub](https://github.com/gandhibhai/LockBoxXtreme/issues/new) repository.

### License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/gandhibhai/LockBoxXtreme/blob/main/LICENSE) file for details.

### Acknowledgments

- **Cryptography Library:** Thanks to the creators of the cryptography library for their secure encryption tools.
- **Flask Framework:** For enabling a clean and intuitive web-based interface.
- **SQLite:** For efficient and lightweight database storage.
- **Contributors:** A big thank you to all contributors who help enhance this project.

### Contact
For any queries or feedback, you can reach out to the project maintainer:

- **Name:** Anonymous
- **Email:** loverslandgandhi@gmail.com

Thank you for using LockBoxXtreme. We hope this tool helps you manage your passwords securely and efficiently!
