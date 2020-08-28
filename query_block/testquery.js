var _bcx=require('./bcx.node.js');

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


bcx.queryBlock({block:'6656802'}).then(res=>{console.log(res);});