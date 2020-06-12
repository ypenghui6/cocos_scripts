-- 私有帮助函数
local func_get_now
local func_incr_metric_counter
local func_get_metric_counter
local func_array_has_item

--[[//存放披萨 NFT 资产数据
    [${nft_asset_id}] //存放披萨 NFT 资产数据
--]]
local tbl_nft_pissas0

--[[//存放披萨 NFT（bounty 预留）资产数据
    [${nft_asset_id}] //存放披萨 NFT 资产数据
--]]
local tbl_nft_pissas1

--[[{//存放卡密 NFT 资产数据
    ${card_type}:[${nft_asset_id}] //存放披萨 NFT 资产数据
}--]]
local tbl_nft_cards

--[[{ //存放预约信息
    ${account_id}:${reservation_time} //预约账户id:预约时间
}--]]
local tbl_reservations

--[[{ //存放披萨订单信息
    ${account_id}:${order_time} //购买账户id:购买时间(如有多条为数组)
}--]]
--local tbl_pissa_orders

--[[{ //存放披萨交易信息
    ${nft_asset_id}:${account_id}} //披萨NFT id:购买账户id
}--]]
local tbl_pissa_deals

--[[{ //存放披萨兑换信息
    ${nft_asset_id}:${account_id} //兑换的披萨 NFT id:购买账户id
}--]]
local tbl_redemptions

--[[{ //存放卡密订单信息
    ${nft_asset_id}:${account_id} //卡密NFT id:购买账户id
}--]]
local tbl_card_orders

--[[{ //存放卡密交易信息
    ${nft_asset_id}:${account_id} //卡密NFT id:购买账户id
}--]]
local tbl_card_deals

--[[ //存放卡密购买者列表
    [${account_id}] //购买账户id
--]]
local tbl_card_buyers

--[[{ //存放产品价格
    ${product_type}:${price} //产品类型(如 pissa):价格
}--]]
local tbl_product_prices

--[[{ //存放计数
    ${metric}:${counter_num} //统计指标:统计数量
}--]]
local tbl_counters

-- 常量
local CNT_INVENTORY_QUALITY = "INVENTORY_QUALITY"
--local BCX_NULL_ACCOUNT = "1.2.3"

--[[ 初始化配置
参数:
    world_view: 创建 NFT 资产的世界观
    payee: 收款账户
    resrv_open_time: 预约开放时间，格式为 %Y-%m-%dT%H:%M:%S
    resrv_close_time: 预约关闭时间，格式为 %Y-%m-%dT%H:%M:%S
    order_open_time: 下单开放时间，格式为 %Y-%m-%dT%H:%M:%S
    order_close_time: 下单关闭时间，格式为 %Y-%m-%dT%H:%M:%S
    redeem_open_time: 披萨兑换开放时间，格式为 %Y-%m-%dT%H:%M:%S
    redeem_close_time：披萨兑换关闭时间，格式为 %Y-%m-%dT%H:%M:%S
--]]
function init(world_view, payee, resrv_open_time, resrv_close_time, order_open_time, order_close_time, redeem_open_time, redeem_close_time)
    assert(chainhelper:is_owner(), 'Unauthorized to init')
    assert(world_view and payee and resrv_open_time and resrv_close_time and order_open_time and order_close_time and redeem_open_time and redeem_close_time, 'Invalid init parameters')
    assert(resrv_open_time < resrv_close_time, "Reserve open time must be less than close time")
    assert(order_open_time < order_close_time, "Order open time must be less than order close time")
    assert(redeem_open_time < redeem_close_time, "Redeem open time must be less than redeem close time")

    read_list = { public_data = {} }
    chainhelper:read_chain()

    -- 【判断只初始化一次】
    --assert(public_data.is_init==nil,'public_data.is_init==nil')
    --public_data.is_init = true
    public_data.is_open = true

    public_data.world_view = world_view
    public_data.payee = payee
    public_data.resrv_open_time = resrv_open_time
    public_data.resrv_close_time = resrv_close_time
    public_data.order_open_time = order_open_time
    public_data.order_close_time = order_close_time
    public_data.redeem_open_time = redeem_open_time
    public_data.redeem_close_time = redeem_close_time

    --- 【初始默认数据】
    public_data.tbl_nft_pissas0 = {}
    public_data.tbl_nft_pissas1 = {}
    public_data.tbl_nft_cards = {}
    public_data.tbl_reservations = {}
    --public_data.tbl_pissa_orders = {}
    public_data.tbl_pissa_deals = {}
    public_data.tbl_card_orders = {}
    public_data.tbl_card_deals = {}
    public_data.tbl_card_buyers = {}
    public_data.tbl_redemptions = {}
    public_data.tbl_product_prices = {}

    public_data.tbl_counters = {}
    public_data.tbl_counters[CNT_INVENTORY_QUALITY] = {}
    
    chainhelper:write_chain()
