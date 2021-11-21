# Tor

**This python module creates a socks5 connection to TOR. It was adapted from r0oth3x49 tor project.**

[![IMAGE ALT TEXT](https://github.com/ohyicong/Tor/blob/master/images/tor_progress.PNG)]

### ***Features***
1. Auto update IPv4 & IPv6 TOR nodes.
2. Auto generate random password to communicate with TOR
3. Supports highly used features
4. TOR runs in background. Able to start and stop whenever you like!

### ***Requirements***
- Python (2 or 3)

### ***Tested on***
- Windows 7/8/8.1/10.
	
### ***Installation***
You can download the latest version of Tor by cloning the GitHub repository:
<pre><code>git clone https://github.com/r0oth3x49/Tor.git</pre></code>

### ***Usage***
<pre><code>
tor_proxy = tor_proxy.Proxy(connection_port = "9050", 
              control_port = "9051", 
              refesh_rate = "60", 
              exit_nodes = "{UK},{JP}", 
              exclude_nodes = "{US}", 
              exclude_exit_nodes = "{KR}")
# Start tor proxy 
tor_proxy.start

# Clear tor cache 
tor_proxy.new_identity

# Stop tor proxy
tor_proxy.stop
</pre></code>

### ***Arguments***
Field | Required | Description | Defaults
:---  | :---: | :---: | :---
connection_port| Optional | listening port for socks | 9050
control_port| Optional | communication port for tor | 9051
refesh_rate| Optional | frequency to rebuild a tor connection. high frequency improves your annonymity but decrease your network performance | 300 seconds
exit_node | Optional |country ip that you will see when you visit https://api.myip.com/ | when not specified, it uses any available exit nodes
exclude_exit_nodes| Optional | do not use tor nodes from the specified countries | when not specified, it uses any available exit nodes
exclude_nodes | Optional | do not use tor nodes from the specified countries | when not specified, it uses any available nodes



