import sys, glob, os
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def attrib_matches(self, tag, attrs):
        return [pair for pair in attrs if
                pair[0] == self.attrib and pair[1] == self.attribVal]    

    def handle_starttag(self, tag, attrs):
        if tag == self.tag:
            if self.attrib_matches(tag, attrs):
                self.nesting = 1
            elif self.nesting:
                self.nesting += 1
        elif tag == "br" and self.nesting:
            self.outf.write("\n")

    def handle_endtag(self, tag):
        if tag == self.tag and self.nesting:
            self.nesting -= 1
            
    def handle_data(self, data):
        if self.nesting:
            self.outf.write(data.strip())
    
    def __init__(self, outf, tag, attrib, attribVal):
        HTMLParser.__init__(self)
        self.outf = outf
        self.tag = tag
        self.attrib = attrib
        self.attribVal = attribVal
        self.nesting = 0

def htmlFileToText(fname, outputDir, tag, attrib, attribVal):
    outfname = "{0}/{1}".format(outputDir, fname.replace(".html", ".txt"))
    with open(fname, "r") as inf, open(outfname, "w") as outf:
        html = inf.read()
        parser = MyHTMLParser(outf, tag, attrib, attribVal)
        parser.feed(html)

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

def main():
    try:
        cmd, dir, tag, attrib, attribVal = sys.argv
    except ValueError:
        sys.exit("Usage: {0} dir tag attrib attribVal".format(sys.argv[0]))
    htmlToText(dir, tag, attrib, attribVal)

if __name__ == "__main__":
    main()