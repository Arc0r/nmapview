from flask import Flask, render_template
import xml.etree.ElementTree as ET
from pathlib import Path

app = Flask(__name__)

def parse_nmap_xml(xml_file):
    """Parse nmap XML file and extract hosts with port information"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    hosts = []
    
    # Find all host elements
    for host_elem in root.findall('host'):
        # Get IP address
        address_elem = host_elem.find('address')
        if address_elem is None:
            continue
        
        ip = address_elem.get('addr')
        
        # Get hostname if available
        hostnames_elem = host_elem.find('hostnames')
        hostname = None
        if hostnames_elem is not None:
            hostname_elem = hostnames_elem.find('hostname')
            if hostname_elem is not None:
                hostname = hostname_elem.get('name')
        
        # Get status
        status_elem = host_elem.find('status')
        status = status_elem.get('state') if status_elem is not None else 'unknown'
        
        # Get ports
        ports = []
        ports_elem = host_elem.find('ports')
        if ports_elem is not None:
            for port_elem in ports_elem.findall('port'):
                port_id = port_elem.get('portid')
                protocol = port_elem.get('protocol')
                
                state_elem = port_elem.find('state')
                port_state = state_elem.get('state') if state_elem is not None else 'unknown'
                port_reason = state_elem.get('reason') if state_elem is not None else ''
                port_reason_ttl = state_elem.get('reason_ttl') if state_elem is not None else ''
                
                service_elem = port_elem.find('service')
                service_name = service_elem.get('name') if service_elem is not None else ''
                service_product = service_elem.get('product') if service_elem is not None else ''
                service_extrainfo = service_elem.get('extrainfo') if service_elem is not None else ''
                service_ostype = service_elem.get('ostype') if service_elem is not None else ''
                service_devicetype = service_elem.get('devicetype') if service_elem is not None else ''
                service_method = service_elem.get('method') if service_elem is not None else ''
                service_conf = service_elem.get('conf') if service_elem is not None else ''
                
                # Get CPE if available
                cpe_elems = []
                if service_elem is not None:
                    for cpe_elem in service_elem.findall('cpe'):
                        cpe_elems.append(cpe_elem.text)
                
                # Get scripts
                scripts = []
                for script_elem in port_elem.findall('script'):
                    script_id = script_elem.get('id')
                    script_output = script_elem.get('output')
                    scripts.append({
                        'id': script_id,
                        'output': script_output
                    })
                
                ports.append({
                    'port': port_id,
                    'protocol': protocol,
                    'state': port_state,
                    'reason': port_reason,
                    'reason_ttl': port_reason_ttl,
                    'service': service_name,
                    'product': service_product,
                    'extrainfo': service_extrainfo,
                    'ostype': service_ostype,
                    'devicetype': service_devicetype,
                    'method': service_method,
                    'conf': service_conf,
                    'cpe': cpe_elems,
                    'scripts': scripts
                })
        
        # Sort ports by port number
        ports.sort(key=lambda x: int(x['port']))

        if not ports:
            status = 'down'
        
        hosts.append({
            'ip': ip,
            'hostname': hostname,
            'status': status,
            'ports': ports
        })
    
    # Sort hosts by IP address
    hosts.sort(key=lambda x: tuple(map(int, x['ip'].split('.'))))
    
    return hosts

def load_all_hosts(xml_dir: Path) -> list:
    """Parse every XML file in the given directory and merge hosts."""
    hosts: list = []

    for xml_path in sorted(xml_dir.glob('*.xml')):
        try:
            hosts.extend(parse_nmap_xml(xml_path))
        except ET.ParseError:
            # Skip files that are not valid Nmap XML exports
            continue

    hosts.sort(key=lambda x: tuple(map(int, x['ip'].split('.'))))
    return hosts


@app.route('/')
def index():
    xml_dir = Path(__file__).parent / 'scans'
    hosts = load_all_hosts(xml_dir)
    return render_template('index.html', hosts=hosts)

if __name__ == '__main__':
    app.run(debug=True)
