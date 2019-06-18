import json
import xlwt
import time

# Protocol Mapping
# https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
proto_mapping = {
    "17": "udp",
    "6": "tcp",
    "1": "icmp"
}

# Return a single port if not range


def port_normalizer(port_range):
    return list(dict.fromkeys(port_range))

# Return protocol name from protocol number


def num_to_name(protocol):
    try:
        return proto_mapping[str(protocol)]
    except:
        return "N/A"


# Return a string with the member of a list separated by ' - '


def normalize(input):
    if not isinstance(input, str):
        return ' - '.join(input)
    else:
        return input

# Write policies and convert to excel


def convert(is_dynamic, policy_file, clusters_file):
    with open('./userupload/{}'.format(clusters_file)) as f:
        clusters = json.load(f)

    with open('./userupload/{}'.format(policy_file)) as f:
        policies = json.load(f)

    # Set ADM name from policy file and appending today date and time
    adm_name = '{}{}'.format(policies['name'], time.strftime("%H%M%S-%d%m%Y"))

    # Init Excel file
    wb = xlwt.Workbook()
    ws = wb.add_sheet(adm_name)
    style0 = xlwt.easyxf('font: name Calibri (Body), color-index red, bold on',
                         num_format_str='#,##0.00')
    style1 = xlwt.easyxf('font: name Calibri (Body), color-index black, bold off; align: wrap on',
                         num_format_str='#,##0.00')
    # Write the first row
    ws.write(0, 0, 'Source', style0)
    ws.write(0, 1, 'Destination', style0)
    ws.write(0, 2, 'Services', style0)

    # Get the endpoints given a cluster name
    def host_list(cluster_name):
        hosts = list()
        for cluster in clusters['clusters']:
            if cluster_name == cluster['name']:
                for node in cluster['nodes']:
                    hosts.append(node['ip'])
        if not hosts:
            # Returning 'any' in case no cluster is found (SCOPE case)
            hosts.append('any')
        return hosts

    # Iterate each policy and write to excel to the right columns
    policy_counter = 0
    for policy in policies['default_policies']:
        policy_counter += 1
        if is_dynamic:
            source = policy['consumer_filter_name']
            destination = policy['provider_filter_name']
        else:
            try:
                source = host_list(policy['consumer_filter_name'])
                destination = host_list(policy['provider_filter_name'])
            except:
                print('Can\'t process data. ADM is Dynamic.')
                quit()
        # Initialize an empty array. This will be where each service will be appended
        services = list()
        for param in policy['l4_params']:
            if 'port' in param:
                protocol = num_to_name(param['proto'])
                port = port_normalizer(param['port'])
                services.append('{} {}'.format(protocol, port))
            else:
                services.append(num_to_name(param['proto']))

        # Write the policy to excel
        ws.write(policy_counter, 0, normalize(source), style1)
        ws.write(policy_counter, 1, normalize(destination), style1)
        ws.write(policy_counter, 2, normalize(services), style1)

    # Save the excel file
    wb.save('{}.xls'.format(adm_name))
    return('{}.xls'.format(adm_name))
