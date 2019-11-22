#!/bin/sh

bin="cli_wallet"
log=${bin}".log"

pkill ${bin}
sleep 1
nohup ./${bin} --chain-id b2feb319994988be8f89dcf81e38b6d57dc124fda5819fa6004a7e7e2c6f80e9 -s ws://127.0.0.1:9788 -r 127.0.0.1:8047 -d  >> ${log}  2>&1 &
sleep 1

if [ $# -gt 0 ]; then
    curl http://127.0.0.1:8047 -d '{"jsonrpc": "2.0", "method": "set_password", "params": ["123"], "id": 1}' >> ${log}
    curl http://127.0.0.1:8047 -d '{"jsonrpc": "2.0", "method": "unlock", "params": ["123"], "id": 1}' >> ${log}
    curl http://127.0.0.1:8047 -d '{"jsonrpc": "2.0", "method": "import_key", "params": ["nicotest", "5KAUeN3Yv51FzpLGGf4S1ByKpMqVFNzXTJK7euqc3NnaaLz1GJm"], "id": 1}' >> ${log}

else
    curl http://127.0.0.1:8047 -d '{"jsonrpc": "2.0", "method": "unlock", "params": ["123"], "id": 1}' >> ${log}
fi

