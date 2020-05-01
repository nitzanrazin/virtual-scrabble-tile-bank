import smtplib

def send_from_gmail(gmail_address, gmail_password, to, subject, body):
    '''
    Send an email from a gmail account

    Parameters
    ----------
    gmail_address : string
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

    fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_address, gmail_password)
    server.sendmail(gmail_address, to, fmt.format(gmail_address, ", ".join(to), subject, body).encode('utf-8'))
    server.close()