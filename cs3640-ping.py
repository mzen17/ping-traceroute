import time

# Local shared file for convinence; not an external library.
from network import make_icmp_socket, send_icmp_echo, recv_icmp_response
from cmdparse import ping_args

# Ping program
if __name__ == "__main__":


    # Parse command args into destination, number of pings, and time to live.
    args = ping_args()


    # Check if args contains the values, otherwise, use defaults
    dest_ip = args.destination if args.destination else print("Error: No destination specified.") and exit()
    num_pings = int(args.ping_count) if args.ping_count else 10000
    ttl = int(args.time_to_live) if args.time_to_live else 64


    # Track success rates with sum, success, and sent.
    # This is enough to find failure rate.
    total_sent = 0
    successful_echos = 0
    sum_of_rtts = 0
    
    
    # Init and reuse this socket for optimization
    icmp_socket = make_icmp_socket(ttl, 1)


    for seq in range(1, num_pings + 1):
        total_sent += 1
        start = time.time()
        send_icmp_echo(icmp_socket, "Hello World", seq, seq, dest_ip)
        

        # Try catch for graceful exception handling in case of error.
        try:
            data, addr = recv_icmp_response()
        except KeyboardInterrupt:
            data = None
            addr = None
        

        ## Check if data was recieved, and if it has the correct payload.
        if data and "Hello World" in str(data):
            rtt = time.time() - start
            sum_of_rtts += rtt
            successful_echos += 1
            print(f"destination = {addr[0]}; icmp_seq = {seq}; icmp_id = {seq}; ttl={ttl}; rtt = {round(rtt * 1000,1)} ms")
        
        


        # Try catch for CTRL+C to exit gracefully. 
        # Sleeps for 1 second to prevent spamming and to allow for variable RTTs.
        try:
            time.sleep(1) 
        except KeyboardInterrupt:
            print()
            break


    if (successful_echos == 0):
        print(f"Unreachable Host. {successful_echos}/{total_sent} packets transmitted successfully.")
    else:
        print(f"Average RTT: {round(sum_of_rtts / successful_echos * 1000, 1)}ms, {successful_echos}/{total_sent} packets transmitted successfully.")