# Internal python module for getting CMD args.
# Uses argparse module to cleanly parse

import argparse

def ping_args() -> argparse.Namespace:
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-n", "--ping-count", help="Amount of pings to send.")
    argParser.add_argument("-destination", "--destination", help="Destination to ICMP packets, pings or traceroute.")
    argParser.add_argument("-ttl", "--time-to-live", help="Time-To-Live of ping.")
    args = argParser.parse_args()
    return args

def traceroute_args() -> argparse.Namespace:
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-destination", "--destination", help="Destination to ICMP packets, pings or traceroute.")
    argParser.add_argument("-n_hops", "--number-of-hops", help="Maximum number of hops for tracing.")
    args = argParser.parse_args()
    return args
