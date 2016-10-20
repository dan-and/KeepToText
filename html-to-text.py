import sys

def main():
	try:
		cmd, dir, tag, attrib, attribVal = sys.argv
	except ValueError as e:
		print "Usage:", sys.argv[0], "dir tag attrib attribVal"
		return;
	print(tag)

if __name__ == "__main__":
	main()