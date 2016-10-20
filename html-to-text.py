import sys, glob, os

def htmlToText(dir, tag, attrib, attribVal):
    try:
        os.chdir(dir)
    except WindowsError as e:
        sys.exit(e)
    
    outputDir = dir + "/Output"
    
    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)
    
    for fname in glob.glob("*.html"):
        print fname

def main():
    try:
        cmd, dir, tag, attrib, attribVal = sys.argv
    except ValueError:
        sys.exit("Usage: {0} dir tag attrib attribVal".format(sys.argv[0]))
    htmlToText(dir, tag, attrib, attribVal)

if __name__ == "__main__":
    main()