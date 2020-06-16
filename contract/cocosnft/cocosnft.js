let _bcx=require('./bcx.node.js');

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

var contractName = "contract.cocosnft2020modified"


var contractData = "function test()\n" +
" chainhelper:log('hello world')\n"    +
" end"


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


async function passwordLogin(_privateKey){
    var loginPromise = new Promise(function(resolve, reject){
        bcx.privateKeyLogin({
            privateKey:_privateKey,//query.loginUserName,
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
                authority:"COCOS6uAYo74uCeLr1jtPE4cZytQZUAA1pXGjG57PPrAm6ohB6Y6SLL",
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

async function callAndQueryContract(_functionName, _parameters){
    var callPromise = new Promise(function(resolve, reject){
        bcx.callContractFunction({
            nameOrId: contractName,
            functionName: _functionName,//["1",1000001,'COCOS']
            valueList: _parameters,//("task1, nicotest,1").split(","),//['4.2.0',{"type":"Employee","employeeId":"551"}],////[{"level":1,"color":"red","clothes":{"size":7}}],//
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
/*    await passwordLogin("5JygARc1DFi2TfepvUKf2S2CMf5MEEiLunzh5n2notpjtK2YkVX")

    await createAndQueryContract(contractName, contractData)
    //(payee, resrv_open_time, resrv_close_time, order_open_time, order_close_time, redeem_open_time, redeem_close_time)
    //[ssssss,2020-06-08T04:00:00,2020-06-21T10:00:00,2020-06-08T02:00:00,2020-06-22T04:00:00,2020-06-08T03:00:00,2020-06-22T05:00:00] 
    await callAndQueryContract("init", ['ssssss','2020-06-08T04:00:00','2020-06-21T10:00:00','2020-06-08T02:00:00','2020-06-22T04:00:00','2020-06-08T03:00:00','2020-06-22T05:00:00'])

    //(world_view, nft_logo, count, base_describe, for_bounty, for_online, for_reservations, for_times)
    //['cocosnft2020','pissas',40,{"name":"披萨2020限量款","icon":"http://cardworld.cocosbcx.net/image/pizza_limited.png","intro":"可通过参加Cocos-BCX社群活动，卡密中心抢购活动以及加密骑士团游戏活动获得，可兑换为实体披萨，价值RMB100元，口味随机。","product_code":"pissa"},false,false,true,false]
    await callAndQueryContract("mine_nft", ['cocosnft2020','pissas',40,'{"name":"披萨2020限量款","icon":"http://cardworld.cocosbcx.net/image/pizza_limited.png","intro":"可通过参加Cocos-BCX社群活动，卡密中心抢购活动以及加密骑士团游戏活动获得，可兑换为实体披萨，价值RMB100元，口味随机。","product_code":"pissa"}',false,false,true,false])
    
    await callAndQueryContract("mine_nft", ['cocosnft2020','pissas',60,'{"name":"披萨2020限量款","icon":"http://cardworld.cocosbcx.net/image/pizza_limited.png","intro":"可通过参加Cocos-BCX社群活动，卡密中心抢购活动以及加密骑士团游戏活动获得，可兑换为实体披萨，价值RMB100元，口味随机。","product_code":"pissa"}',true,false,true,false])
    //[chinamobile30,30,{"name":"中国移动30元充值卡","icon":"http://cardworld.cocosbcx.net/image/mobile_top-up-30.png","intro":"价值RMB50元的移动充值卡，提供卡密。","product_code":"chinamobile30"}]
    //['cocosnft2020','chinamobile30',40,{"name":"中国移动30元充值卡","icon":"http://cardworld.cocosbcx.net/image/mobile_top-up-30.png","intro":"价值RMB50元的移动充值卡，提供卡密。","product_code":"chinamobile30"},false,true,false,false]
    await callAndQueryContract("mine_nft", ['cocosnft2020','chinamobile30',30,'{"name":"中国移动30元充值卡","icon":"http://cardworld.cocosbcx.net/image/mobile_top-up-30.png","intro":"价值RMB30元的移动充值卡，提供卡密。","product_code":"chinamobile30"}',false,true,false,false])
    await callAndQueryContract("mine_nft", ['cocosnft2020','chinamobile50',20,'{"name":"中国移动50元充值卡","icon":"http://cardworld.cocosbcx.net/image/mobile_top-up-50.png","intro":"价值RMB50元的移动充值卡，提供卡密。","product_code":"chinamobile50"}',false,true,false,false])

    await callAndQueryContract("mine_nft", ['cocosnft2020','chinamobile10',50,'{"name":"中国移动10元充值卡","icon":"http://cardworld.cocosbcx.net/image/mobile_top-up-10.png","intro":"价值RMB10元的移动充值卡，提供卡密。","product_code":"chinamobile10"}',true,true,false,true])

    await callAndQueryContract("set_product_prices", ['{"pissas":666,"chinamobile30":60,"chinamobile50":96,"chinamobile10":16}'])

    await callAndQueryContract("make_reservation", ["pissas"])
    
*/
    //another buy a pissa
    /*await passwordLogin("5KfnxZYsc9VK9oHhjtCRDgnARxqiaEJuqq2uBwSKnVFDEhCu6Mt")
    await createAndQueryContract(contractName, contractData)
    await callAndQueryContract("make_reservation", ["pissas"])
    await callAndQueryContract("make_order", ["pissas"])
    */
    //take a pissa
    /*await passwordLogin("5KfnxZYsc9VK9oHhjtCRDgnARxqiaEJuqq2uBwSKnVFDEhCu6Mt")
    await createAndQueryContract(contractName, contractData)
    await callAndQueryContract("redeem_pissa", ["4.2.1161","pissas"])*/

    //another buy a card
    /*await passwordLogin("5KfnxZYsc9VK9oHhjtCRDgnARxqiaEJuqq2uBwSKnVFDEhCu6Mt")
    await createAndQueryContract(contractName, contractData)
    await callAndQueryContract("make_order", ["chinamobile30"])*/
    

    //take a card
    // await passwordLogin("5JygARc1DFi2TfepvUKf2S2CMf5MEEiLunzh5n2notpjtK2YkVX")
    // await createAndQueryContract(contractName, contractData)
    // await callAndQueryContract("deliver_card_nft", ["chinamobile30","4.2.1261",'{"from": "COCOS7MWYTPRpnyJEiWaH8dr6u628Va7x2Jw3Lo97AdbFSQeKMA8wgr","to": "COCOS8KZbjv75M8n2EYkzcjmUpgMye11VH8AQHGuH9J1MQLy1GguvyF","nonce": "13620476881211212058","message": "a0946b9bb0bba64ef469fdd17c9c44f0f01c7305d3cf69affc65979b65ffbc4c"}',false])

    //another buy a pissa
    /*await passwordLogin("5J2SChqa9QxrCkdMor9VC2k9NT4R4ctRrJA6odQCPkb3yL89vxo")
    await createAndQueryContract(contractName, contractData)
    await callAndQueryContract("make_reservation", ["pissas"])
    await callAndQueryContract("make_order", ["pissas"])*/
    
    //take a pissa
    /*await passwordLogin("5J2SChqa9QxrCkdMor9VC2k9NT4R4ctRrJA6odQCPkb3yL89vxo")
    await createAndQueryContract(contractName, contractData)
    await callAndQueryContract("redeem_pissa", ["4.2.1162","pissas"])*/
    
    //set times
/*    await passwordLogin("5JygARc1DFi2TfepvUKf2S2CMf5MEEiLunzh5n2notpjtK2YkVX")
    await createAndQueryContract(contractName, contractData)
    await callAndQueryContract("set_times", ['{"order_close_time":"2020-06-22T05:00:00","order_open_time":"2020-06-08T02:00:00","redeem_close_time":"2020-06-22T05:00:00","redeem_open_time":"2020-06-08T03:00:00","resrv_close_time":"2020-06-21T10:00:00","resrv_open_time":"2020-06-08T06:00:00"}'])
*/



    /*//for test tbl_offline_deals datas
    await passwordLogin("5JygARc1DFi2TfepvUKf2S2CMf5MEEiLunzh5n2notpjtK2YkVX")
    await createAndQueryContract(contractName, contractData)
    await callAndQueryContract("mine_nft", ['cocosnft2020','testOrderData',10,'{"name":"testOrderData","icon":"http://cardworld.cocosbcx.net/image/pizza_limited.png","intro":"可通过参加Cocos-BCX社群活动，卡密中心抢购活动以及加密骑士团游戏活动获得，可兑换为实体披萨，价值RMB100元，口味随机。","product_code":"testOrderData"}',false,false,false,true])
    await callAndQueryContract("set_product_prices", ['{"pissas":36937.68784273785,"chinamobile30":60,"chinamobile50":96,"chinamobile10":16,"testOrderData":1}'])


    await passwordLogin("5J2SChqa9QxrCkdMor9VC2k9NT4R4ctRrJA6odQCPkb3yL89vxo")
    await createAndQueryContract(contractName, contractData)
    await callAndQueryContract("make_order", ["testOrderData"])
    await callAndQueryContract("make_order", ["testOrderData"])
    await callAndQueryContract("make_order", ["testOrderData"])
    await callAndQueryContract("make_order", ["testOrderData"])
    await callAndQueryContract("make_order", ["testOrderData"])*/



    // //for test order datas
    // await passwordLogin("5JygARc1DFi2TfepvUKf2S2CMf5MEEiLunzh5n2notpjtK2YkVX")
    // await createAndQueryContract(contractName, contractData)
    // await callAndQueryContract("mine_nft", ['cocosnft2020','orderData',60,'{"name":"testOrderData","icon":"http://cardworld.cocosbcx.net/image/pizza_limited.png","intro":"可通过参加Cocos-BCX社群活动，卡密中心抢购活动以及加密骑士团游戏活动获得，可兑换为实体披萨，价值RMB100元，口味随机。","product_code":"orderData"}',false,true,false,true])
    // // await callAndQueryContract("set_product_prices", ['{"pissas":36937.68784273785,"chinamobile30":60,"chinamobile50":96,"chinamobile10":16,"testOrderData":1,"orderData":1}'])


    // await passwordLogin("5J2SChqa9QxrCkdMor9VC2k9NT4R4ctRrJA6odQCPkb3yL89vxo")
    // await createAndQueryContract(contractName, contractData)
    // await callAndQueryContract("make_order", ["orderData"])
    // await callAndQueryContract("make_order", ["orderData"])
    // await callAndQueryContract("make_order", ["orderData"])
    // await callAndQueryContract("make_order", ["orderData"])
    // await callAndQueryContract("make_order", ["orderData"])

    //for test pissa datas
    await passwordLogin("5JygARc1DFi2TfepvUKf2S2CMf5MEEiLunzh5n2notpjtK2YkVX")
    await createAndQueryContract(contractName, contractData)
    await callAndQueryContract("mine_nft", ['cocosnft2020','NFT2020',100,'{"name":"粽子礼盒","icon":"","intro":"","product_code":"NFT2020"}',true,false,false,true])

}

consoleResult()
