
import subprocess,os,sys

def main():
    args = sys.argv[1:]
    p = subprocess.Popen(args)
    p.wait()
    print(p.returncode)

if __name__ == "__main__":
    main()