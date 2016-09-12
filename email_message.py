import smtplib
import scraper
exec('scraper')
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scraper import subreddits, titles, urls, selftext, top_comments, top_comments_author
# me == my email address
# you == recipient's email address
me = "mehulmshah22@gmail.com"
you = "mms005@ucsd.edu"
# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Reddit Briefing v1... Thoughts?"
msg['From'] = me
msg['To'] = you
# Create the body of the message (a plain-text and an HTML version).
#text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>
       <h1>Subreddit:</h1> %s<br>
       <h1>Post:</h1> <a href=%s>%s</a><br>
       <h1>Self Text:</h1> %s<br>
       <h1>Top Comment:</h1> %s -- %s<br><br>
    </p>
  </body>
</html>
""" % (subreddits[0],urls[0],titles[0],selftext[0],top_comments_author[0],top_comments[0])

# Record the MIME types of both parts - text/plain and text/html.
#part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
#msg.attach(part1)
msg.attach(part2)
# Send the message via local SMTP server.
mail = smtplib.SMTP('smtp.gmail.com', 587)

mail.ehlo()

mail.starttls()

mail.login('mehulmshah22', 'caLlofdutykavya1')
mail.sendmail(me, you, msg.as_string())
mail.quit()
