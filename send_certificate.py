import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import streamlit as st
email_address = st.secrets["email"]["email_address"]
email_password = st.secrets["email"]["email_password"]
# Function to get the receiver's email from the configuration file
def get_receiver_add():
    try:
        with open("config.txt") as f:
            emails = [i for i in f.read().split('\n')] 
            return emails
    except FileNotFoundError:
        print("Config file not found. Initiating email setup.")
        return None

# Function to get the log file path
import os

def get_certificate(name, certificate_dir="certificates"):
    """
    Function to get the path of the certificate for a given name.

    Parameters:
    - name (str): The name of the participant for whom the certificate is being requested.
    - certificate_dir (str): The directory where certificates are stored (default is 'certificates').

    Returns:
    - str: Path to the certificate if found, or a message indicating it's not found.
    """
    # Normalize the name to match the expected certificate file format (e.g., 'John Doe.pdf')
    certificate_filename = f"{name}.pdf"  # Assuming certificates are in PDF format

    # Construct the full path to the certificate
    certificate_path = os.path.join(certificate_dir, certificate_filename)

    # Check if the certificate exists in the specified directory
    if os.path.exists(certificate_path):
        return certificate_path
    else:
        return f"Certificate for '{name}' not found in the '{certificate_dir}' directory."


# Function to send the email with the provided details
def send_mail(certificate,receiver_add):
    # Set up the email parameters
    message = MIMEMultipart()
    message["From"] = email_address
    password = email_password
    
    message["Subject"] = "CODE CRAVE'25"
    
    # Check if the receiver email is available
    if not receiver_add:
        raise ValueError("Receiver email address is not specified.")
    
    message["To"] = receiver_add

    # Compose the body of the email with dynamic content
    body = f"""
    Dear Participant,

    Greetings from the Project Club! 🌟

    We are thrilled to have had you participate in the Code Crave'25 event. Your involvement and enthusiasm made the event a great success! As a token of appreciation for your contribution, we are pleased to present you with your e-certificate.

    Thank you once again for being a part of Code Crave'25!

    Warm Regards,
    The Code Crave'25 Team
    """


    # Attach the body to the email
    message.attach(MIMEText(body, "plain"))

    # Attach the log file to the email
    certificate = get_certificate()
    try:
        with open(certificate, "rb") as attachment:
            mime_base = MIMEBase("application", "octet-stream")
            mime_base.set_payload(attachment.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(certificate)}"
            )
            message.attach(mime_base)
    except FileNotFoundError:
        print(f"File not found: {certificate}")
        exit(1)

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(message["From"], password)
            server.send_message(message)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")

