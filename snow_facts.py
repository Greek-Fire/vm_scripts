from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import json

# Configuration for vCenter access
vcenter_ip = 'vcenter.lou.land'
username = 'administrator@lou.land'
password = 'Gr33k*G0d7'

def collect_datacenter_info(service_instance):
    data = []
    content = service_instance.RetrieveContent()

    for datacenter in content.rootFolder.childEntity:
        if isinstance(datacenter, vim.Datacenter):
            dclusters = datacenter.hostFolder.childEntity
            for cluster in dclusters:
                if isinstance(cluster, vim.ClusterComputeResource):
                    network_names = [nw.name for nw in cluster.network]
                    datastore_info = [(ds.name, ds.summary.capacity) for ds in cluster.datastore]
                    
                    info = {
                        'datacenter': datacenter.name,
                        'compute_cluster': cluster.name,
                        'network_names': network_names,
                        'datastore_cluster': datastore_info
                    }
                    data.append(info)
    return data

def main():
    # Disabling SSL certificate verification
    context = ssl._create_unverified_context()
    service_instance = SmartConnect(host=vcenter_ip, user=username, pwd=password, sslContext=context)

    try:
        datacenter_info = collect_datacenter_info(service_instance)
        print(json.dumps(datacenter_info, indent=4))
    finally:
        Disconnect(service_instance)

if __name__ == "__main__":
    main()
