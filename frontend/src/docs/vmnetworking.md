---
id: networking
---

# VM Networking

Our network infrastructure is a bit different from a traditional hosting provider. VMs have static addresses, but have no static gateway. Instead, each VM selects the "best fit" gateway for itself, using ICMP echo broadcasts.

To learn more, check out our [blog post](https://arm-64.com/post/infrastructure-overview) for an overview of the infrastructure architecture.
