
_bcxjscores=require('bcxjs-cores')
_bcxjsws=require('bcxjs-ws')
// import {PrivateKey,TransactionBuilder} from 'bcxjs-cores';
// import {Apis} from 'bcxjs-ws';

const wifKey = "5Jrw5tb6zDyiG9mnZsxvQALd1FPnuocq6nuGbHST719gJpyERrG";
const pKey = _bcxjscores.PrivateKey.fromWif(wifKey);

_bcxjsws.Apis.instance("http://test.cocosbcx.net", true,10000,undefined,()=>{console.log("test...");}).init_promise.then(
    res => {
        console.log("connection success...");
        let tr = new _bcxjscores.TransactionBuilder();
        tr.add_type_operation("account_update", {
            account: "1.2.265305",
            amount: {
                amount: 1,
                asset_id: "1.3.0"
            },
            new_options: {
                memo_key:"COCOS6WrmiT2LRqfabSbX4Fjzy5aNoXKzt31sptsR6wHRDTvHbWSCkA",
                votes:[],
                extensions:[]
            },
            extensions: {
            }
        });
        // tr.set_required_fees().then(() => {
            tr.add_signer(pKey, pKey.toPublicKey().toPublicKeyString());
            console.log("serialized transaction:", tr.serialize().operations);
            tr
                .broadcast()
                .then(() => {
                    console.log("Broadcast success!");
                })
                .catch(err => {
                    console.error(err);
                });
        // });
    }
);
// _bcxjsws.Apis.close();

/*

ck@ubuntu:~/yp/node_package/test/test2$ node change_memo_1.js 
Unknown chain id (this may be a testnet) 1ae3653a3105800f5722c5bda2b55530d0e9e8654314e2f3dc6d2b010da641c5
connection success...
serialized transaction: [ [ 6,
    { lock_with_vote: undefined,
      account: '1.2.265305',
      owner: undefined,
      active: undefined,
      new_options: [Object],
      extensions: [] } ] ]
Broadcast success!


浏览器查看对应交易记录：
执行成功后：https://testnet.cocosabc.com/txs/tx/80eec0535d86cc7cf98b2535e1c6767be47a6cb08001a444330b766d3a3483dd

*/