ICONTEXT=$( which icontext )

icontext() {
    $ICONTEXT $@
    if [ -e ~/.irods/icontext.env ]
    then
        source ~/.irods/icontext.env
    fi
}

if [ -e ~/.irods/icontext.env ]
then
  source ~/.irods/icontext.env
fi
