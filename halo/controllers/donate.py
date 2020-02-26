import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import JsonResponse
from halo.settings_secret import GMAIL, GMAIL_PASSWORD


def donate_email(request):
    gamertag = request.POST['gamertag']
    twitch = request.POST['twitch']
    twitter = request.POST['twitter']
    youtube = request.POST['youtube']
    message = request.POST['message']
    donation = str(request.POST['donate'])

    from_email = "mccstats@noreply.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Donation by  " + gamertag + ": " + donation
    msg['From'] = from_email
    msg['To'] = GMAIL

    # Create the body of the message (a plain-text and an HTML version).
    text = "Gamertag: " + gamertag + "\n" + "Twitch: " + twitch + "\n" + "Twitter: " + twitter + "\n" + "Youtube: " + youtube + "\n\n" + "Message: " + message
    html = """\
    <html>
      <head></head>
      <body>
        <div>
        <p>
        Gamertag: """ + gamertag + """<br />""" + """Twitch: """ + twitch + """<br />""" + """Twitter: """ + twitter + """<br />""" + """Youtube: """ + youtube + """<br /><br />""" + """Message: """ + message + """
        </p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(GMAIL, GMAIL_PASSWORD)

    # sendmail function takes 3 arguments: sender's address, recipient's address
    s.sendmail(from_email, GMAIL, msg.as_string())
    s.quit()

    return JsonResponse({'success': True}, safe=False)
