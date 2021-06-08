---
id: networking
---

# Networking

The virtualization network is IPv6 only, with translation technologies to enable backward compatibility with IPv4 hosts.

Our VM templates have [Cloudflare's DNS64 servers](https://developers.cloudflare.com/1.1.1.1/support-nat64) configured by default, and all of our hypervisor fleets run stateless NAT64 routers onboard that route - the 64:ff9b::/96 block - for IPv6 to IPv4 translation. In short, this allows our IPv6-only VMs to access IPv4-only sites. However, they aren't able to access IPv4 addresses directly, so please use DNS names where possible.

## IPv4 Only Users

Due to each Virtual Machine not having its own public IPv4, we, AArch64, deploy multiple transition mechanisms so that IPv4 only users can access AArch64 VMs.

### Web Proxy

Each hypervisor runs a web proxy to allow IPv4 only users to load websites hosted on Virtual Machines. The proxy is configured in the proxies tab for a project and can take up to 5 minutes to synchronize changes across the cluster. It is powered by Squid and will forward HTTP traffic by Host Header, and HTTPS by SNI. This allows you to host a web server on your VM that works with HTTP and HTTPS, and terminate TLS directly on your machine as if it had IPv4 to begin with. Make sure to set a CNAME pointing towards [POP].proxy.infra.aarch64.com on the relevant domain.

### SSH Jump Server

IPv4-only users wishing to SSH into a virtual machine are about to use our SSH jump server. The user and host should be jump@[POP]0.infra.aarch64.com. For example, to SSH into the root user on the host `root@2001:0db8::aa64`, the SSH jump command is `ssh -J jump@dfw0.infra.aarch64.com root@2001:0db8::aa64`