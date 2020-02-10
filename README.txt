The data produced is mostly random, but with a few
constraints. We want the program to create a file tree with a single
top-level directory called 'dataroot'. Within this directory we want
regular files and sub-directories. The regular files contain lines of
randomly generated text. The lines should be approximately 60
characters long. The number of lines is between 5 and 15, chosen at
random for each file.

The dataroot directory should have a random mix of files and
sub-directories. The sub-directories should also be populated in a
similar manner, with the maximum depth of nesting determined by the first
parameter given to the script on the command line. The number of
entries in each directory is given by a second command line argument.

For example,

$ python2.7 gen-data.py 6 2
$ tree dataroot

dataroot
├── ckk
│   ├── bfkv
│   │   ├── dzlgm
│   │   │   ├── jsvm
│   │   │   │   ├── ghxf
│   │   │   │   └── thl
│   │   │   └── jzhxs
│   │   │       ├── dvjn
│   │   │       └── hwrwvlj
│   │   └── jkgwz
│   │       ├── mrlwkr
│   │       └── nszgprj
│   │           ├── vtl
│   │           └── xxmqxb
│   └── plv
│       ├── lvrvgzk
│       └── snsq
└── rxhnj

12 directories, 6 files
$
$ cat dataroot/ckk/plv/lvrvgzk 
qck xxgc pkb zdt lvpp zhwncxr wjz xgtgqc vncr rmvmjfz dwnfcvs 
vbpdjsm mvzs fgjvzn kqfxj thrqncf hqj kfd gclllsn mzdt mptm 
qdsjsg glr jwdt twkljg smlnz qct ldkn jrkgtwf lhgl bwtpz ccxkx 
cwfhd mjrlnkl vszcgj jjscb llkvtpv vtl dqgp kxfpdv sktc trfrpp 
cbpzc qfllzx mnjmg bqj fdn ksbdcb pwtff bjvw wnnhps jsvf jxzvwb 
tkvdmng jmx wcnd vkvc wbwhsjt cvwz zbjjsc vsg qmbpkg lzp rphsc 
vksld lbls sltbcjm mzx frh crrcf hzgqbhx zxn tvrgv khmxqt gwndd 
$ 
