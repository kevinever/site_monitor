import sre, urllib2, sys, BaseHTTPServer, string, time, os


def parseAddress(input):
        if input[:7] != "http://":
                if input.find("://") != -1:
                        print "Error: Cannot retrive URL, address must be HTTP"
                        sys.exit(1)
                else:
                        input = "http://" + input

        return input

def retrieveWebPage(address):

        req = urllib2.Request(address)
		
        req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')
        req.add_header('Referer', address.strip())
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Accept', 'en-us')


        try:
                web_handle = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
                #print "Cannot retrieve URL: " + str(e.code) + ": " + error_desc
                return 'error'
        except urllib2.URLError, e:
                print "Cannot retrieve URL: " + e.reason[1] + '\n'
                return 'error'
        except:
                print "Cannot retrieve URL: unknown error" + '\n'
                return 'error'
        return web_handle

 

 

def fetchsite(url):

  match_set = set()
  print url
  print '-> Fetching ' + url + '\n'

  address = url
  website_handle = retrieveWebPage(address)
  if website_handle == 'error' : return
  website_text = website_handle.read()

  return website_text

 

try:    
  fp = open(sys.argv[1], 'r')
except:    
  print '[*] error: file does NOT exist.'    
  sys.exit(1)


while 1:
 
  input = fp.readline()
  if not input: break

  website_text = fetchsite(input)
  filename = str(input.strip())
  website_text = str(website_text)

  os.chdir(r'/root/Desktop/web/new-version/1/latest-sign//')
  fw = open(filename[7:],'w')
  fw.write(website_text)

  fw.close()
  time.sleep(1)  
fp.close()





