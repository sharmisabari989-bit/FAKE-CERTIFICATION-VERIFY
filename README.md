# Fake Certificate Verification System

A beginner-friendly web application developed using Flask and PostgreSQL to verify the authenticity of certificates using QR codes.

# 📌 Project Overview

The Fake Certificate Verification System helps organizations verify whether a certificate is genuine or invalid.

Each registered certificate is assigned a unique Certificate ID and a QR code. When the QR code is scanned, the system checks the certificate details from the PostgreSQL database and displays the verification result.

#  Features

- Certificate registration
- Unique Certificate ID generation
- QR code generation
- QR-based certificate verification
- Valid certificate verification
- Invalid certificate detection
- PostgreSQL database integration
- Simple web interface
- Local network QR verification

# Technologies Used

- Python
- Flask
- PostgreSQL
- HTML
- CSS
- QR Code
- psycopg2
- Python qrcode library

# Project Structure

```text
fake-cert-verify/
│
├── static/
│   └── Generated QR codes and static files
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── success.html
│   └── verify.html
│
├── app.py
├── .env
├── .gitignore
└── README.md