let _bcx=require('./bcx.min.js');

let bcx=_bcx.createBCX({
    default_ws_node:"ws://test.cocosbcx.net",
    ws_node_list:[
        {url:"ws://test.cocosbcx.net",name:"COCOS3.0节点1"},
    ],
    networks:[{
        core_asset:"COCOS",
        chain_id:"1ae3653a3105800f5722c5bda2b55530d0e9e8654314e2f3dc6d2b010da641c5"
    }],
    faucet_url:"http://47.93.62.96:8041",
    auto_reconnect:true,
    check_cached_nodes_data:false
});

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

async function queryAccountOperationsResult(_account){
    var createPromise = new Promise(function(resolve, reject){
        bcx.queryAccountOperations({
            account: _account,
            endId: "1.11.0",
            limit: 10,
            callback:function(res){
                console.info("queryAccountOperations res",res);
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

async function queryDataByIdsResult(_ids){

    var createPromise = new Promise(function(resolve, reject){
        bcx.queryDataByIds ({
            ids:_ids,
            callback:function(res){
                console.info("queryDataByIdsResult res",res);
                console.info("queryDataByIdsResult op res",res.data[0].op);
                console.info("queryDataByIdsResult result res",res.data[0].result);
                console.info("queryDataByIdsResult op res",res.data[1].op);
                console.info("queryDataByIdsResult result res",res.data[1].result);
                console.info("queryDataByIdsResult op res",res.data[2].op);
                console.info("queryDataByIdsResult result res",res.data[2].result);                                
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


async function queryBlockResult(_block){

    var createPromise = new Promise(function(resolve, reject){
        bcx.queryBlock({
            block:_block,
            callback:function(res){
                console.info("queryBlockResult res",res);
                console.info("queryBlockResult transactions res",res.data.transactions);
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

async function consoleResult(){

    //await queryAccountOperationsResult("fee2test")
    //await queryDataByIdsResult(['1.11.834475','1.11.834474','1.11.834473'])
    await queryBlockResult(6770672)

}

consoleResult()
