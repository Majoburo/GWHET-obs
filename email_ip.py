import smtplib
import email.utils
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os.path
import datetime
import importlib
import txttwilio
carriers = {'consumer':'@mailmymobile.net','gphi':'@msg.fi.google.com','verizon':'@vtext.com','tmobile': '@tmomail.net', 'att': '@txt.att.net'}
def SendText(content,AlertType='',emailcontent=None,plotfiles=[],datafiles=[],numbers=None,emails=None,recipients='recipients.py'):
    try:
        if not os.path.exists(recipients):
            print("Couldn't find " + recipients)
        pr = importlib.import_module(recipients.split('.')[0])
        if numbers == None:
            numbers = pr.numbers
        if emails == None:
            emails = pr.emails
        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(pr.username, pr.password)
        msg = MIMEMultipart()
        msg['Subject'] = AlertType +' GW ALERT'
        msg['From'] = pr.username
        #msg['Date'] = email.utils.localtime()
        msg.preamble = 'Gravitational Wave Alert'
        msg.attach(MIMEText(content))
        for number,carrier in numbers:
            msg['To'] = number+carriers[carrier]
            txttwilio.sentxt(pr.TW_account_sid, pr.TW_auth_token, number, content)
            #mailserver.sendmail(pr.username, number + carriers[carrier], msg.as_string())
            print("Sent {} to {}.".format(content,number))
        msg = MIMEMultipart()
        msg['Subject'] = AlertType +' GW ALERT'
        msg['From'] = pr.username
        msg.preamble = 'Gravitational Wave Alert'
        if emailcontent == None:
            msg.attach(MIMEText(content,'html'))
        else:
            msg.attach(MIMEText(emailcontent))
        for datafile in datafiles:
            if not os.path.exists(datafile):
                print("Couldn't find " + datafile)
                continue
            with open(datafile) as f:
                attach = MIMEApplication(f.read())
                attach.add_header('Content-Disposition', 'attachment', filename = datafile)
                msg.attach(attach)
        for plotfile in plotfiles:
            if not os.path.exists(plotfile):
                print("Couldn't find " + plotfile)
                continue
            if plotfile.endswith('pdf'):
                with open(plotfile,'rb') as f:
                    attach = MIMEApplication(f.read(),'pdf')
                    attach.add_header('Content-Disposition', 'attachment', filename = plotfile)
                    msg.attach(attach)
            else:
                with open(plotfile,'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-ID', '<{}>'.format(plotfile))
                    msg.attach(img)
        for em in emails:
            mailserver.sendmail(pr.username,em,msg.as_string())
            print("Sent alert to {}.".format(em))
        mailserver.close()
    except:
        print('Error sending email!')

def main():
    #SendText('TEST  ',plotfiles=['LSTs_MS181101ab.pdf','MOLL_GWHET_M2052.pdf'],numbers=[('5125763501','tmobile')],emails=['majoburo@gmail.com'])
    SendText('TEST  ',plotfiles=['LSTs_MS181101ab.pdf','MOLL_GWHET_M2052.pdf'],numbers=[],emails=['rjrosati@utexas.edu'])

if __name__=='__main__':
    main()
