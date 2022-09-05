import sre, urllib2, sys, BaseHTTPServer, string, time


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

  print '-> Fetching ' + url + '\n'

  address = url
  website_handle = retrieveWebPage(address)
  if website_handle == 'error' : return
  website_text = website_handle.read()


  matches = sre.findall('<img .*src="(.*?)"', website_text)

  if len(matches) == 0 : 
        matches = sre.findall('iframe src="(.*?)"', website_text)
  elif len(matches) == 0 : 
        matches = sre.findall('<a href="(.*?)"', website_text)

         
  try:
    return matches[0]
  except:
    return 'error'



try:    
  fp = open(sys.argv[1], 'r')
except:    
  print '[*] error: file does NOT exist.'    
  sys.exit(1)

try:    
  fw = open('signature.txt', 'w+')
except:    
  print '[*] error: file does NOT exist.'    
  sys.exit(1)

while 1:
 
  input = fp.readline()
  if not input: break

  sig = fetchsite(input)
  try:
       fw.write(input.strip() + '|' + sig.strip() + '\n')
  except:
       print 'error'
  time.sleep(1)

fp.close()
fw.close()




