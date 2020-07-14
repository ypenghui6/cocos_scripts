var _bcx=require('./bcx.node.js');

// var bcx=_bcx.createBCX({
//     default_ws_node:"ws://test.cocosbcx.net",
//     ws_node_list:[
//         {url:"ws://test.cocosbcx.net",name:"COCOS3.0节点1"},
//     ],
//     networks:[{
//         core_a1set:"COCOS",
//         chain_id:"1ae3653a3105800f5722c5bda2b55530d0e9e8654314e2f3dc6d2b010da641c5"
//     }],
//     faucet_url:"http://47.93.62.96:8041",
//     auto_reconnect:true,
//     check_cached_nodes_data:false
// });



async function publishVotes(_bcx,_type="witnesses", _vote_ids, _votes){
    bcx = _bcx;
    bcx.publishVotes({
        type: _type,
        vote_ids: _vote_ids,
        votes: _votes,
        callback:function(res){
            console.info("publishVotes res",res);
        }
    });
}

async function queryVotesResult(_bcx,_account, _type="witnesses"){
    bcx = _bcx;    
    bcx.queryVotes({
        queryAccount: _account,
        type: _type,
        callback:function(res){
            console.info("--------------queryVotesResult res size: ",res.data.length);
            console.info("queryVotesResult res",res);
            var repeat_map = new Map();
            for(i=0;i<res.data.length;i++){
                if(!repeat_map.get(res.data[i]["account_id"])){
                    repeat_map.set(res.data[i]["account_id"],1);
                }else{
                    console.info("++++++++++queryVotesResult repeat data: ",res.data[i]);
                }
            }
        }
    });
}

async function passwordLogin(_privateKey){
    var bcx=_bcx.createBCX({
        default_ws_node:"ws://test.cocosbcx.net",
        ws_node_list:[
            {url:"ws://test.cocosbcx.net",name:"COCOS3.0节点1"},
        ],
        networks:[{
            core_a1set:"COCOS",
            chain_id:"1ae3653a3105800f5722c5bda2b55530d0e9e8654314e2f3dc6d2b010da641c5"
        }],
        faucet_url:"http://47.93.62.96:8041",
        auto_reconnect:true,
        check_cached_nodes_data:false
    });

    await bcx.privateKeyLogin({
        privateKey:_privateKey,//query.loginUserName,
        password:"123"
    }).then(async res =>{
        console.info("bcx passwordLogin res",res);
        await queryVotesResult(bcx,"init1");
        await publishVotes(bcx,"witnesses",["1.2.8"],10);
    });
}


/*
var contractData = "function test()\n" +
" chainhelper:log('hello world')\n"    +
" end"
*/

// bcx.subscribeToRpcConnectionStatus({
//     callback:status=>{
//         console.info("rpc status",status);
//         if(status=="closed"){
//             server.close();
//         }
//     }
// })

// bcx.subscribeToBlocks({
//     callback:res=>{
//         // console.info("subscribeToBlocks res",res);
//     }
// })


// async function publishVotes(_type="witnesses", _vote_ids, _votes){
//     var createPromise = new Promise(function(resolve, reject){
//         bcx.publishVotes({
//             type: _type,
//             vote_ids: _vote_ids,
//             votes: _votes,
//             callback:function(res){
//                 console.info("publishVotes res",res);
//                 if (res.code == 1) {
//                     resolve(true)
//                 } else {
//                     reject(false);
//                 }
//             }
//         })
//     })

//     await createPromise
// }


// async function queryVotesResult(_account, _type="witnesses"){
//     var createPromise = new Promise(function(resolve, reject){
//         bcx.queryVotes({
//             account: _account,
//             type: _type,
//             callback:function(res){
//                 console.info("--------------queryVotesResult res size: ",res.data.length);
//                 // console.info("queryVotesResult res",res);
//                 var repeat_map = new Map();
//                 for(i=0;i<res.data.length;i++){
//                     if(!repeat_map.get(res.data[i]["account_id"])){
//                         repeat_map.set(res.data[i]["account_id"],1);
//                     }else{
//                         console.info("++++++++++queryVotesResult repeat data: ",res.data[i]);
//                     }
//                 }
//                 if (res.code == 1) {
//                     resolve(true)
//                 } else {
//                     reject(false);
//                 }
//             }
//         })
//     })

//     await createPromise
// }

