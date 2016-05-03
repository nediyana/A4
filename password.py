import imaplib, email, getpass
from email.utils import getaddresses
from mailbot import MailBot, register, Callback

# Email settings
imap_server = 'imap.gmail.com'
imap_user = 'nediyana_daskalova@brown.edu'
# imap_password = getpass.getpass()
imap_password = 'oynjexpnxurqvtnp'


#mailbot = MailBot(imap_server, imap_user, imap_password)

#class MyCallback(Callback):

#    def trigger(self):
#        print("Mail received: {O}".format(self.subject))


# register your callback
#register(MyCallback)

# check the unprocessed messages and trigger the callback
#mailbot.process_messages()



# Connection
imap_conn = imaplib.IMAP4_SSL(imap_server)
(retcode, capabilities) = imap_conn.login(imap_user, imap_password)

# Specify email folder
# print conn.list()
# conn.select("INBOX.Sent Items")
# conn.select("INBOX.Archive", readonly=True)
# imap_conn.select('INBOX',readonly=True)

imap_conn.select('[Gmail]/All Mail',readonly=True)

# Search for email ids between dates specified
result, data = imap_conn.uid('search', None, '(SINCE "01-Jan-2014" BEFORE "05-May-2016")')
# Download headers
uids = data[0].split()
result, data = imap_conn.uid('fetch', ','.join(uids), '(BODY[HEADER.FIELDS (MESSAGE-ID IN-REPLY-TO FROM TO CC DATE SUBJECT)])')
# Where data will be stored
raw_file = open('all_mail.csv', 'w')
# Header for TSV file
raw_file.write("Message-ID,Date,Subject,In-Reply-To,From,To,Cc\n")

# Parse data and spit out info
for i in range(0, len(data)):
     
    # If the current item is _not_ an email header
    if len(data[i]) != 2:
        continue
     
    # Okay, it's an email header. Parse it.
    msg = email.message_from_string(data[i][1])
    mids = msg.get_all('message-id', None)
    mdates = msg.get_all('date', None)
    senders = msg.get_all('from', [])
    receivers = msg.get_all('to', [])
    subject = msg.get_all('subject', [])
    reply_to = msg.get_all('in-reply-to', None)
    # references= msg.get_all('references', [])

    ccs = msg.get_all('cc', [])
     
    row = "," if not mids else mids[0] + ","
    row += "," if not mdates else mdates[0] + ","
    row += "," if not subject else subject[0] + ","
    row += "," if not reply_to else reply_to[0] + ","

    # Only one person sends an email, but just in case
    for name, addr in getaddresses(senders):
        row += "from "+addr + " "
    row += ","
     
    # Space-delimited list of those the email was addressed to
    for name, addr in getaddresses(receivers):
        row += "to "+addr + " "
    row += ""
     
    # # GET REFERENCES
    # for email_id in references:
    #     row += email_id + " "
    # row += "\t"

    # Space-delimited list of those who were CC'd
    for name, addr in getaddresses(ccs):
        row += addr + " "
     
    row += "\n"
     
    # Just going to output tab-delimited, raw data.
    raw_file.write(row)
# Done with file, so close it
raw_file.close()