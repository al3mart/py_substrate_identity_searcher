# Substrate Identity Searcher

Identity searcher for a Substrate-based chain with the identities pallet installed.

### Context

The identities pallet allows an account owner to register real-world information alongside their account on-chain. This is helpful for validator identification, Council member metadata, and more.

Please read more about substrate based identities at the [official wiki]()https://wiki.polkadot.network/docs/en/learn-identity

## Installation
```
git clone https://github.com/al3mart/substrate_identity_searcher.git
cd substrate_identity_searcher
```
Use of virtualenv is recomended

```
pip install virtualenv
virtualenv .
source bin/activate
pip install substrate-interface
```

And finally run it with a simple `python ./searcher.py [options] arg` 

### Functionality

This searcher is developed in a fairly simple script, that will set a connection with a network node of your election, this node endpoint is provided by the `--endpoint` option, also, user is able to choose a file for caching results by setting the `--cache` option.

**Default Values**:

- endpoint: `http://127.0.0.1:9933`
- cache: `./.identities_cache.json`

So, if user is confortable using the default values there is no need of providing these options.

In the other hand, is mandatory for the user to provide `arg`, from now on `target`, being this one the string to be looked for in the identities' metadata.

At any moment user can run ./python searcher.py <-h, --help> for displaying all the command information.

Running this script will end up retrieving all identities that contain the given `target` at some part of their information fields.

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

It is worth mentioning that when running this script, identities in the result list will not only be the ones with information that completely matches our `target`, but also identities which have information that is not exactly equals to `target`, but contains `target` at some point.

Given the magnitude of the problem, and being metadata whatever information owners of those identities wanted to input, it is difficult to find an efficient solution at first sight, and for that, a little cache system is included, so the heavy work is only done once.

## Features
- inputting `target` return all identities with `target` anywhere in any of their fields.
- inputting `filter:target` filter by `filter` field only, and return all identities with `target` anywhere in their `filter` field.
- partial matches are included, e.g. target "bob" will match with identities containing "bobamazoo".
- Persistent cache system to speed up repetitive requests.

## Dependencies
- [substrate-interface](https://github.com/polkascan/py-substrate-interface)

## Possible upgrades & ongoing work

- While developing this script I have been able to get a flawless connection with the node I have been using, a local polkadot node by running the latest polkadot binary with `--dev` flag, but it has not been the same when connecting to live networks, as I have been receiving [Err(UnsafeRpcError)](https://substrate.dev/rustdocs/v2.0.0/sc_rpc_api/enum.DenyUnsafe.html), and for the time being I still don't know the cause of that denial.

- Identities request could be done in a separate thread
