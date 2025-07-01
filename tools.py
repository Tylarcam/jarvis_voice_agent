import logging
from livekit.agents import function_tool, RunContext
import requests
from   import DuckDuckGoSearchRun
import os
import smtplib
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
from typing import Optional
import difflib
import subprocess
import platform

@function_tool()
async def get_weather(
    context: RunContext,  # type: ignore
    city: str) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()   
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}." 

@function_tool()
async def search_web(
    context: RunContext,  # type: ignore
    query: str) -> str:
    """
    Search the web using DuckDuckGo.
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."    

@function_tool()    
async def send_email(
    context: RunContext,  # type: ignore
    to_email: str,
    subject: str,
    message: str,
    cc_email: Optional[str] = None
) -> str:
    """
    Send an email through Gmail.
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        message: Email body content
        cc_email: Optional CC email address
    """
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Get credentials from environment variables
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")  # Use App Password, not regular password
        
        if not gmail_user or not gmail_password:
            logging.error("Gmail credentials not found in environment variables")
            return "Email sending failed: Gmail credentials not configured."
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add CC if provided
        recipients = [to_email]
        if cc_email:
            msg['Cc'] = cc_email
            recipients.append(cc_email)
        
        # Attach message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to Gmail SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(gmail_user, gmail_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(gmail_user, recipients, text)
        server.quit()
        
        logging.info(f"Email sent successfully to {to_email}")
        return f"Email sent successfully to {to_email}"
        
    except smtplib.SMTPAuthenticationError:
        logging.error("Gmail authentication failed")
        return "Email sending failed: Authentication error. Please check your Gmail credentials."
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        return f"Email sending failed: SMTP error - {str(e)}"
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return f"An error occurred while sending email: {str(e)}"

@function_tool()
async def open_directory(context: RunContext, directory_name: str) -> str:
    r"""
    Fuzzy search for a directory under C:\Users\tylar\code and open it in Cursor using cnew. If the user says 'code', 'the code folder', or similar, open the main code directory.
    """
    # Normalize and interpret common references
    normalized = directory_name.strip().lower()
    if normalized in ["code", "the code folder", "my code", "main code", "code directory", "the code directory"]:
        best_match = r"C:\Users\tylar\code"
        try:
            subprocess.Popen(["cnew", best_match])
            return f"Opened directory: {best_match} in Cursor using cnew."
        except Exception as e:
            return f"Failed to open directory: {str(e)}"
    
    root_dir = r"C:\Users\tylar\code"
    all_dirs = []
    for dirpath, dirnames, _ in os.walk(root_dir):
        for d in dirnames:
            all_dirs.append(os.path.join(dirpath, d))
    matches = difflib.get_close_matches(normalized, [os.path.basename(d).lower() for d in all_dirs], n=1, cutoff=0.6)
    if not matches:
        return f"No directory found matching '{directory_name}'."
    best_match = next(d for d in all_dirs if os.path.basename(d).lower() == matches[0])
    try:
        subprocess.Popen(["cnew", best_match])
        return f"Opened directory: {best_match} in Cursor using cnew."
    except Exception as e:
        return f"Failed to open directory: {str(e)}"

@function_tool()
async def list_files(context: RunContext, directory: str = r"C:\Users\tylar\code") -> str:
    r"""
    List all files in the specified directory. Defaults to C:\Users\tylar\code.
    """
    try:
        if not os.path.isdir(directory):
            return f"Directory not found: {directory}"
        files = os.listdir(directory)
        if not files:
            return f"No files found in {directory}."
        return "Files in {}:\n".format(directory) + "\n".join(files)
    except Exception as e:
        return f"Failed to list files in {directory}: {str(e)}"

@function_tool()
async def get_os_info(context: RunContext) -> str:
    r"""
    Get information about the operating system, including name, version, and platform details.
    """
    try:
        os_name = platform.system()
        os_version = platform.version()
        os_release = platform.release()
        platform_info = platform.platform()
        return (
            f"OS Name: {os_name}\n"
            f"OS Version: {os_version}\n"
            f"OS Release: {os_release}\n"
            f"Platform Info: {platform_info}"
        )
    except Exception as e:
        return f"Failed to get OS info: {str(e)}"