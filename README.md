# list all contexts
```
icontext ls
```

# switch to context
```
icontext use <server>[:<user>]
```

# show configuration of (current) context
```
incontext describe
```

```
incontext describe <server>[:<user>]
```

# edit / view notes of context
## server nodes
```
icontext note <server>
```
## user nodes
```
icontext note <server> <user>
```

# create context
## interactive dialog
```
icontext create [OPTIONS]
```

Create options:
* --with-ssl
* --with-pam
* --without-ssl
* --without-pam
* --port <PORT>
* --host <SERVER>

## interactive with server name
```
icontext create [OPTIONS] <server>
```

## interactive with server name and user name
```
context create [OPTIONS] <server> <user>
```

## clone
```
context clone [OPTIONS] <server> <user> <new_server> <new_user>
```

## rename
```
context rename <server> <user> <new_server> <new_user>
```

## reconfigure
```
context configure [OPTIONS] <server> <user>
```

## activate tab completion
eval "$(_ICONTEXT_COMPLETE=source_bash icontext)"

## reads
* https://systemdump.io/posts/2017-05-06-openstack-cliff
* https://docs.openstack.org/cliff/latest/user/demoapp.html
