import commands
import sys

# blender colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'



def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, "Usage: pywhois DOMAINNAME"
        sys.exit(1)
    out = commands.getoutput('whois %s' % (sys.argv[1]))
    if 'No match' in out:
        print Colors.OKGREEN + "Available" + Colors.ENDC
    else:
        print Colors.FAIL + "Taken" + Colors.ENDC
        
        
if __name__ == "__main__":
    main()