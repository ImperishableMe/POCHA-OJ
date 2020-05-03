import subprocess,os,sys,resource

def setlimits():
    print("Setting resource limit in child (pid {})".format(os.getpid()))
    resource.setrlimit(resource.RLIMIT_AS, (2**30, 2**30))
    resource.setrlimit(resource.RLIMIT_CPU, (5,5))

def main():
    args = sys.argv[1:]
    with open(args[1],'r') as fin,open(args[2],'w') as fout :
        
        p = subprocess.Popen([args[0]],stdin=fin,stdout=fout,stderr= subprocess.DEVNULL, preexec_fn = setlimits)
        #p = subprocess.Popen(args)
        p.wait()
        print(p.returncode)
        tmp = resource.getrusage(resource.RUSAGE_CHILDREN)
        total_time = tmp.ru_utime
        total_memory = tmp.ru_maxrss
        print(total_time*1000)
        print(total_memory)

if __name__ == "__main__":
    main()


