"""
This script is used to get zeek log files from all pcap files inside a directory. 
The script will create a directory called 'zeeklog' in the current directory and store the log files in it. 
The script will use multiprocessing to process the pcap files in parallel. 
The script will create a directory for each pcap file and store the log files in it.

Usage:
    python get_zeeklog.py -P <path> -N <process_num> -S <script>

Arguments:
    -P, --path: The absolute path to the directory containing pcap files.
    -N, --process_num: The number of processes to use for parallel processing.
    -S, --script: The absolute path to the zeek script. (optional)

Example:
    python get_zeeklog.py -P /path/to/pcap/files -N 4 -S /path/to/zeek/script

"""

import os
import argparse
import multiprocessing

parser = argparse.ArgumentParser(description='Get zeek log files from pcap files.')
parser.add_argument('-P', '--path', dest='path', type=str, required=True,help='The absolute path to the directory.')
parser.add_argument('-N', '--process_num', dest='process_num', required=True,type=int, help='The number of processes.')
parser.add_argument('-S', '--script', dest='script', required=False, type=str, help='The absolute path to the zeek script. (optional)')
args = parser.parse_args()


def get_all_files(path:str)->list:
    """
    Get all files in a directory.
    
    Args:
        path (str): The path to the directory.
        
    Returns:
        list: A list of all files in the directory.
    """
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            abs_path = os.path.abspath(os.path.join(r, file))
            files.append(abs_path)
    return files

def get_pcapfile(path:str)->list:
    """
    Get all pcap files in a directory.
    
    Args:
        path (str): The path to the directory.
    """
    pcap_files = []
    files = get_all_files(path)
    for file in files:
        if file.endswith('.pcap'):
            pcap_files.append(file)
    return pcap_files

def get_logfile(pcapfile:str, scirpt:str)->None:
    """
    Get log files from pcap files.
    
    Args:
        pcapfile (str): The path to the pcap file.
        script (str): The path to the script.
    """
    print(f'Processing {pcapfile}...')
    pcapfilename = '.'.join(os.path.basename(pcapfile).split(".")[:-1])
    if scirpt is None:
        os.system(f'mkdir zeeklog/{pcapfilename}; cd zeeklog/{pcapfilename}; zeek -C -r {pcapfile}')
    else:
        os.system(f'mkdir zeeklog/{pcapfilename}; cd zeeklog/{pcapfilename}; zeek -C -r {pcapfile} {scirpt}')
    print(f'{pcapfile} done.')

main_path = args.path
process_num = args.process_num
script_path = args.script
pool = multiprocessing.Pool(processes=process_num)
pcapfiles = get_pcapfile(main_path)

if not os.path.exists('zeeklog'):
    os.system('mkdir zeeklog')

for pcapfile in pcapfiles:
    pool.apply_async(get_logfile, (pcapfile, script_path))

pool.close()
pool.join()
print('All done.')
