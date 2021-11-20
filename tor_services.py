import tor_proxy
import time	

if __name__ == '__main__':
    tor_proxy = tor_proxy.Proxy(connection_port = "9050", 
                  control_port = "9051", 
                  refesh_rate = "60", 
                  exit_nodes = "{SG},{JP}", 
                  exclude_nodes = "{US}", 
                  exclude_exit_nodes = "{KR}")
	# Start tor proxy 
    tor_proxy.start
    
    # Clear tor cache 
    tor_proxy.new_identity
    
    # Stop tor proxy after 1 hour
    time.sleep(60 * 60)
    tor_proxy.stop

    