// async function passwordLogin(_privateKey,_callback){
//     var loginPromise = new Promise(function(resolve, reject){
//         bcx.privateKeyLogin({
//             privateKey:_privateKey,//query.loginUserName,
//             password:"123",
//             callback:function(res){
//                 console.info("bcx passwordLogin res",res);
//                 resolve(1);
//             }
//         });
//     })

//     loginPromise.then(function(resolve, reject){
//         queryVotesResult("init1");
//         publishVotes("witnesses",["1.2.6"],16);
//     })
//     //await loginPromise
// }



async function consoleResult(){

    
    // await passwordLogin("5HrSkzMW4rBuZKiU1qR8fhZNKxAKQ4CJv2GNwt4rtXda15ZK4SQ") //ssssss

    // passwordLogin("5KCR24N7ZouvzziYAMzhWFky8XsaTTWQkbneB8GDgjbXNH8N7B2") //ssssss1
    
    // passwordLogin("5JTJbb5XvtCxPR45qexErMrfhhCuDL1jtKqeZokirunVzSWnCWN") //ssssss2

    // passwordLogin("5KjG4ikkNSGpQnLVtrtR1XV57NL9o9EUKeqagAPmMoC7T73zU3g") //ssssss3
    
    // passwordLogin("5KHckQ1xRtR8JmWa7vmGQe5LMv2UpB16ypkVEvQ4oGTS4RPQcy3") //ssssss4
    
    // passwordLogin("5JLRG3EcxNG49bB5TLWHg3oF1ugg951129za923LNEuZgkFF4V8") //ssssss5

    // passwordLogin("5KfnxZYsc9VK9oHhjtCRDgnARxqiaEJuqq2uBwSKnVFDEhCu6Mt") //fee2test

    // pros=[passwordLogin("5HrSkzMW4rBuZKiU1qR8fhZNKxAKQ4CJv2GNwt4rtXda15ZK4SQ"),passwordLogin("5KCR24N7ZouvzziYAMzhWFky8XsaTTWQkbneB8GDgjbXNH8N7B2"),passwordLogin("5JTJbb5XvtCxPR45qexErMrfhhCuDL1jtKqeZokirunVzSWnCWN"),passwordLogin("5KjG4ikkNSGpQnLVtrtR1XV57NL9o9EUKeqagAPmMoC7T73zU3g"),passwordLogin("5KHckQ1xRtR8JmWa7vmGQe5LMv2UpB16ypkVEvQ4oGTS4RPQcy3"),passwordLogin("5JLRG3EcxNG49bB5TLWHg3oF1ugg951129za923LNEuZgkFF4V8"),passwordLogin("5KfnxZYsc9VK9oHhjtCRDgnARxqiaEJuqq2uBwSKnVFDEhCu6Mt")]
    // Promise.all(pros).then((values) => {
    //   console.log(values);
    // });
    
    // _account.queryVotesResult("init2")

    // let keys=["5HrSkzMW4rBuZKiU1qR8fhZNKxAKQ4CJv2GNwt4rtXda15ZK4SQ","5KCR24N7ZouvzziYAMzhWFky8XsaTTWQkbneB8GDgjbXNH8N7B2","5JTJbb5XvtCxPR45qexErMrfhhCuDL1jtKqeZokirunVzSWnCWN","5KjG4ikkNSGpQnLVtrtR1XV57NL9o9EUKeqagAPmMoC7T73zU3g","5KHckQ1xRtR8JmWa7vmGQe5LMv2UpB16ypkVEvQ4oGTS4RPQcy3","5JLRG3EcxNG49bB5TLWHg3oF1ugg951129za923LNEuZgkFF4V8","5KfnxZYsc9VK9oHhjtCRDgnARxqiaEJuqq2uBwSKnVFDEhCu6Mt"]
    // for(i=0;i<1;i++){
    //     await passwordLogin(keys[i]);
    // }

    var bcx=_bcx.createBCX({
        default_ws_node:"ws://test.cocosbcx.net",
        ws_node_list:[
            {url:"ws://test.cocosbcx.net",name:"COCOS3.0节点1"},
        ],
        networks:[{
            core_a1set:"COCOS",
            chain_id:"1ae3653a3105800f5722c5bda2b55530d0e9e8654314e2f3dc6d2b010da641c5"
        }],
        faucet_url:"http://47.93.62.96:8041",
        auto_reconnect:true,
        check_cached_nodes_data:false
    });
    queryVotesResult(bcx,"init0")
}

consoleResult()