end

--[[ 批量铸造披萨 NFT 资产
参数:
    count: 数量
    base_describe: 基本描述
    bounty: 是否用于bounty
--]]
function mine_pissa_nft(count, base_describe, for_bounty)
    assert(chainhelper:is_owner(),'Unauthorized to mine pissa NFT')

    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    for i = 1, count do  
        nh_asset_id = chainhelper:create_nh_asset(contract_base_info.owner, "COCOS", public_data.world_view, base_describe, true) 
        if for_bounty then -- 在末尾插入
            table.insert(public_data.tbl_nft_pissas1, nh_asset_id)
        else
            table.insert(public_data.tbl_nft_pissas0, nh_asset_id)
        end
    end

    -- 增加计数
    if (not for_bounty) then
        local tbl_counters = public_data.tbl_counters
        func_incr_metric_counter(tbl_counters[CNT_INVENTORY_QUALITY],"pissa",count)
    end

    -- 写入数据
    write_list = { public_data = {tbl_nft_pissas0=true,tbl_nft_pissas1=true,tbl_counters=true} }
    chainhelper:write_chain();
end

--[[ 批量铸造卡密 NFT 资产
参数:
    card_type: 卡密类型
    count: 数量
    base_describe: 基本描述
--]]
function mine_card_nft(card_type, count, base_describe)
    assert(chainhelper:is_owner(),'Unauthorized to mine card NFT')

    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    if (not public_data.tbl_nft_cards[card_type]) then
        public_data.tbl_nft_cards[card_type] = {}
    end

    for i = 1, count do
        nh_asset_id = chainhelper:create_nh_asset(contract_base_info.owner, "COCOS", public_data.world_view, base_describe, true) 
        table.insert(public_data.tbl_nft_cards[card_type], nh_asset_id)
    end

    -- 增加计数
    local tbl_counters = public_data.tbl_counters
    func_incr_metric_counter(tbl_counters[CNT_INVENTORY_QUALITY],card_type,count)

    -- 写入数据
    write_list = { public_data = {tbl_nft_cards=true, tbl_counters=true} }
    chainhelper:write_chain();
end

--[[ 设置产品价格
参数:
    price_setting_json: 价格配置json，如 {"pissa":1, "${card_type}":5} 表示 pissa 价格为 1 个 COCOS...
--]]
function set_product_prices(price_setting_json)
    assert(chainhelper:is_owner(),'Unauthorized to set product prices')
    assert(price_setting_json,'Invalid empty price setting json')

    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    local tbl_product_prices = cjson.decode(price_setting_json)
    assert(tbl_product_prices,'Bad price setting json')

    -- 写入数据
    public_data.tbl_product_prices = tbl_product_prices
    write_list = { public_data = {tbl_product_prices = true} }
    chainhelper:write_chain();
end

--[[ 预约购买
参数: 无
--]]
function make_reservation()
    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    -- 确认市场未关闭
    assert(public_data.is_open, "Marketplace closed")

    -- 确认预约时间
    local now = func_get_now()
    assert(now >= public_data.resrv_open_time, "Reservation not open yet")
    assert(now < public_data.resrv_close_time , "Reservation already closed")

    local tbl_reservations = public_data.tbl_reservations
    local caller = contract_base_info.caller
    -- 防止重复预约
    assert(not tbl_reservations[caller], 'Reservation already exists')
    tbl_reservations[caller] = now

    -- 写入数据
    write_list = { public_data = {tbl_reservations = true} }
    chainhelper:write_chain();
end

