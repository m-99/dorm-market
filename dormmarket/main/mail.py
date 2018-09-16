import smtplib

try:
    from . import mailconfig
except:
    pass


def send_mail(recipient, subject, text):
    # Gmail Sign In
    gmail_sender = mailconfig.sender
    gmail_passwd = mailconfig.passwd

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % recipient,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % subject,
                        '', text])

    try:
        server.sendmail(gmail_sender, [recipient], BODY)
        print('email sent')
    except Exception as e:
        print('error sending mail' + str(e))

    server.quit()
