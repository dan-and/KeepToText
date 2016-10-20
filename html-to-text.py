import sys, glob, os

def htmlFileToText(fname, outputDir, tag, attrib, attribVal):
    outFname = "{0}/{1}".format(outputDir, fname.replace(".html", ".txt"))
    with open(fname, "r") as inF, open(outFname, "w") as outF:
        html = inF.read()
        outF.write(html)

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