--[[ 下订单购买 NFT
参数: product_type, 产品类型如 pissa
--]]
function make_order(product_type)
    assert(product_type, "Wrong product type")
    assert(product_type ~= "pissa", "Pissa is not for sale now")

    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    -- 确认市场未关闭
    assert(public_data.is_open, "Marketplace closed")

    -- 确认购买时间
    local now = func_get_now()
    assert(now >= public_data.order_open_time , "Order not open yet")
    --assert(now < public_data.order_close_time , "Order already closed")

    -- 确保用户已预约购买
    local tbl_reservations = public_data.tbl_reservations
    local caller = contract_base_info.caller
    assert(tbl_reservations[caller], "No reservation before order pissa NFT")

    -- 防止用户多次购买卡密以及存在该产品类型的卡密
    if (product_type ~= "pissa") then
        assert(public_data.tbl_nft_cards[product_type], "No such NFT card product type")

        local tbl_card_buyers = public_data.tbl_card_buyers
        assert(not func_array_has_item(tbl_card_buyers, caller), "Card NFT can only be bought once")
    end

    -- 防止超卖
    local tbl_counters = public_data.tbl_counters
    local pissa_inventory_num = func_get_metric_counter(tbl_counters[CNT_INVENTORY_QUALITY],product_type)
    assert(pissa_inventory_num > 0, "Sold out")

    -- 获取价格
    local tbl_product_prices = public_data.tbl_product_prices
    assert(tbl_product_prices and tbl_product_prices[product_type], "Price not set yet")

    -- 转账
    local price = tbl_product_prices[product_type] * 1.0 * 100000;
    chainhelper:transfer_from_caller(public_data.payee, price, "COCOS", true)

    if (product_type == "pissa") then -- pissa NFT 发货处理
        local tbl_nft_pissas0 = public_data.tbl_nft_pissas0
        local tbl_pissa_deals = public_data.tbl_pissa_deals

        -- 分配 NFT asset
        local alloc_nft_asset_id = nil
        for _, nft_asset_id in pairs(tbl_nft_pissas0) do
            if (not tbl_pissa_deals[nft_asset_id]) then
                alloc_nft_asset_id = nft_asset_id
                break
            end
        end
        assert(alloc_nft_asset_id, "No pissa NFT avaible for this order")
        tbl_pissa_deals[alloc_nft_asset_id] = caller

        -- 转移 pissa NFT
        chainhelper:transfer_nht_from_owner(caller,alloc_nft_asset_id, true)
    else -- 加入发货队列
        local nft_cards = public_data.tbl_nft_cards[product_type]
        local card_deals = public_data.tbl_card_deals
        local card_order = public_data.tbl_card_orders[product_type]

        -- 分配 NFT asset
        local alloc_nft_asset_id = nil
        for _, nft_asset_id in pairs(nft_cards) do
            if ((card_deals and not card_deals[nft_asset_id]) or (not card_deals)) and ((card_order and not card_order[nft_asset_id]) or (not card_order)) then
                alloc_nft_asset_id = nft_asset_id
                break
            end
        end
        assert(alloc_nft_asset_id, "No card NFT avaible for this order")

        -- 添加入订单队列
        if (not card_order) then
            card_order = {}
            card_order[alloc_nft_asset_id]=caller
            public_data.tbl_card_orders[product_type] = card_order
        else
            card_order[alloc_nft_asset_id]=caller
        end
        -- 保存购买用户id
        table.insert(public_data.tbl_card_buyers, caller)
    end

    -- 减少库存
    func_incr_metric_counter(tbl_counters[CNT_INVENTORY_QUALITY],product_type,-1)

    -- 写入数据
    write_list = { public_data={tbl_pissa_deals=true,tbl_card_orders=true,tbl_counters=true,tbl_card_buyers=true} }
    chainhelper:write_chain();
end

--[[ 卡密订单发货
参数:
    card_type: 卡密类型
    nft_asset_id: NFT 资产的 id
    encrypted_memo: 加密后的memo信息
--]]
function deliver_card_nft(card_type,nft_asset_id,encrypted_memo)
    assert(chainhelper:is_owner(),"Unauthorized to deliver card NFT")
    assert(card_type and nft_asset_id and encrypted_memo, "Invalid card delivery parameters")

    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()
    
    -- 确认订单是否存在
    local card_order = public_data.tbl_card_orders[card_type]
    assert(card_order and card_order[nft_asset_id],"Order does not exist for card delivery")

    -- 写入卡密信息
    chainhelper:nht_describe_change(nft_asset_id, "redeem_code_memo", encrypted_memo, true)
    -- 转移卡密 NFT
    chainhelper:transfer_nht_from_owner(card_order[nft_asset_id],nft_asset_id,true)

    -- 将 NFT 资产从订单队列转移到 deals 队列
    local card_deals = public_data.tbl_card_deals
    if (not card_deals) then
        card_deals = {}
        public_data.tbl_card_deals = card_deals
    end
    card_deals[nft_asset_id]=card_order[nft_asset_id]
    card_order[nft_asset_id]=nil

    -- 写入数据
    write_list = { public_data={tbl_card_deals=true,tbl_card_orders=true} }
    chainhelper:write_chain();
