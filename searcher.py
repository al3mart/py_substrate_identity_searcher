# This should be a request for the identities in the network's state data
id_list = [
        ['0x2aeddc77fe58c98d50bd37f1b90840f9cd7f37317cd20b61e9bd46fab87047140a2672fe736d19284a2d91e49e215e207dc6f70d8b1dbcbb1caf9168b5209149ddea4c35ba1f345b',
            {'judgements':[],
            'deposit':10000000000000,
            'info':{
                'additional':[],
                'display':{'Raw':'0x44656c6567614e6574776f726b73'},
                'legal':{'Raw':'0x44656c6567614e6574776f726b73'},
                'web':{'Raw':'0x68747470733a2f2f64656c6567612e696f'},
                'riot':{'None':None},
                'email':{'Raw':'0x64656c6567614070726f746f6e6d61696c2e636f6d'},
                'pgpFingerprint':None,
                'image':{'None':None},
                'twitter':{'None':None}
                }
            }
        ],
        ['0x2aeddc66fe58c98d50bd37f1b90840f9cd7f37317cd20b61e9bd46fab87047140b1f48e194c65da836a8d9cd83adc53fe0cb6cd66dba40838269dcba9c1e0833b67dcb6477ae5d29', {'judgements':[[0,{'KnownGood':None}]],'deposit':10000000000000,'info':{'additional':[],'display':{'Raw':'0xf09f8dba2047617620f09fa583'},'legal':{'Raw':'0x44656c6567614e6574776f726b73'},'web':{'Raw':'0x676176776f6f642e636f6d'},'riot':{'Raw':'0x406761766f66796f726b3a6d61747269782e7061726974792e696f'},'email':{'Raw':'0x676176696e407061726974792e696f'},'pgpFingerprint':None,'image':{'None':None},'twitter':{'Raw':'0x6761766f66796f726b'}}}],
        ['0x2aeddc77fe58c98d50bd37f1b90840f9cd7f37317cd20b61e9bd46fab87047140b1f48e194c65da836a8d9cd83adc53fe0cb6cd66dba40838269dcba9c1e0833b67dcb6477ae5d29', {'judgements':[[0,{'KnownGood':None}]],'deposit':10000000000000,'info':{'additional':[],'display':{'Raw':'0xf09f8dba2047617620f09fa583'},'legal':{'Raw':'0x476176696e20576f6f64'},'web':{'Raw':'0x676176776f6f642e636f6d'},'riot':{'Raw':'0x406761766f66796f726b3a6d61747269782e7061726974792e696f'},'email':{'Raw':'0x676176696e407061726974792e696f'},'pgpFingerprint':None,'image':{'None':None},'twitter':{'Raw':'0x6761766f66796f726b'}}}]]

matching_ids = {}

id_dict = {account:data for account, data in id_list}

def string_to_hex(text):
    
    text_binary = text.encode(encoding='utf-8')
    text_hex = text_binary.hex()
    
    return text_hex

def find_in_id_list(target, id_dict):

    print('\nLooking for target: {} \n'.format(target))
    for account in id_dict.keys():
        if is_matching_target(target, id_dict[account]['info']):
            matching_ids[target].append(account)

def is_matching_target(target, id_data):
    
    for field, value in id_data.items():

        if value is None:
            print('{} is None'.format(value))
            continue

        elif target in value:
            print('Checking if {} is in {}'.format(target, value))
            print('Found in field {}!'.format(field))
            return True

        elif type(value) is dict:
            print('value is a dict, then, checking in {}'.format(value.values()))
            for val in value.values():
                if val is None: continue
                if target in val:
                    print('Found in field {}!'.format(field))
                    return True

        elif type(value) is list:
            print('value is a dict, then, checking in {}'.format(value))
            for val in value:
                if target in val:
                    print('Found in field {}!'.format(field))
                    return True



target = string_to_hex(input('Input the information to be looked for in the network existing identities: '))
matching_ids[target] = []

find_in_id_list(target, id_dict)

print(matching_ids)                
