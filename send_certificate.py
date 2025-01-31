import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import streamlit as st

# Function to get the receiver's email from the configuration file
def get_receiver_add():
    # Open the config.txt file which should be in the root directory of your repo
    try:
        with open("config.txt") as f:
            emails = [i.strip() for i in f.read().splitlines()]  # Read and clean emails
            return emails
    except FileNotFoundError:
        st.error("Config file not found. Please ensure config.txt is uploaded.")
        return []

# Function to get the certificate path
def get_certificate(name, certificate_dir="certificates"):
    # Assuming certificates are stored in a 'certificates' folder in your repo
    certificate_filename = f"{name}.pdf"  # Certificates should be in PDF format
    certificate_path = os.path.join(certificate_dir, certificate_filename)
    
    # Check if the certificate exists in the specified directory
    if os.path.exists(certificate_path):
        return certificate_path
    else:
        return f"Certificate for '{name}' not found in the '{certificate_dir}' directory."

# Function to send the email with the provided details
def send_mail(certificate, receiver_add):
    # Retrieve sensitive data like email address and password from Streamlit secrets
    email_address = st.secrets["cortexoa@gmail.com"]
    email_password = st.secrets["rdhrxsyuvujnglta"]
    
    # Set up the email parameters
    message = MIMEMultipart()
    message["From"] = email_address
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
    message.attach(MIMEText(body, "plain"))

    # Attach the certificate
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
            server.login(email_address, email_password)
            server.send_message(message)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")

# Streamlit UI for running the function
def main():
    # Step 1: Get the email list from the uploaded config file
    receiver_emails = get_receiver_add()
    if not receiver_emails:
        st.error("Config file is missing or empty. Please upload a valid config file.")
        return
    
    # Step 2: Get participant's name and the corresponding certificate
    name = st.text_input("Enter participant's name:")
    if name:
        certificate_path = get_certificate(name)
        if "not found" in certificate_path:
            st.error(certificate_path)
            return
        
        # Step 3: Send the certificate
        if st.button("Send Certificate"):
            for email in receiver_emails:
                send_mail(certificate_path, email)
                st.success(f"Certificate sent to {email}")
    else:
        st.error("Please enter a participant's name.")

if __name__ == "__main__":
    main()
