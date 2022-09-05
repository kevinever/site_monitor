import sre, urllib2, sys, BaseHTTPServer

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
                sys.exit(1)
        except urllib2.URLError, e:
                print "Cannot retrieve URL: " + e.reason[1]
                sys.exit(1)
        except:
                print "Cannot retrieve URL: unknown error"
                sys.exit(1)
        return web_handle

if len(sys.argv) < 2:
        print "Usage:"
        print "%s url" % (sys.argv[0])
        sys.exit(1)

match_set = set()

address = parseAddress(sys.argv[1])
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
        else:
                match_set.add(match)

match_set = list(match_set)
match_set.sort()

for item in match_set:
        print item



