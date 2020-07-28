# list all contexts
```
icontext ls
```

# switch to context
```
icontext use <server>[:<user>]
```

# switch to default context
```
icontext unuse
```

Note: this command will set

```
IRODS_ENVIRONMENT_FILE=~/.irods/irods_environment.json
IRODS_AUTHENTICATION_FILE=~/.irods/.irodsA
```

# get server and user of current context
```
icontext which
```

# show configuration

## configuration of current context
```
icontext describe
```

## configuration for given server user
```
icontext describe <server> <user>
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
icontext create [OPTIONS] <server> <user>
```

## clone
Clone a configuration. Use *icontext clone* to copy a configuration and then *icontext configure* to
configure the cloned configuration.
```
icontext clone [OPTIONS] <server> <user> <new_server> <new_user>
```

## rename
```
icontext rename <server> <user> <new_server> <new_user>
```

## reconfigure
```
icontext configure [OPTIONS] <server> <user>
```

## activate tab completion and variable export

### For Bash, add this to ~/.bashrc:

```
eval "$(_ICONTEXT_COMPLETE=source_bash icontext)"
```


### For Zsh, add this to ~/.zshrc:
(not supported yet)
```
eval "$(_ICONTEXT_COMPLETE=source_zsh icontext)"
```

### For Fish, add this to ~/.config/fish/completions/foo-bar.fish:
(not supported yet)
```
eval (env _ICONTEXT_COMPLETE=source_fish icontext)
```

## reads
* https://systemdump.io/posts/2017-05-06-openstack-cliff
* https://docs.openstack.org/cliff/latest/user/demoapp.html
