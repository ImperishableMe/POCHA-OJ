
import subprocess,os,sys

def main():
    args = sys.argv[1:]
    try :
        p = subprocess.check_output(args,stderr=subprocess.DEVNULL)
        print("0")
    except subprocess.CalledProcessError:
        print("1")

if __name__ == "__main__":
    main()