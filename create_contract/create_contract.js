let _bcx=require('./bcx.node.js');

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

var contractName = "contract.cocos1"


var contractData = "local SUIT_SPADE = 1\n"     +
"local SUIT_HEART = 2\n"        +
"local SUIT_CLUB = 3\n"     +
"local SUIT_DIAMOND = 4\n"      +
" \n"       +
"function clear()\n"        +
"    -- assert(chainhelper:is_owner(), 'unauthorized')\n"       +
"\n"        +
"    write_list = {\n"      +
"        public_data = {},\n"       +
"    }\n"       +
"\n"        +
"    public_data = {}\n"        +
"\n"        +
"    chainhelper:write_chain()\n"       +
"end\n"     +
"\n"        +
"local function shuffle()\n"        +
"    local cards = {}\n"        +
"\n"        +
"    local suits = {SUIT_SPADE, SUIT_HEART, SUIT_CLUB, SUIT_DIAMOND}\n"     +
"    for isuit, suit in pairs(suits) do\n"      +
"        for n = 1, 13 do\n"        +
"            cards[13 * (isuit - 1) + n] = tonumber(string.format('%d%02d', suit, n == 1 and 14 or n))\n"       +
"        end\n"     +
"    end\n"     +
"\n"        +
"    for i = 52, 2, -1 do\n"        +
"        local j = chainhelper:random() % i + 1\n"      +
"        cards[i], cards[j] = cards[j], cards[i]\n"     +
"    end\n"     +
"\n"        +
"    return cards\n"        +
"end\n"     +
"\n"        +
"function dealCards()\n"        +
"    -- assert(chainhelper:is_owner(), 'unauthorized')\n"       +
"\n"        +
"    local cards = shuffle()\n"     +
"\n"        +
"    local public_cards = {cards[1], cards[2], cards[3], cards[4], cards[5]}\n"     +
"    local cowboy_cards = {cards[6], cards[7]}\n"           +
"    local bull_cards = {cards[8], cards[9]}\n"         +
"\n"            +
"    read_list = {\n"           +
"        public_data = {},\n"           +
"    }\n"           +
"    chainhelper:read_chain()\n"            +
"\n"            +
"    public_data.round_id = (public_data.round_id or 0) + 1\n"          +
"    public_data.public_cards = public_cards\n"         +
"    public_data.cowboy_cards = cowboy_cards\n"         +
"    public_data.bull_cards = bull_cards\n"         +
"    write_list = {\n"          +
"        public_data = {},\n"           +
"    }\n"           +
"\n"            +
"    chainhelper:write_chain()\n"           +
"\n"            +
"    local log = cjson.encode(public_data)\n"           +
"    chainhelper:log(log)\n"            +
"end"   



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

    //for test pissa datas
    await passwordLogin("5JygARc1DFi2TfepvUKf2S2CMf5MEEiLunzh5n2notpjtK2YkVX")
    await createAndQueryContract(contractName, contractData)
    // await callAndQueryContract("mine_nft", ['cocosnft2020','NFT2020',100,'{"name":"粽子礼盒","icon":"","intro":"","product_code":"NFT2020"}',true,false,false,true])

}

consoleResult()
