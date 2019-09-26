from itertools import groupby

#See https://bgpstream.caida.org/v2-beta#api
def get_bgp_fields(line, api_version='v1'):
    """
    #format is: <dump-type>|<elem-type>|<record-ts>|<project>|<collector>|<peer-ASn>|<peer-IP>|
    # <prefix>|<next-hop-IP>|<AS-path>|<origin-AS>|<communities>|<old-state>|<new-state>|<validity-state>
    :param line: BGP RIB entry
    :return: dictionary with fields as keys
    """

    fields = {}

    #BGPReader Version 1
    #Record Format
    # <dump-type>|<dump-pos>|<project>|<collector>|<status>|<dump-time>
    #Elem Format
    # <dump-type>|<elem-type>|<record-ts>|<project>|<collector>|<peer-ASN>|<peer-IP>|<prefix>|<next-hop-IP>|<AS-path>|<origin-AS>|<communities>|<old-state>|<new-state>
    if api_version == 'v1':
        try:
            line = line.split('|')
            fields['time'] = int(line[2].rstrip())
            fields['project'] = line[3].rstrip()
            fields['collector'] = line[4].rstrip()
            fields['peer_asn'] = line[5].rstrip()
            fields['peer_ip'] = line[6].rstrip()
            fields['prefix'] = line[7].rstrip()

            fields['as_path'] = line[9].rstrip()
            fields['origin'] = line[10].rstrip()
            #fields['vstate'] = int(line[14].rstrip())

        except Exception as e:
            print(e)
            print('Exception occured in the following line: ')
            print(line)
            print('---')

            # Return empty dict in case of exception
            fields = {}

    #BGPReader Version 2
    #Record Format
    # <type>|<dump-pos>|<rec-ts-sec>.<rec-ts-usec>|<project>|<collector>|<router>|<router-ip>|<status>|<dump-time>
    #Elem Format
    # <rec-type>|<elem-type>|<rec-ts-sec>.<rec-ts-usec>|<project>|<collector>|<router>|<router-ip>|<peer-ASN>|<peer-IP>|<prefix>|<next-hop-IP>|<AS-path>|<origin-AS>|<communities>|<old-state>|<new-state>
    elif api_version == 'v2':
        try:
            line = line.split('|')
            fields['time'] = float(line[2].rstrip())
            fields['project'] = line[3].rstrip()
            fields['collector'] = line[4].rstrip()

            #fields['router'] = line[5].rstrip()
            #fields['router-ip'] = line[6].rstrip()

            fields['peer_asn'] = line[7].rstrip()
            fields['peer_ip'] = line[8].rstrip()
            fields['prefix'] = line[9].rstrip()

            # fields['next-hop-ip'] = line[10].rstrip()

            fields['as_path'] = line[11].rstrip()
            fields['origin'] = line[12].rstrip()
            fields['communities'] = line[13].rstrip()

            #fields['vstate'] = int(line[16].rstrip())

        except Exception as e:
            print(e)
            print('Exception occured in the following line: ')
            print(line)
            print('---')

            # Return empty dict in case of exception
            fields = {}

    return fields


def remove_prepending_from_as_path(as_path):
    """
    Removes prepending from a path, example:
    A<-B<-C<-C<-C becomes A<-B<-C
    :param as_path: AS path attribute from BGP protocol
    :return: AS path without prepending
    """
    return " ".join([x[0] for x in groupby(as_path.split(' '))])


def is_relevant_line(line, symbols):
    beginning_of_line = line[0] not in symbols
    proper_line = len(line.split('|')) >= 6
    return beginning_of_line and proper_line


def is_valid_bgp_entry(bgp_fields):
    """
    :param bgp_fields: Dictionary with BGP information, such as origin, as_path
    :return: True if origin and as_path are valid values
    """
    if not bgp_fields: #dict is empty as exception occured before while reading the line
        return False
    if bgp_fields['origin'] == "" or bgp_fields['origin'] == "0":
        return False
    if bgp_fields['origin'][0] == '{':
        return False
    if bgp_fields['as_path'] == "":
        return False
    if bgp_fields['prefix'] == "0.0.0.0/0":
        return False
    return True


def find_divergence_point(path1, path2):
    """
    :param path1: AS path
    :param path2: AS path
    :return: Divergence point of paths (index of first AS that's different between paths, starting at origin (0). -1 if
    paths are the same.
    """
    path1 = path1.split(' ')
    path1.reverse()
    path2 = path2.split(' ')
    path2.reverse()
    i = 0
    diverge = False
    while i < len(path1) and i < len(path2):
        if path1[i] != path2[i]:
            diverge = True
            break
        i += 1

    # if i == 0:
    #   raise Exception("Origin is divergence point")

    if diverge:
        return i

    return -1
