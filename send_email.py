import smtplib

def send_from_gmail(gmail_user, gmail_password, to, subject, body):
    '''
    Send an email from a gmail account

    Parameters
    ----------
    gmail_user : string
        gmail email to be used for sending the e-mail.
    gmail_password : string
        password of the gmail account to be used for sending the e-mail.
    to : list of strings
        email addresses to which to send the e-mail.
    subject : string
        subject of the e-mail.
    body : string
        body of the e-mail.

    Returns
    -------
    None.

    '''
    
    sent_from = gmail_user
    
    fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, fmt.format(sent_from, ", ".join(to), subject, body).encode('utf-8'))
    server.close()