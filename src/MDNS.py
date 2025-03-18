import socket
from zeroconf import Zeroconf, ServiceInfo

class MDNS:
    def __init__(self, domain, port=5000):
        self.domain = domain
        self.port = port
        self.zeroconf = Zeroconf()

    def get_local_ip(self) -> str:
        """Returns the local IP address of the machine."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # Try connecting to an external server (Google DNS server), we don't care about the response
            s.connect(('10.254.254.254', 1))  # Use an arbitrary external IP to get local IP address
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'  # Fallback if we can't get an external connection
        finally:
            s.close()
        return ip

    def start_mdns_service(self) -> None:
        """Starts the mDNS service and registers it on the local network."""
        local_ip = self.get_local_ip()

        service_info = ServiceInfo(
            "_http._tcp.local.",
            f"{self.domain}._http._tcp.local.",  # Use instance's domain
            addresses=[socket.inet_aton(local_ip)],  # Convert IP to byte format
            port=self.port,  # Use instance's port
            properties={},
            server=f"{self.domain}.local."  # Advertise with domain
        )

        self.zeroconf.register_service(service_info)
        print(f"Service {self.domain}.local registered via mDNS with IP {local_ip} on port {self.port}")

    def stop_mdns_service(self) -> None:
        """Stops the mDNS service and unregisters it."""
        self.zeroconf.close()
        print(f"mDNS service for {self.domain}.local stopped.")