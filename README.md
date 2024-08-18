# Secure File Sharing Application

This is a secure file-sharing server implemented in Python. It allows users to upload and download files through a simple web interface over an HTTPS connection. The server generates a QR code for easy access from other devices on the same network.

## Features

- **HTTPS Connection**: Secures the communication between the client and server using SSL/TLS.
- **File Upload and Download**: Allows users to upload files to the server and download available files from the shared directory.
- **QR Code Access**: Generates a QR code to easily access the server from mobile devices or other clients.
- **Secure Path Handling**: Prevents directory traversal attacks by securely handling file paths.
- **Logging**: Logs all file upload activities for auditing and monitoring purposes.

## Requirements

- Python 3.x
- Required Python modules:
  - `http.server`
  - `socketserver`
  - `ssl`
  - `cgi`
  - `shutil`
  - `logging`
  - `pyqrcode`

## Installation

1. Clone the repository or download the code.
2. Install the required Python modules:
   ```bash
   pip install pyqrcode pypng
   ```
3. Generate SSL certificates for HTTPS:
   ```bash
   openssl req -new -x509 -keyout key.pem -out cert.pem -days 365 -nodes
   ```
4. Place the generated `key.pem` and `cert.pem` files in the same directory as the script.

## Usage

1. Run the server script:
   ```bash
   python file_sharing_server.py
   ```
2. The server will start and listen on port `4433` by default.
3. A QR code will be generated and saved as `server_qr.png`. Scan this QR code with a mobile device to access the server.
4. Alternatively, you can access the server via a web browser using the provided HTTPS link.

## Directory Structure

- **uploads/**: The directory where uploaded files are stored. This directory is created automatically if it doesn't exist.
- **server_qr.png**: The QR code image for accessing the server.
- **file_sharing.log**: Log file recording all file upload activities.

## Security Considerations

- Ensure that the `uploads/` directory is appropriately secured and does not contain sensitive information.
- Use strong SSL certificates to protect the data in transit.
- Regularly monitor the `file_sharing.log` for any unusual activity.

## Customization

- You can change the upload directory by modifying the `UPLOAD_DIR` variable in the script.
- The server port can be modified by changing the `PORT` variable.
- Additional security features or custom logging can be added as per your requirements.

