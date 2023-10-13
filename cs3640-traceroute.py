import time
import socket

# Local shared file for convinence; not an external library.
from network import make_icmp_socket, send_icmp_echo, recv_icmp_response
from cmdparse import traceroute_args

# Ping program
if __name__ == "__main__":

    args = traceroute_args()

    # Force everything to be IP for easy comparison when to stop
    dest_ip = socket.gethostbyname(args.destination)
    n_hops = int(args.number_of_hops)

    for i in range(1, n_hops + 1):
        # Make an ICMP socket with TTL of i, and timeout of 1 second.
        icmp_socket = make_icmp_socket(i, 1)

        # Start time for tracking RTT
        start = time.time()

        send_icmp_echo(icmp_socket, "Hello World", i, i, dest_ip)
        
        # Try catch for graceful exception handling.
        try:
            data, addr = recv_icmp_response()
        except KeyboardInterrupt:
            data = None
            addr = None

        if data:
            rtt = time.time() - start
            print(f"{i} destination = {addr[0]}; hop_num = {i}; rtt = {round(rtt * 1000,1)} ms")
        else:
            print(f"{i} * * *")
        if (addr is not None and addr[0] == dest_ip):
            break
