# nanog-80-hackathon
The codes in this repository were used for the following problem, proposed by students of CU Boulder-ITP:

**Problem statement** : POC for a fully automated configuration of a Tier2 ISP data center with real-time monitoring via a webpage.

Tools to be used:

- Netmiko/NAPALM: Configuration push
- Flask: Webpage
- Jinja2: Config template generation
- IPSec/6to4 tunneling: For encryption and IPv6 connectivity
- DHCPv4/DHCPv6: IP address assignment
- Troubleshooting options: Display OnDemand configuration to the administrator for a Specific node level/Global level
- Cloud: For automated backups of logs and configuration files

**Team Name** : CU-Boulder ITP
**Team Members** : [@Aakashrawal](https://www.linkedin.com/in/aakash-rawal-/) [@Hast Patel](https://www.linkedin.com/in/hastpatel/) [@Mukesh Jaiswal](https://www.linkedin.com/in/mukeshkjaiswal/) [@Nikhil Gadre](https://www.linkedin.com/in/nikhil-gadre/) [@Swati Niture](https://www.linkedin.com/in/swati008/)

**PoC for design:**

![](https://github.com/nikhilgadre/nanog-80-hackathon/blob/main/GNS3_topo.png)

**Assumptions:**

- Configured management network

**Functionalities:**

- Run a web application using Flask to provide a user-friendly interface
- Create configuration files for OSPF, BGP, NAT using Jinja2 templates
- Push configurations onto devices
- Monitor individual devices
- Compare running and golden configurations
- Backup configuration to cloud

**Achievements:**

- Centralized control and monitoring of the network
- One-click configuration and deployment
- Reduction in human errors

**Future work on this project could include:**

- ZTP
- Automated device backups
- Security
  - Firewalls
  - Access Lists
- Redundancy
  - Default gateway
  
**SLides**

(https://drive.google.com/file/d/1RWjprcQw7sdYCnvi2o-bZofuM7ZwnL4T/view?usp=sharing)

**How to use:**

- Enable management interfaces on all the desired devices

- Enable sshv2 on devices

- Install modules listed in the requirements.txt file
- Make changes in the device name, int (Interfaces), network (Network to advertise), area (OSPF area), pid (process id) to the ospf.txt file according to your requirements
- Make changes in the device name, IP (IP address), Interface (Interface), Mask (Network mask), NetworksToAdvertise (Networks to advertise), LocalAS\_Number (AS number of the device), Neighbor\_RemoteAS (AS of the neighbor device), Neighbor\_IP (IP address of neighbor device in neighbor AS) to the bgp.txt file according to your requirements
- Make changes in the intefaceout (NAT outside interfaces), intefacein (NAT inside interfaces), accesslist1 (list of networks to be translated) to the nat.txt file according to your requirements
- To implement IPSec and 6to4 tunneling, change the fields of IP addresses, routes and access lists accordingly for peer formation
- Makes changes to the sshInfo-2.csv file to provide your ssh login credentials
- All other sub scripts should be in the same folder as Automated\_DC.py. The same folder should also contain templates, static folders and all other .txt files
- Run Automated\_DC.py script and browse web page at 127.0.0.1:1234
