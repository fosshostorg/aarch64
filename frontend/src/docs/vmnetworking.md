---
id: networking
---

# Networking

The virtualization network is IPv6 only with translation technologies to enable backwards-compatibility with IPv4 hosts.

VM templates have [Cloudflare's DNS64 servers](https://developers.cloudflare.com/1.1.1.1/support-nat64) configured by default, and our hypervisor fleet all run stateless NAT64 routers onboard that route the 64:ff9b::/96 block for IPv6 to IPv4 translation.

In short, this allows our IPv6-only VMs to access IPv4 only sites. They aren't, however, able to access IPv4 addresses directly, so please use DNS names where possible.

