import os,argparse
import subprocess
import time
from multiprocessing import Process

fastp="/staging/software/fastp"
dragen="/opt/dragen/4.5.4/bin/dragen"
parser = argparse.ArgumentParser("dragen 5-base")
parser.add_argument("-p1","--pe1",type=str,required=True,help="R1 fastq")
parser.add_argument("-p2","--pe2",type=str,required=True,help="R2 fastq")
parser.add_argument("-r","--ref",type=str,required=True,help="hash table directory")
parser.add_argument("-p","--prefix",type=str,required=True,help="prefix for output files")
parser.add_argument("-u","--UMI",type=str,choices=["T","F"],help="remove UMI from reads",required=True)
parser.add_argument("-o","--outdir",type=str,required=True,help="output directory")
args = parser.parse_args()

args.outdir = os.path.abspath(args.outdir)
args.pe1 = os.path.abspath(args.pe1)
args.pe2 = os.path.abspath(args.pe2)
args.ref = os.path.abspath(args.ref)

start = time.time()
if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)
out = args.outdir + "/" + args.prefix
def shell_run(x):
    subprocess.check_call(x, shell=True)

dragen=(f'{dragen} -f -r {args.ref} --output-directory {args.outdir} --output-file-prefix {args.prefix} '
         f'--RGSM illumina --RGID {args.prefix} '
         f'--enable-map-align true --enable-map-align-output true --enable-sort true --enable-duplicate-marking true '
         f'--methylation-conversion illumina --methylation-generate-cytosine-report true --methylation-compress-cx-report true '
         f'--enable-variant-caller true --enable-sv true --enable-cnv true --cnv-enable-self-normalization true ')

if args.UMI == "T":
    if not os.path.exists(f"{args.outdir}/fastp"):
        os.makedirs(f"{args.outdir}/fastp")
    cmd = (f'cd {args.outdir}/fastp && {fastp} -i {args.pe1} -I {args.pe2} '
           f'-Q -L -A -G '# disable:length filter、Quality filtering、Adapter trimming、polyG tail trimming
           f'--thread 64 -U --umi_loc per_read --umi_len 7 --umi_skip 1 -o {args.prefix}.umi.1.fq -O {args.prefix}.umi.2.fq --length_required 75')
    subprocess.check_call(cmd, shell=True)
    string = {}
    string["a"] = f'cd {args.outdir}/fastp && sed -E \'1~4s/(:[ACGTN]+)_([ACGTN]+)/\\1+\\2/\' < {args.prefix}.umi.1.fq |pigz -c -p 32 >{args.prefix}_S1_R1_001.fastq.gz && rm {args.prefix}.umi.1.fq fastp.html fastp.json'
    string["b"] = f'cd {args.outdir}/fastp && sed -E \'1~4s/(:[ACGTN]+)_([ACGTN]+)/\\1+\\2/\' < {args.prefix}.umi.2.fq |pigz -c -p 32 >{args.prefix}_S1_R2_001.fastq.gz && rm {args.prefix}.umi.2.fq'
    p1 = Process(target=shell_run, args=(string["a"],))
    p2 = Process(target=shell_run, args=(string["b"],))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    dragen+=f'--fastq-file1 {args.outdir}/fastp/{args.prefix}_S1_R1_001.fastq.gz --fastq-file2 {args.outdir}/fastp/{args.prefix}_S1_R2_001.fastq.gz'
else:
    dragen+=f'--fastq-file1 ${args.pe1} --fastq-file2 ${args.pe2}'
print(dragen)
p1 = subprocess.Popen(dragen, shell=True)
p1.wait()
########Dragen report
report=f'/usr/bin/dragen-reports -f -d {args.outdir} -o {args.outdir}/report.html -m /opt/dragen-reports/manifests/methylation.json'
print(report)
subprocess.check_call(report, shell=True)

end=time.time()
print(f"\nSampleID {args.prefix}:Elapse time is {(end-start)} seconds\n")