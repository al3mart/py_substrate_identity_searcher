from optparse import OptionParser
from substrateinterface import SubstrateInterface
import json

""" Setting script usage, options and args parsing """

usage = "usage: %prog [--cache, --endpoint] target"
parser = OptionParser(usage)

parser.add_option('-c', '--cache', dest='cache_file', default='./.identites_cache.json', help='file to use as cache file, uses .json files. Default is ./.identities_cache.json', metavar='CACHE')
parser.add_option('-e', '--endpoint', dest='endpoint', default='http://127.0.0.1:9933', help='endpoint of network node you want to connect to, and retrieve identities from. Default is http://127.0.0.1:9933')

(options, args) = parser.parse_args()

if len(args) != 1:
        parser.error("missing target to search for \n")

""" Initializing node connection & data structures """
substrate = SubstrateInterface(url=options.endpoint)
matching_ids = {}

def find_in_id_list(target, id_list):
    """ Sets data collection where target is to be looked for
        
        Parameters
        ----------
        target: str
            String to be found in id_dict

        id_list: list
            Data collection that will be filtered or used as source to
            look for target

        Returns
        -------
        matching_ids: dict
            dict of ids matching the target
    """
    matching_ids[target] = [] 

    id_dict = {account:data for account, data in id_list}
    search_filter, target = set_search_filter(target)

    for account in id_dict.keys():
        # If filter is provided search is restricted to given identity field
        if search_filter is None:
            if is_matching_target(target, id_dict[account]['info']):
                matching_ids[target].append(account)
        else:
            if is_matching_target(target, id_dict[account]['info'][search_filter]):
                matching_ids[search_filter+':'+target].append(account)

    return matching_ids

def is_matching_target(target, id_data):
    """ Checks if target is contained in given id_data

         Parameters
         ----------
         target: str
            String to be found in id_data

         id_data: iterable
            Data collection where target is going to be looked for

         Returns
         -------
            <True, False>: depending if target is found
    """

    for field, value in id_data.items():        
        if value is None:
            continue

        elif target in value:
            app.logger.debug('Found in field {}!'.format(field))
            return True

        elif type(value) is dict:
            # Looping through is required for sebstring search
            for val in value.values():
                if val is None: continue
                if target in val:
                    return True

        elif type(value) is list:
            # Looping through is required for sebstring search
            for val in value:
                if target in val:
                    return True

def set_search_filter(target):
    """ Set metadata filter if given at request
        
        Parameters
        ----------
        target: str
            Input from seach request

        Returns
        -------
        search_filter: <None, str>
            Filter defined in request, None in case no filter is given
        
        target: str
            Target but filter is stripped out
    """

    filtered_target = target.split(':')
    if len(filtered_target) > 1:
        return filtered_target[0], filtered_target[1]
    return None, target

def search(target):
    """ Entry point, renders a simple html with search result """
    print(target)
    
    cache = {}
        
    id_list = substrate.iterate_map(module='Identity', storage_function='IdentityOf')
    id_list_hash = hash(str(id_list))
    
    try:
        # Try reading cache
        print('>> Leyendo fichero')
        with open(options.cache_file, 'r') as f:
            cache = json.loads(f.read())

    except FileNotFoundError:
        # Create cache file        
        print('>> Escribiendo fichero')
        cache['hash'] = id_list_hash
        cache[target] = find_in_id_list(target, id_list)[target]
        with open(options.cache_file, 'w') as f:
            f.write(json.dumps(cache))

    else:
        # Check if cache is empty
        # Check if identities on chain have been modified since the last request
        # If so, we have to update cache, what will result in doing the full search again
        if 'hash' not in cache or id_list_hash != cache['hash']:
            cache['hash'] = id_list_hash
            cache[target] = find_in_id_list(target, id_list)[target]
            with open(options.cache_file, 'w') as f:
                f.write(json.dumps(cache))
    
    finally:
        # returning identities
        print(cache[target])

search(args[0])
