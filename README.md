# Substrate Identity Searcher

Identity searcher for a Substrate-based chain with the identities pallet installed.

### Context

The identities pallet allows an account owner to register real-world information alongside their account on-chain. This is helpful for validator identification, Council member metadata, and more.

Please read more about substrate based identities at the [official wiki]()https://wiki.polkadot.network/docs/en/learn-identity

### Functionality

This searcher is developed in a fairly simple API way using Flask, and will wait for GET requests at path `/search/<target>`, being `target` a string that will be looked for within identities metadata.

This request will end up retrieving all identities that contain the given `target` at some part of their information fields.

Notice that `target` can not only contain a simple string, but also an identity information field filter, being the existing fields at the moment of writing the following ones:
- additional
- display
- legal
- web
- riot
- email
- pgpFingerprint
- image
- twitter

Filters can be express within target like this `filter:str_to_be_found`. Only accepting one field filter for the moment.

It is worth mentioning that when requesting for a search, identities in the result list will not only be the ones with information that completely matches our `target`, but also identities which have information that is not exactly equals to `target`, but contains `target` at some point.

Given the magnitude of the problem, and being metadata whatever information owener of those identities wanted to input, it is difficult to find an efficient solution at first sight, and for that, a little cache system is included into the API, so the heavy work is only done once.

## Features
- inputting `target` return all identities with `target` anywhere in any of their fields.
- inputting `filter:target` filter by `filter` field only, and return all identities with `target` anywhere in their `filter` field.
- partial matches are included, e.g. target "bob" will match with identities containing "bobamazoo".
- Cache system to speed up repetitive requests.

## Dependencies
- [Flask](https://palletsprojects.com/p/flask/)
- [substrate-interface](https://github.com/polkascan/py-substrate-interface) (not in use right now)

## Installing
```
git clone https://github.com/al3mart/substrate_identity_searcher.git
cd substrate_identity_searcher
```
Use of virtualenv is recomended

```
pip install virtualenv
virtualenv ./
pip install flask
pip install substrate-interface
export FLASK_APP=searcher.py
```

If we want to activate flask's development mode and have debug: `export FLASK_ENV=development`

And finally run it with a simple `flask run` 


## Future Work

At the time of writing I have not being able, using the python library substrate-interface, to retrieve a list of every indentity existing in a substrate network. So, for showcasing the job done I got the identities list from Polkadot JS Apps Developer JavaScript interface, and later save the result in identities.py file.
The idea is that the API could be able to update the identity list by its own, and keeping track if the new identity list received has any update, and therefore cache has to be updated too.
