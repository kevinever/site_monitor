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
                error_desc = BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
                #print "Cannot retrieve URL: " + str(e.code) + ": " + error_desc
                print "Cannot retrieve URL: HTTP Error Code", e.code

        except urllib2.URLError, e:
                print "Cannot retrieve URL: " + e.reason[1]

        except:
                print "Cannot retrieve URL: unknown error"

        return web_handle





def fetchsite(url,fw):

  match_set = set()

  print '-> Fetching ' + url + '\n'

  address = url
  website_handle = retrieveWebPage(address)
  website_text = website_handle.read()

  dir = website_handle.geturl().rsplit('/',1)[0]
  if (dir == "http:/"):
        dir = website_handle.geturl()

  matches = sre.findall('<img .*src="(.*?)"', website_text)

  for match in matches:
        if match[:7] != "http://":
                if match[0] == "/":
                        slash = ""
                else:
                        slash = "/"
                match_set.add(dir + slash + match)
                break
        else:
                match_set.add(match)
                break

  match_set = list(match_set)
  match_set.sort()


  for item in match_set:
        fw.write(url + '|' + item + '\n')




try:    
  fp = open(sys.argv[1], 'r')
except:    
  print '[*] error: file does NOT exist.'    
  sys.exit(1)

try:    
  fw = open('test.txt', 'w')
except:    
  print '[*] error: file does NOT exist.'    
  sys.exit(1)

while 1:
 
  input = fp.readline()
  if not input: break

  fetchsite(input,fw)
  time.sleep(1)

fp.close()
fw.close()




