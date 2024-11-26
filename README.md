# Description
This script is used to extract Zeek log files from all pcap files inside a directory. The script will create a directory called `zeeklog` in the current directory and store the log files in it. The script utilizes multiprocessing to process the pcap files in parallel and each pcap file will have its own directory to store its own log files.

# Usage
`python get_zeeklog.py -P <path> -N <process_num> [-S <script>]`

# Arguments
`-P, --path`: The **absolute** path to the directory containing pcap files.

`-N, --process_num`: The number of processes to use for parallel processing.

`-S, --script`: The **absolute** path to the zeek script. (optional)

# Example
`python get_zeeklog.py -P /path/to/pcap/files -N 4 -S /path/to/zeek/script`