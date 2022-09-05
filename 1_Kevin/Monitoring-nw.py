import sre, urllib2, sys, BaseHTTPServer, string, time, difflib, os, httplib
# from twilio.rest import TwilioRestClient


import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


####Send Email###
def sendemail(url):

    fromaddr = "you@gmail.com"
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
    print ("Successfully sent email")
    server.quit()
	
	
def sendsms(url):
   # account = "AC8bcdc58638b52c572ea443aa6d1d0c53"
   # token = "92750f747dc5ba1ab58b210d4183a0d4"
    client = TwilioRestClient(account, token)
    message = client.messages.create(to=phonenumber, from_="+12565761286", body=url+' has been defaced')

def parseAddress(input):
        if input[:7] != "http://":
                if input.find("://") != -1:
                        print ("Error: Cannot retrive URL, address must be HTTP")
                        sys.exit(1)
                else:
                        input = "http://" + input

        return input

def retrieveWebPage(address):
        req = urllib2.Request(address)
		
        req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')
        req.add_header('Referer', address.strip())
		
        try:
                web_handle = urllib2.urlopen(req)
				
        except urllib2.HTTPError as e:
                error_desc = BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
                #print "Cannot retrieve URL: " + str(e.code) + ": " + error_desc
                print ("Cannot retrieve URL: HTTP Error Code", e.code + '\n')
                return 'error'
        except urllib2.URLError as e:
                print ("Cannot retrieve URL: " + e.reason[1] + '\n')
                return 'error'
        except:
                print ("Cannot retrieve URL: unknown error" + '\n')
                return 'error'
        return web_handle



def fetchsite(url):

  match_set = set()

  print ('-> Fetching ' + url.strip() )

  address = url
  website_handle = retrieveWebPage(address)
  
  #If page is not accessible, return
  if website_handle == 'error' : return

  #Parse page content and compare signature
  website_text=''
  website_text = website_handle.read()
  website_handle.close()
  compare(str(website_text), url)


def compare(website_text, url):

  #Read contents from Signiture file 
  os.chdir(r'/root/Desktop/web/old-version/rg')
  fp_filename = url.strip()
  try : 
    fp_signiture = open(fp_filename[7:],'r')
  except : return
  filedata=''
  filedata = str(fp_signiture.readlines())
  fp_signiture.close()


  #Store the downloaded contents into a temp file and read again
  website_text = str(website_text)
  temp = open('temp.txt','w')
  temp.write(website_text)
  temp = open('temp.txt','r')
  temptemp = str(temp.readlines())
  temp.close()
  defacement=0

  #Search signature string in the download contents
  for k in signature:
      if temptemp.find(k) != -1: 
          defacement=1


  #Compare the two contents and extract similarity
  s = difflib.SequenceMatcher(None, filedata, temptemp)

  if s.ratio() < 0.3 :
        defacement=1

  print (s.ratio())
  print ('\n')
  

  #Check If URL is already in Blacklist
  fb.seek(0)
  blacklist = fb.readlines()
  duplication=0
  for i in blacklist:
        if i.strip() == url.strip() : 
              duplication=1
        
  #If web is defaced and is already in Blacklist, it just display alert message
  #If web is defaced and is not in Blacklist, it display alert message and send Email,SMS
  if defacement==1 and duplication==1 :
        print ('!!' + url.strip() + ' has been defaced!!\n')

  elif defacement==1 and duplication!=1 :
        print ('!!' + url.strip() + ' has been defaced!!\n')
        sendemail(url.strip())
        #sendsms(url)
        fb.write(url) 

  else : return



###Starting Point####
###Load Signature and Config File###
if len(sys.argv) < 2:
        print ("Usage:")
        print ("%s signaturefile" % (sys.argv[0]))
        sys.exit(1)

try:    
  fp = open(sys.argv[1], 'r')
except:    
  print ('[*] error: file does NOT exist.'    )
  sys.exit(1)

print ('-> Sccessfully loaded the signature file\n')

try:    
  fc = open('config.txt', 'r')
except:    
  print ('[*] error: file does NOT exist.')
  sys.exit(1)


try:    
  fb = open('blackurl.txt', 'r+')
except:    
  print ('[*] 1error: file does NOT exist.')
  sys.exit(1)  
  
###Parse Config File###
while 1:
   configdata = fc.readline()
   configarry = configdata.split('=')
   if configarry[0].strip() == 'Email' : toaddr=configarry[1].strip().split(',')
   elif configarry[0].strip() == 'Phonenumber' : phonenumber=configarry[1].strip()
   elif configarry[0].strip() == 'ID' : emailid=configarry[1].strip()
   elif configarry[0].strip() == 'Password' : emailpass=configarry[1].strip()
   elif configarry[0].strip() == 'account' : account=configarry[1].strip()
   elif configarry[0].strip() == 'token' : token=configarry[1].strip()
   elif configarry[0].strip() == 'signature' : signature=configarry[1].strip().split(',')
   else : break


###Main Function###   
while 1:
  input = fp.readline()
  
  #When reach the end of signature file, start again

  if not input: 
          fp.seek(0)	
          input = fp.readline()		  
          time.sleep(1)
	 
  
  try:
      fetchsite(input)

  except :
      print ('Fetchsite failed')
	  
  time.sleep(0.1)  

fp.close()
server.quit()




