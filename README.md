# LockBoxXtreme

![LockBoxXtreme Logo](https://via.placeholder.com/728x90.png?text=LockBoxXtreme)

## Overview

**LockBoxXtreme** is a fun and secure command-line tool for storing and retrieving passwords. Designed with both functionality and flair, LockBoxXtreme encrypts your passwords to keep them safe from prying eyes, while also providing a colorful and engaging interface to make password management a bit more enjoyable.

## Features

- 🔒 **Secure Storage**: Encrypts passwords using the robust `cryptography` library.
- 🔍 **Easy Retrieval**: Retrieve passwords by simply entering the service name.
- 🎨 **Engaging Interface**: A playful, colorful command-line experience.
- 🕹️ **Interactive Prompts**: Unique and entertaining prompts to brighten up password management.

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
pip install -r requirements.txt
```

### Run the Application

- Start the application:

```bash
python3 main.py
```

### Usage

**Storing a Password**

- The password will be encrypted and stored.
  
  (Encryption):

```python
encrypted_password = encrypt_message(password, key)
passwords[service] = encrypted_password.decode()
save_passwords(passwords)
```

### Retrieving a Password

- If the service exists, the decrypted password will be displayed.

 (Decryption):

```python
encrypted_password = passwords.get(service)
if encrypted_password:
    decrypted_password = decrypt_message(encrypted_password.encode(), key)
```

### Contributing
We welcome contributions to LockBoxXtreme! If you have suggestions, bug reports, or improvements, please submit an issue or pull request on our [GitHub](https://github.com/gandhibhai/LockBoxXtreme/issues/new) repository.

### License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/gandhibhai/LockBoxXtreme/blob/main/LICENSE) file for details.

### Acknowledgments

- **Cryptography Library:** Thanks to the creators of the cryptography library for their secure encryption tools.
- **Colorama Library:** Appreciation for the colorama library which helps in making the command-line interface colorful and engaging.
- **Contributors:** A big thank you to all contributors who help enhance this project.

### Contact
For any queries or feedback, you can reach out to the project maintainer:

- **Name:** Anonymous
- **Email:** loverslandgandhi@gmail.com

Thank you for using LockBoxXtreme. We hope this tool helps you manage your passwords securely and efficiently!
