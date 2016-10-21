import sys, glob, os, shutil, zipfile
from HTMLParser import HTMLParser
from zipfile import ZipFile

class MyHTMLParser(HTMLParser):
    def attrib_matches(self, tag, attrs):
        return [pair for pair in attrs if
                pair[0] == self.attrib and pair[1] == self.attribVal]    

    def handle_starttag(self, tag, attrs):
        if tag == self.tag:
            if self.attrib_matches(tag, attrs) and not self.nesting:
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

def htmlFileToText(inputPath, outputDir, tag, attrib, attribVal):
    basename = os.path.basename(inputPath).replace(".html", ".txt")
    outfname = os.path.join(outputDir, basename)
    with open(inputPath, "r") as inf, open(outfname, "w") as outf:
        html = inf.read()
        parser = MyHTMLParser(outf, tag, attrib, attribVal)
        parser.feed(html)

def htmlDirToText(inputDir, outputDir, tag, attrib, attribVal):
    if os.path.isdir(outputDir):
        shutil.rmtree(outputDir)
    os.mkdir(outputDir)
    
    for path in glob.glob(os.path.join(inputDir, "*.html")):
        htmlFileToText(path, outputDir, tag, attrib, attribVal)
        
def keepZipToText(zipFileName):
    zipFileDir = os.path.dirname(zipFileName)
    takeoutDir = os.path.join(zipFileDir, "Takeout")
    outputDir=os.path.join(zipFileDir, "Text")
    if os.path.isdir(takeoutDir):
        shutil.rmtree(takeoutDir)

    with ZipFile(zipFileName) as zipFile:
        zipFile.extractall(zipFileDir)
        
    htmlDir = os.path.join(takeoutDir, "Keep")
    htmlDirToText(inputDir=htmlDir, outputDir=outputDir,
        tag="div", attrib="class", attribVal="content")

def main():
    try:
        cmd, zipFile = sys.argv
    except ValueError:
        sys.exit("Usage: {0} zipFile".format(sys.argv[0]))
    
    try:
        keepZipToText(zipFile)
    except WindowsError as e:
        sys.exit(e)

if __name__ == "__main__":
    main()