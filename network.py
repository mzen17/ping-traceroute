# Shared functions for traceroute and ping.
# Implements functions for making ICMP sockets, sending ICMP packets, and receiving ICMP responses.
# Does not use external libraries other than socket and dpkt.
import socket
import dpkt


# Make an ICMP socket using the given TTL and timeout
def make_icmp_socket(ttl: int, timeout: int) -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.settimeout(timeout)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    return s


def send_icmp_echo(sending_socket: socket.socket, payload: str, id: int, seq: int, destination):
    data = dpkt.icmp.ICMP.Echo()
    data.seq = seq
    data.id = id
    data.data = payload.encode('utf-8')

    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO
    icmp.data = data

    sending_socket.sendto(bytes(icmp), (destination, 1))


def recv_icmp_response():
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_socket.settimeout(1)

    try:
        packet, addr = icmp_socket.recvfrom(1000)

        return packet, addr
    except socket.error:
        return None, None
    finally:
        icmp_socket.close()
