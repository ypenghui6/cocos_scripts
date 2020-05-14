let _bcx=require('./bcx.min.js');

let bcx=_bcx.createBCX({
    default_ws_node:"ws://127.0.0.1:8649",
    ws_node_list:[
        {url:"ws://127.0.0.1:8649",name:"COCOS3.0节点1"},
    ],
    networks:[{
        core_asset:"COCOS",
        chain_id:"1ae3653a3105800f5722c5bda2b55530d0e9e8654314e2f3dc6d2b010da641c5"
    }],
    faucet_url:"http://47.93.62.96:8041",
    auto_reconnect:true,
    check_cached_nodes_data:false
});

var contractName = "contract.yphui.test67"

var contractData = "function get_nft(hash_or_id)\n" +
"    nft_assert = chainhelper:get_nft_asset(hash_or_id)\n" +
"    chainhelper:log(nft_assert)\n" +
"end"

/*
var contractData = "function test()\n" +
" chainhelper:log('hello world')\n"    +
" end"
*/

bcx.subscribeToRpcConnectionStatus({
    callback:status=>{
        console.info("rpc status",status);
        if(status=="closed"){
            server.close();
        }
    }
})

bcx.subscribeToBlocks({
    callback:res=>{
        // console.info("subscribeToBlocks res",res);
    }
})


async function passwordLogin(){
    var loginPromise = new Promise(function(resolve, reject){
        bcx.privateKeyLogin({
            privateKey:"5KfnxZYsc9VK9oHhjtCRDgnARxqiaEJuqq2uBwSKnVFDEhCu6Mt",//query.loginUserName,
            password:"123",
            callback:function(res){
                console.info("bcx passwordLogin res",res);
            }
        });
    })
    // await loginPromise
}

async function createAndQueryContract(_contractName, _contractData){
    var queryPromise = new Promise(function(resolve, reject){
        bcx.queryContract({nameOrId: _contractName}).then(
            res =>{
                console.info("queryContract res", res);
                if (res.code == 1) {
                    resolve(res.data.contract_data);
                } else {
                    resolve(false);
                }
            });
    })

    var randData = await queryPromise

    if (!randData) {
        var createPromise = new Promise(function(resolve, reject){
            bcx.createContract({
                name:_contractName,
                data:_contractData,
                authority:"COCOS7yE9skpBAirth3eSNMRtwq1jYswEE3uSbbuAtXTz88HtbpQsZf",
                callback:function(res){
                    console.info("contract_create res",res);
                    if (res.code == 1) {
                        resolve(true)
                    } else {
                        reject(false);
                    }
                }
            })
        })

        await createPromise
    }
}

async function callAndQueryContract(_parameter){
    var callPromise = new Promise(function(resolve, reject){
        bcx.callContractFunction({
            nameOrId: contractName,
            functionName: "get_nft",//["1",1000001,'COCOS']
            valueList: [_parameter],//("task1, nicotest,1").split(","),//['4.2.0',{"type":"Employee","employeeId":"551"}],////[{"level":1,"color":"red","clothes":{"size":7}}],//
            onlyGetFee: false,
            callback: function (res) {
                if (res.code == 1) {
                    console.info("callContractFunction res", res);
                    resolve(true)
                } else {
                    reject(false);
                    console.error(res.message);
                }
            }
        })
    })

    var value = await callPromise

    if (value){
        var queryPromise = new Promise(function(resolve, reject){
            bcx.queryContract({nameOrId: contractName}).then(
                res =>{
                    console.info("queryContract res", res);
                    if (res.code == 1) {
                        console.info("callContractFunction res", res);
                        resolve(res.data.contract_data);
                    } else {
                        reject(false);
                        console.error(res.message);
                    }
                });
        })

        var randData = await queryPromise

        if (randData) {
            rands = randData.rand
        }
    }

}

async function consoleResult(){
    await passwordLogin()
    await createAndQueryContract(contractName, contractData)

    await callAndQueryContract("4.2.65")

    await callAndQueryContract("4.2.650")

    await callAndQueryContract("")
}

consoleResult()