end

--[[ 兑换披萨
参数:
    pissa_nft_id: 披萨 NFT 资产 id
--]]
function redeem_pissa(pissa_nft_id)
    assert(pissa_nft_id, "Wrong pissa NFT id")

    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    -- 确认市场未关闭
    assert(public_data.is_open, "Marketplace closed")

    -- 确认兑换时间
    local now = func_get_now()
    assert(now >= public_data.redeem_open_time, "Redeem not open yet")
    assert(now < public_data.redeem_close_time, "Redeem already closed")

    -- 确认是本合约铸造出来的 NFT
    local tbl_nft_pissas0 = public_data.tbl_nft_pissas0
    local tbl_nft_pissas1 = public_data.tbl_nft_pissas1
    assert(func_array_has_item(tbl_nft_pissas0, pissa_nft_id) or func_array_has_item(tbl_nft_pissas1, pissa_nft_id), "Invalid pissa NFT id");

    -- 确认尚未被兑换
    local tbl_redemptions = public_data.tbl_redemptions
    --assert(not tbl_redemptions[pissa_nft_id], "Pissa NFT already redeemed")
    if (not tbl_redemptions[pissa_nft_id]) then
        -- 写入销毁信息
        chainhelper:nht_describe_change(pissa_nft_id, "discard_time", now, true)
        -- 记录兑换记录
        local caller = contract_base_info.caller
        tbl_redemptions[pissa_nft_id] = caller

        write_list = { public_data={tbl_redemptions=true} }
        chainhelper:write_chain();
    end

    -- 销毁披萨 NFT, 向 NULL_ACCOUNT 转移 NFT
    -- chainhelper:transfer_nht_from_caller(BCX_NULL_ACCOUNT, pissa_nft_id, true)
    
    -- 记录兑换记录
    -- local caller = contract_base_info.caller
    -- tbl_redemptions[pissa_nft_id] = caller
    
    -- 写入数据
    -- write_list = { public_data={tbl_redemptions=true} }
    -- chainhelper:write_chain();
end

--[[ 关闭交易市场
参数:无
--]]
function close()
    assert(chainhelper:is_owner(),"Unauthorized to close")

    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    assert(public_data.is_open, "Marketplace already closed")
    public_data.is_open = false

    -- 写入数据
    write_list = { public_data={is_open=true} }
    chainhelper:write_chain();
end


--[[ 获取当前时间帮助函数
参数: 无
返回: 当前时间，格式为 %Y-%m-%dT%H:%M:%S
--]]
func_get_now=function()
    return date('%Y-%m-%dT%H:%M:%S', chainhelper:time())
end

--[[ 增加计数器
参数: 
    counters_ref: 记录表引用
    metric: 统计指标
    count: 增加数量
--]]
func_incr_metric_counter=function(counters_ref,metric,count)
    local prev_count = counters_ref[metric]
    if (not prev_count) then
        counters_ref[metric] = count
    else
        counters_ref[metric] = prev_count + count
    end

    assert(counters_ref[metric] >= 0, "Bad metric counter operation")
end

--[[ 获取计数器
参数: 
    counters_ref: 记录表引用
    metric: 统计指标
返回：
    返回计数，如果不存在则为0
--]]
func_get_metric_counter=function(counters_ref,metric)
    local prev_count = counters_ref[metric]
    if (not prev_count) then
       return 0
    else
        return prev_count
    end
end

--[[ 检查数组中是否有元素
参数: 
    counters_ref: 记录表引用
    metric: 统计指标
返回：
    返回计数，如果不存在则为0
--]]
func_array_has_item=function(arr,item)
    for index, value in pairs(arr) do
        if value == item then
            return true
        end
    end

    return false
end
