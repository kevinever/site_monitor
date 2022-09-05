import sre, urllib2, sys, BaseHTTPServer, string, time
from twilio.rest import TwilioRestClient


import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


####Send Email###
def sendemail(url):

    fromaddr = "you@gmail.com"
    toaddr = ['shin@rw-csirt.rw','rosemary@rw-csirt.rw','shyaka@rw-csirt.rw','gahongayire@rw-csirt.rw','arielle@rw-csirt.rw','asaph.kimenyi@rw-csirt.rw','ben.nkwaya@rw-csirt.rw','mugisha@rw-csirt.rw','roger@rw-csirt.rw','ali.gapwepwe@rw-csirt.rw','erick@rw-csirt.rw','iglooadmin@rw-csirt.rw','kim@rw-csirt.rw','mun@rw-csirt.rw'',moses.ruzigamanzi@rw-csirt.rw','richard@rw-csirt.rw','paul@rw-csirt.rw','saphir@rw-csirt.rw','alice@rw-csirt.rw']
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ','.join(toaddr)
    msg['Subject'] = "Website " + url+ " has been defaced!!!"

    body = "Website " + url+ " has been defaced!!!" 
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(emailid, emailpass)

    server.sendmail(fromaddr, toaddr, text)        
    print "Successfully sent email"
    server.quit()
	
	
def sendsms(url):
    account = "AC8a17ceb209e844c217c8d3c703652379"
    token = "5cbb220f3a05d8929778615daff43851"
    client = TwilioRestClient(account, token)
    message = client.messages.create(to=phonenumber, from_="+14062852181", body=url+' has been defaced')

def parseAddress(input):
        if input[:7] != "http://":
                if input.find("://") != -1:
                        print "Error: Cannot retrive URL, address must be HTTP"
                        sys.exit(1)
                else:
                        input = "http://" + input

        return input

def retrieveWebPage(address):
        try:
                web_handle = urllib2.urlopen(address)
        except urllib2.HTTPError, e:
                error_desc = BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
                #print "Cannot retrieve URL: " + str(e.code) + ": " + error_desc
                print "Cannot retrieve URL: HTTP Error Code", e.code + '\n'
                return 'error'
        except urllib2.URLError, e:
                print "Cannot retrieve URL: " + e.reason[1] + '\n'
                return 'error'
        except:
                print "Cannot retrieve URL: unknown error" + '\n'
                return 'error'
        return web_handle



def fetchsite(url, signature):

  match_set = set()

  print '-> Fetching ' + url + '\n'

  address = url
  website_handle = retrieveWebPage(address)
  
  #If page is not accessible, return
  if website_handle == 'error' : return
  
  #Parse page content and compare signature
  website_text = website_handle.read()
  matches = website_text.find(signature)
  if matches==-1:
        print '!!' + url + ' has been defaced!!\n'
        fb.seek(0)
        blacklist = fb.readlines()
        for i in blacklist:
            if blacklist[i] == url:
                    return           
        fb.write(url+'\n')         
        sendemail(address)
        sendsms(url)             
 

###Load Signature and Config File###
if len(sys.argv) < 2:
        print "Usage:"
        print "%s signaturefile" % (sys.argv[0])
        sys.exit(1)

try:    
  fp = open(sys.argv[1], 'r')
except:    
  print '[*] error: file does NOT exist.'    
  sys.exit(1)

print '-> Sccessfully loaded the signature file\n'

try:    
  fc = open('config.txt', 'r')
except:    
  print '[*] error: file does NOT exist.'    
  sys.exit(1)

try:    
  fb = open('blackurl.txt', 'r+')
except:    
  print '[*] 1error: file does NOT exist.'    
  sys.exit(1)
  
  
###Parse Config File###
while 1:
   configdata = fc.readline()
   configarry = configdata.split('=')
   if configarry[0].strip() == 'Email' : toaddr=configarry[1].strip()
   elif configarry[0].strip() == 'Phonenumber' : phonenumber=configarry[1].strip()
   elif configarry[0].strip() == 'ID' : emailid=configarry[1].strip()
   elif configarry[0].strip() == 'Password' : emailpass=configarry[1].strip()
  # elif configarry[0].strip() == 'account' : account=configarry[1].strip()
  # elif configarry[0].strip() == 'token' : token=configarry[1].strip()
   else : break

   
###Main Function###   
while 1:
  input = fp.readline()
  
  #When reach the end of signature file, start again
  if not input: 
          fp.seek(0)	
          input = fp.readline()		  
          time.sleep(10)
		  
  #Parse signature     
  str = input.split("|")
  try:
      url = str[0]
      signature = str[1]
  except:
      print 'Error'
	  
  try:
      fetchsite(url,signature.strip())
  except :
      print ''
	  
  time.sleep(1)

fp.close()
server.quit()




