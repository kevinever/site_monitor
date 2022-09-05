import sre, urllib2, sys, BaseHTTPServer, string, time

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


#####Send email when it detect Web defacement##### 


def sendemail(url):

    fromaddr = "you@gmail.com"
    toaddr = "shin@rw-csirt.rw"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Website" + url+ " has been defaced!!!"

    body = "Website " + url+ " has been defaced!!!" 
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("macgeri12382@gmail.com", "tlsehddms130!")

    server.sendmail(fromaddr, toaddr, text)        
    print "Successfully sent email"
    server.quit()
	 
###############################################################

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
  
  if website_handle == 'error' : return
  
  website_text = website_handle.read()

  matches = website_text.find(signature)

  if matches==-1:
        print '!!' + url + ' has been defaced!!\n'
        sendemail(address)




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


while 1:
  input = fp.readline()
  if not input: 
          fp.seek(0)	
          input = fp.readline()		  
          time.sleep(10)	
     
		  
  str = input.split("|")
  
  try:
      url = str[0]
      signature = str[1]
  except:
      print 'Error'
	  
  try:
      fetchsite(url,signature.strip())
  except :
      print 'Error'
	  
  time.sleep(1)


fp.close()
server.quit()




