import sys, glob, os
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag        

    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag

    def handle_data(self, data):
        print "Encountered some data  :", data
        
    def __init__(self, outf):
        HTMLParser.__init__(self)
        self.outf = outf

def htmlFileToText(fname, outputDir, tag, attrib, attribVal):
    outfname = "{0}/{1}".format(outputDir, fname.replace(".html", ".txt"))
    with open(fname, "r") as inf, open(outfname, "w") as outf:
        html = inf.read()
        parser = MyHTMLParser(outf)
        parser.feed(html)
        #outF.write(html)

def htmlToText(dir, tag, attrib, attribVal):
    try:
        os.chdir(dir)
    except WindowsError as e:
        sys.exit(e)
    
    outputDir = dir + "/Output"
    
    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)
    
    for fname in glob.glob("*.html"):
        try:
            htmlFileToText(fname, outputDir, tag, attrib, attribVal)
        except WindowsError as e:
            sys.exit(e)
            
        break


def main():
    try:
        cmd, dir, tag, attrib, attribVal = sys.argv
    except ValueError:
        sys.exit("Usage: {0} dir tag attrib attribVal".format(sys.argv[0]))
    htmlToText(dir, tag, attrib, attribVal)

if __name__ == "__main__":
    main()