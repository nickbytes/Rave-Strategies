import os
from dotenv import load_dotenv
import random
from email.message import EmailMessage
import smtplib
import songdata
from songdata import *

load_dotenv(".env")
SENDER = os.environ.get("GMAIL_USER")
PASSWORD = os.environ.get("GMAIL_PASSWORD")

# GENERATE A TRACK TEMPO
# BETWEEN 80 AND 200 BPM
bpm = str(random.randint(8,20)*10)

# WEIGHTED PROBABILITY FOR SONG LENGTH
# 1:00 => 10%
# 2:00 => 20%
# 3:00 => 40%
# 4:00 => 20%
# 5:00 => 10%
length = ["1:00"] + ["2:00"] * 2 + ["3:00"] * 4 + ["4:00"] * 2 + ["5:00"]

genre = random.choice(genre_list)
key = random.choice(key_list)

# WEIGHTED PROBABILITY FOR SYSTEM SELECTION
# SYSTEM 0 => 50% : BIG RIG (ANY SEQUENCER OR NO SEQUENCER)
# SYSTEM 1 => 10% : MIDI DEVICES (CIRKLON OR NERDSEQ OR NO SEQUENCER)
# SYSTEM 2 => 15% : SOUND TOYS (NO SEQUENCER)
# SYSTEM 3 => 15% : STANDALONE (NO SEQUENCER)
# SYSTEM 4 => 10% : HIGH LEVEL (ANY SEQUENCER)
system_weights = [0] * 50 + [1] * 10 + [2] * 15 + [3] * 15 + [4] * 10

system_selection = random.choice(system_weights)
sounds = random.sample(system_list[system_selection], random.randint(1, 3))

sequencer_prepend = ""
sequencer = random.choice(sequencer_list[system_selection])

# IF SYSTEM 0 BIG RIG IS SELECTED, CHECK IF 
# THERE ARE ANY MIDI DEVICES IN SOUND SOURCES
# IF THERE ARE AND THE SEQUENCER IS TELETYPE,
# RANDOMLY RESELECT SEQUENCER FROM SYSTEM 1 SEQUENCER OPTIONS
if system_selection == 0 :
	check = any(item in sounds for item in system_list[1])
	if check is True and sequencer == "Teletype" :
		sequencer = random.choice(sequencer_list[1])

# IF NO SEQUENCER IS SELECTED, DO NOT LIST IT
# IN THE FULL PRINTOUT OF THE RAVE STRATEGY
if sequencer == "none" :
	sequencer = ""
else :
	sequencer_prepend = " sequenced by "

# ASSEMBLE THE RAVE STRATEGY
strategy = "Write a " + bpm + "bpm " + genre + " track in " + key + " using " + " / ".join(sounds) + sequencer_prepend + sequencer + " with a duration of ~" + random.choice(length) + ". \n\nIt should " + random.choice(action_list) + " like " + random.choice(thing_list) + " " + random.choice(context_list) + "."

subject = 'Today\'s Rave Strategy'

def send_email(recipient, subject, body) :
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = recipient
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER, PASSWORD)
    server.send_message(msg)
    server.quit()

send_email("nullsleep@gmail.com", subject="Today\'s Rave Strategy", body=strategy)


# CONSTRUCT THE EMAIL
# gmail_user = 'nullsleep@gmail.com'
# gmail_password = 'wteujzphnxtmbipf'
# sent_from = "RAVE STRATEGIES"
# to = ['nullsleep@gmail.com']
# subject = 'Today\'s Rave Strategy'

# email_text = """\
# From: %s
# To: %s
# Subject: %s

# %s
# """ % (sent_from, ", ".join(to), subject, body)

# # SEND THE EMAIL
# try:
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     server.set_debuglevel(1)
#     server.ehlo()
#     server.login(gmail_user, gmail_password)
#     server.sendmail(sent_from, to, email_text)
#     server.close()
#     print ('Email sent!')
# except:
#     print ('Something went wrong...')