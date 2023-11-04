import sys, glob, os, shutil, zipfile, time
from HTMLParser import HTMLParser
from zipfile import ZipFile

class MyHTMLParser(HTMLParser):
    def attrib_matches(self, tag, attrs):
        return [pair for pair in attrs if
            pair[0] == "class" and pair[1] == "content"]

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if self.attrib_matches(tag, attrs) and not self.nesting:
                self.nesting = 1
            elif self.nesting:
                self.nesting += 1
        elif tag == "br" and self.nesting:
            self.outf.write("\n")
        elif tag == "img":
            self.outf.write("\n\n")
            self.outf.write("oneImage")
        elif tag == "span" and attrs[0][1] == "label-name":
            self.nesting = 1
            self.wrap = 1

    def handle_endtag(self, tag):
        if tag == "div" and self.nesting:
            self.nesting -= 1

    def handle_data(self, data):
        if self.nesting:
            if self.wrap:
                self.outf.write("\n\n")
                self.outf.write("label({0})".format(data.strip()))
                self.wrap = 0
            else:
                self.outf.write(data.strip())
    
    def __init__(self, outf):
        HTMLParser.__init__(self)
        self.outf = outf
        self.nesting = 0
        self.wrap = 0

def msg(s):
    print >> sys.stderr, s
    sys.stderr.flush()

def htmlFileToText(inputPath, outputDir):
    basename = os.path.basename(inputPath).replace(".html", ".txt")
    outfname = os.path.join(outputDir, basename)
    with open(inputPath, "r") as inf, open(outfname, "w") as outf:
        html = inf.read()
        parser = MyHTMLParser(outf)
        parser.feed(html)
        
def htmlDirToText(inputDir, outputDir):
    try_rmtree(outputDir)
    try_mkdir(outputDir)
    msg("Building text files in {0} ...".format(outputDir))
    
    for path in glob.glob(os.path.join(inputDir, "*.html")):
        htmlFileToText(path, outputDir)
        
    msg("Done.")
    
def tryUntilDone(action, check):
    ex = None
    i = 1
    while True:
        try:
            if check(): return
        except Exception as e:
            ex = e
                
        if i == 20: break
        
        try:
            action()
        except Exception as e:
            ex = e
            
        time.sleep(1)
        i += 1
        
    sys.exit(ex if ex != None else "Failed")          
        
def try_rmtree(dir):
    if os.path.isdir(dir): msg("Removing {0}".format(dir))

    def act(): shutil.rmtree(dir)        
    def check(): return not os.path.isdir(dir)        
    tryUntilDone(act, check)
        
def try_mkdir(dir):
    def act(): os.mkdir(dir)        
    def check(): return os.path.isdir(dir)        
    tryUntilDone(act, check)
        
def keepZipToText(zipFileName):
    zipFileDir = os.path.dirname(zipFileName)
    takeoutDir = os.path.join(zipFileDir, "Takeout")
    outputDir=os.path.join(zipFileDir, "Text")
    
    try_rmtree(takeoutDir)
    
    if os.path.isfile(zipFileName):
        msg("Extracting {0} ...".format(zipFileName))

    try:
        with ZipFile(zipFileName) as zipFile:
            zipFile.extractall(zipFileDir)
    except IOError as e:
        sys.exit(e)
    translatedKeepDirs = ["Keep", "Notizen"]    
    for dirName in translatedKeepDirs:
	if os.path.isdir(takeoutDir+"/"+dirName): htmlDir = os.path.join(takeoutDir, dirName)

    htmlDirToText(inputDir=htmlDir, outputDir=outputDir)

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
