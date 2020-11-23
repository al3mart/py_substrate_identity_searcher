from flask import Flask
from flask import render_template
from identities import id_list

global matching_ids
global id_dict 

matching_ids = {}
id_dict = {account:data for account, data in id_list}

app = Flask(__name__)

def string_to_hex(text):
    """ Transforms given string to his hexiadecimal representation """

    text_binary = text.encode(encoding='utf-8')
    text_hex = text_binary.hex()
    # Returning without 0x prefix for enabling substring search
    return text_hex

def find_in_id_list(target, id_dict):
    """ Sets data collection where target is to be looked for
        
        Parameters
        ----------
        target: str
            String to be found in id_dict

        id_dict: dict
            Data collection that will be filtered or used as source to
            look for target
    """

    search_filter, target = set_search_filter(target)

    app.logger.debug('Looking for target: {}'.format(string_to_hex(target)))
    for account in id_dict.keys():
        # If filter is provided search is restricted to given identity field
        if search_filter is None:
            if is_matching_target(string_to_hex(target), id_dict[account]['info']):
                matching_ids[target].append(account)
        else:
            app.logger.debug('Search is filtered by {}'.format(search_filter))
            if is_matching_target(string_to_hex(target), id_dict[account]['info'][search_filter]):
                matching_ids[search_filter+':'+target].append(account)

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
            app.logger.debug('{} is None'.format(value))
            continue

        elif target in value:
            app.logger.debug('Checking if {} is in {}'.format(target, value))
            app.logger.debug('Found in field {}!'.format(field))
            return True

        elif type(value) is dict:
            app.logger.debug('Value is a dict, then, checking in {}'.format(value.values()))
            # Looping through is required for sebstring search
            for val in value.values():
                if val is None: continue
                if target in val:
                    app.logger.debug('Found in field {}!'.format(field))
                    return True

        elif type(value) is list:
            app.logger.debug('Value is a list, then, checking in {}'.format(value))
            # Looping through is required for sebstring search
            for val in value:
                if target in val:
                    app.logger.debug('Found in field {}!'.format(field))
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
    app.logger.debug(filtered_target)
    if len(filtered_target) > 1:
        return filtered_target[0], filtered_target[1]
    return None, target


@app.route('/search/<string:target>', methods=['GET'])
def search(target):
    """ Entry point, renders a simple html with search result """
    
    # Check cache is case request has been already done
    if target in matching_ids:
        app.logger.debug('Returning from cache')
        return render_template('search.html', account_list=matching_ids[target])
    
    matching_ids[target] = []

    # Look for identites containing target metadata
    find_in_id_list(target, id_dict)

    app.logger.debug(matching_ids)
    return render_template('search.html', account_list=matching_ids[target])
