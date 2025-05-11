# email_notification.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
from datetime import datetime

def send_email_with_attachment(file_path, gmail_user, gmail_password, recipient_email):
    """Send an email with formatted HTML articles and CSV attachment."""
    df = pd.read_csv(file_path)
    
    # Custom HTML formatting for each article
    html_articles = []
    for _, row in df.iterrows():
        article_html = f"""
        <div style="margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px;">
            <p style="font-size: 16px; font-weight: bold; margin: 5px 0;">{row['TITLE']}</p>
            <p style="margin: 5px 0; color: #555;">
                {row['AUTHOR']} - {row['DATE_PUBLISHED']}
            </p>
            <p style="margin: 5px 0;">
                <a href="{row['ARTICLE_LINK']}" style="color: #1a73e8; text-decoration: none;">Read Article</a>
            </p>
            <p style="margin: 5px 0; font-style: italic; color: #777;">
                Source: {row['SOURCE']}
            </p>
        </div>
        """
        html_articles.append(article_html)
    
    # Full HTML email body
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #202124;">Sportiverse</h2>
            <p style="color: #5f6368;">{datetime.now().strftime('%B %d, %Y')}</p>
            {"".join(html_articles)}
        </body>
    </html>
    """

    # Create email
    msg = MIMEMultipart()
    msg['Subject'] = f"Sportiverse: What’s Hot in Sports Today"
    msg['From'] = f"Sportiverse {gmail_user}"
    msg['To'] = recipient_email

    # Attach HTML body
    msg.attach(MIMEText("Your daily Sportiverse update is ready!", 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)