----合约公私钥
----COCOS6uAYo74uCeLr1jtPE4cZytQZUAA1pXGjG57PPrAm6ohB6Y6SLL
----5JdRhtRERcw8xTRBEp2VDgHu8uvhWmrJDdqmKKVXE1dCykZuTkJ

-- 私有帮助函数
local func_get_now
local func_incr_metric_counter
local func_get_metric_counter
local func_array_has_item


--[[nft_logo:{// NFT 资产数据
    ${card_type}:[${nft_asset_id}] 
}--]]
local tbl_nfts

--[[nft_logo:{ //存放预约信息
    ${account_id}:${reservation_time} //预约账户id:预约时间
}--]]
local tbl_reservations

--[[{ //存放披萨订单信息
    ${account_id}:${order_time} //购买账户id:购买时间(如有多条为数组)
}--]]
--local tbl_pissa_orders

--[[nft_logo:{ //存放披萨交易信息
    ${nft_asset_id}:${account_id}} //披萨NFT id:购买账户id
}--]]
local tbl_offline_deals

--[[nft_logo:{ //存放披萨兑换信息
    ${nft_asset_id}:${account_id} //兑换的披萨 NFT id:购买账户id
}--]]
local tbl_redemptions

--[[nft_logo:{ //存放卡密订单信息
    ${nft_asset_id}:${account_id} //卡密NFT id:购买账户id
}--]]
local tbl_online_orders

--[[nft_logo:{ //存放卡密交易信息
    ${nft_asset_id}:${account_id} //卡密NFT id:购买账户id
}--]]
local tbl_online_deals

--[[nft_logo:{ //存放卡密购买者列表
    [${account_id}] //购买账户id
}--]]
local tbl_online_buyers

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

--[[//存放线上支付交易 nft logo
    'pissa','chinamobile30'
--]]
local tbl_online 

--[[nft_logo:{//存放 NFT 资产数据
    ${card_type}:[${nft_asset_id}] //用以支付bounty
}--]]
local tbl_bounty 

--[[//存放 nft logo
    'pissa','chinamobile30'
--]]
local tbl_for_reservations   --是否需要预约

--[[//存放 nft logo
    'pissa','chinamobile30'
--]]
local tbl_for_times   --是否可以购买多次


--[[ 初始化配置
参数:
    payee: 收款账户
    resrv_open_time: 预约开放时间，格式为 %Y-%m-%dT%H:%M:%S
    resrv_close_time: 预约关闭时间，格式为 %Y-%m-%dT%H:%M:%S
    order_open_time: 下单开放时间，格式为 %Y-%m-%dT%H:%M:%S
    order_close_time: 下单关闭时间，格式为 %Y-%m-%dT%H:%M:%S
    redeem_open_time: 披萨兑换开放时间，格式为 %Y-%m-%dT%H:%M:%S
    redeem_close_time：披萨兑换关闭时间，格式为 %Y-%m-%dT%H:%M:%S
--]]
function init(payee, resrv_open_time, resrv_close_time, order_open_time, order_close_time, redeem_open_time, redeem_close_time)
    assert(chainhelper:is_owner(), 'Unauthorized to init')
    assert(payee and resrv_open_time and resrv_close_time and order_open_time and order_close_time and redeem_open_time and redeem_close_time, 'Invalid init parameters')
    assert(resrv_open_time < resrv_close_time, "Reserve open time must be less than close time")
    assert(order_open_time < order_close_time, "Order open time must be less than order close time")
    assert(redeem_open_time < redeem_close_time, "Redeem open time must be less than redeem close time")

    read_list = { public_data = {} }
    chainhelper:read_chain()

    -- 【判断只初始化一次】
    --assert(public_data.is_init==nil,'public_data.is_init==nil')
    --public_data.is_init = true
    public_data.is_open = true

    public_data.payee = payee
    public_data.resrv_open_time = resrv_open_time
    public_data.resrv_close_time = resrv_close_time
    public_data.order_open_time = order_open_time
    public_data.order_close_time = order_close_time
    public_data.redeem_open_time = redeem_open_time
    public_data.redeem_close_time = redeem_close_time

    --- 【初始默认数据】
    public_data.tbl_online = {}    --线上 模式
    public_data.tbl_nfts = {}
    public_data.tbl_bounty = {}     --用以支付bounty
    public_data.tbl_reservations = {}
    public_data.tbl_for_reservations = {}   --是否需要预约
    public_data.tbl_for_times = {}   --是否可以购买多次
    --public_data.tbl_pissa_orders = {}
    public_data.tbl_offline_deals = {}

    public_data.tbl_online_orders = {}
    public_data.tbl_online_deals = {}
    public_data.tbl_online_buyers = {}

    public_data.tbl_redemptions = {}
    public_data.tbl_product_prices = {}

    public_data.tbl_counters = {}
    public_data.tbl_counters[CNT_INVENTORY_QUALITY] = {}
    
    chainhelper:write_chain()
end

--[[ 批量铸造披萨 NFT 资产
参数:
    world_view: 世界观
    nft_logo: nft logo
    count: 数量
    base_describe: 基本描述
    for_bounty：是否用于bounty
    for_online: 是否线上
    for_reservations: 是否需要预定
    for_times: 是否可以购买多个，默认只能买一个
--]]
function mine_nft(world_view, nft_logo, count, base_describe, for_bounty, for_online, for_reservations, for_times)
    assert(chainhelper:is_owner(),'Unauthorized to mine NFT')

    assert(world_view, 'Invalid init parameters')
    assert(nft_logo, 'Invalid init parameters')
    assert(count > 0, 'Invalid init parameters')
    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    for i = 1, count do  
        nh_asset_id = chainhelper:create_nh_asset(contract_base_info.owner, "COCOS", world_view, base_describe, true) 
        if for_bounty then -- 在末尾插入
            if not public_data.tbl_bounty[nft_logo] then
                public_data.tbl_bounty[nft_logo] = {}
            end     
            table.insert(public_data.tbl_bounty[nft_logo], nh_asset_id)
        else
            if not public_data.tbl_nfts[nft_logo] then
                public_data.tbl_nfts[nft_logo] = {}
            end 
            table.insert(public_data.tbl_nfts[nft_logo], nh_asset_id)
        end
    end

    -- 支付方式
    if for_online then
        if not public_data.tbl_online[nft_logo] then
            public_data.tbl_online[nft_logo]=1
        end
    end

    -- 需要预定
    if for_reservations then
        if not public_data.tbl_for_reservations[nft_logo] then
            public_data.tbl_for_reservations[nft_logo]=1
            public_data.tbl_reservations[nft_logo] = {}
        end
    end

    -- 可以购买多次
    if for_times then
        if not public_data.tbl_for_times[nft_logo] then
            public_data.tbl_for_times[nft_logo]=1
        end
    end

    -- 增加计数
    if (not for_bounty) then
        local tbl_counters = public_data.tbl_counters
        func_incr_metric_counter(tbl_counters[CNT_INVENTORY_QUALITY],nft_logo,count)
    end

    -- 写入数据
    write_list = { public_data = {tbl_nfts=true,tbl_bounty=true,tbl_counters=true,tbl_for_reservations=true,tbl_online=true,tbl_reservations=true,tbl_for_times=true} }
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

--[[ 设置时间
参数:
    times_setting_json: 时间配置json，如 {"order_close_time":"2020-06-22T04:00:00", "order_open_time":"2020-06-08T02:00:00"...} 
--]]
function set_times(times_setting_json)
    assert(chainhelper:is_owner(),'Unauthorized to set times')
    assert(times_setting_json,'Invalid empty times setting json')

    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    local tbl_times = cjson.decode(times_setting_json)
    assert(tbl_times,'Bad times setting json')

    -- 写入数据
    public_data.order_close_time  = tbl_times['order_close_time']
    public_data.order_open_time   = tbl_times['order_open_time']
    public_data.redeem_close_time = tbl_times['redeem_close_time']
    public_data.redeem_open_time  = tbl_times['redeem_open_time']
    public_data.resrv_close_time  = tbl_times['resrv_close_time']
    public_data.resrv_open_time   = tbl_times['resrv_open_time']
    write_list = { public_data = {order_close_time=true,order_open_time=true,redeem_close_time=true,redeem_open_time=true,resrv_close_time=true,resrv_open_time=true} }
    chainhelper:write_chain();
end

--[[ 预约购买
参数: 
    product_type (nft_logo)
--]]
function make_reservation(product_type)
    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    -- 确认市场未关闭
    assert(public_data.is_open, "Marketplace closed")

    -- 确认预约时间
    local now = func_get_now()
    assert(now >= public_data.resrv_open_time, "Reservation not open yet")
    assert(now < public_data.resrv_close_time , "Reservation already closed")

    -- 确认是否需要预约
    assert(public_data.tbl_for_reservations[product_type], 'Not need reservation')

    local tbl_reservations = public_data.tbl_reservations
    local caller = contract_base_info.caller
    -- 防止重复预约
    assert(not tbl_reservations[product_type][caller], 'Reservation already exists')
    tbl_reservations[product_type][caller] = now

    -- 写入数据
    write_list = { public_data = {tbl_reservations = true} }
    chainhelper:write_chain();
end

--[[ 下订单购买 NFT
参数: product_type, 产品类型如 pissa (nft_logo)
--]]
function make_order(product_type)
    assert(product_type, "Wrong product type")
    -- assert(product_type ~= "pissa", "Pissa is not for sale now")

    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    -- 确认市场未关闭
    assert(public_data.is_open, "Marketplace closed")

    -- 确认购买时间
    local now = func_get_now()
    assert(now >= public_data.order_open_time , "Order not open yet")
    --assert(now < public_data.order_close_time , "Order already closed")

    local caller = contract_base_info.caller
    if public_data.tbl_for_reservations[product_type] then
        -- 确保用户已预约购买
        local tbl_reservations = public_data.tbl_reservations
        assert(tbl_reservations[product_type][caller], "No reservation before order NFT")
    end    

    -- 用户不可以多次购买
    if (not public_data.tbl_for_times[product_type]) then
        assert(public_data.tbl_nfts[product_type], "No such NFT product type")

        if public_data.tbl_online[product_type] then
            local tbl_online_buyers = public_data.tbl_online_buyers[product_type]
            if not tbl_online_buyers then
                tbl_online_buyers = {}
                public_data.tbl_online_buyers[product_type] = tbl_online_buyers
            end
            assert(not func_array_has_item(tbl_online_buyers, caller), "NFT can only be bought once")
        else
            local tbl_offline_buyers = public_data.tbl_offline_deals[product_type]
            if not tbl_offline_buyers then
                tbl_offline_buyers = {}
                public_data.tbl_offline_deals[product_type] = tbl_offline_buyers
            end
            assert(not func_array_has_item(tbl_offline_buyers, caller), "NFT can only be bought once")
        end
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

    if not public_data.tbl_online[product_type] then -- pissa NFT 发货处理   (线下方式)
        local tbl_nft_pissas0 = public_data.tbl_nfts[product_type]
        local tbl_pissa_deals = public_data.tbl_offline_deals[product_type]

        if not tbl_pissa_deals then
            tbl_pissa_deals = {}
            public_data.tbl_offline_deals[product_type] = tbl_pissa_deals
        end

        -- 分配 NFT asset
        local alloc_nft_asset_id = nil
        for _, nft_asset_id in pairs(tbl_nft_pissas0) do
            if (not tbl_pissa_deals[nft_asset_id]) then
                alloc_nft_asset_id = nft_asset_id
                break
            end
        end
        assert(alloc_nft_asset_id, "No NFT avaible for this order")
        tbl_pissa_deals[alloc_nft_asset_id] = caller

        -- 转移 pissa NFT
        chainhelper:transfer_nht_from_owner(caller,alloc_nft_asset_id, true)
    else -- 加入发货队列      (线上方式)
        local nft_cards = public_data.tbl_nfts[product_type]
        local card_deals = public_data.tbl_online_deals[product_type]
        local card_order = public_data.tbl_online_orders[product_type]

        if not card_deals then
            card_deals = {}
            public_data.tbl_online_deals[product_type] = card_deals
        end


        -- 分配 NFT asset
        local alloc_nft_asset_id = nil
        for _, nft_asset_id in pairs(nft_cards) do
            if ((card_deals and not card_deals[nft_asset_id]) or (not card_deals)) and ((card_order and not card_order[nft_asset_id]) or (not card_order)) then
                alloc_nft_asset_id = nft_asset_id
                break
            end
        end
        assert(alloc_nft_asset_id, "No NFT avaible for this order")

        -- 添加入订单队列
        if (not card_order) then
            card_order = {}
            card_order[alloc_nft_asset_id]=caller
            public_data.tbl_online_orders[product_type] = card_order
        else
            card_order[alloc_nft_asset_id]=caller
        end

        if not public_data.tbl_online_buyers[product_type] then
            public_data.tbl_online_buyers[product_type] = {}
        end
        -- 保存购买用户id
        table.insert(public_data.tbl_online_buyers[product_type], caller)
    end

    -- 减少库存
    func_incr_metric_counter(tbl_counters[CNT_INVENTORY_QUALITY],product_type,-1)

    -- 写入数据
    write_list = { public_data={tbl_offline_deals=true,tbl_online_orders=true,tbl_counters=true,tbl_online_buyers=true,tbl_online_deals=true} }
    chainhelper:write_chain();
end

--[[ 卡密订单发货   线上发货
参数:
    card_type: 卡密类型 (nft_logo)
    nft_asset_id: NFT 资产的 id
    encrypted_memo: 加密后的memo信息
    for_bounty: 是否bounty渠道
--]]
function deliver_card_nft(card_type,nft_asset_id,encrypted_memo,for_bounty)
    assert(chainhelper:is_owner(),"Unauthorized to deliver NFT")
    assert(card_type and nft_asset_id and encrypted_memo, "Invalid delivery parameters")

    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()
    
    if (not for_bounty) then
        -- 确认订单是否存在
        local card_order = public_data.tbl_online_orders[card_type]
        assert(card_order and card_order[nft_asset_id],"Order does not exist for delivery")

        -- 写入卡密信息
        chainhelper:nht_describe_change(nft_asset_id, "redeem_code_memo", encrypted_memo, true)
        -- 转移卡密 NFT
        chainhelper:transfer_nht_from_owner(card_order[nft_asset_id],nft_asset_id,true)

        -- 将 NFT 资产从订单队列转移到 deals 队列
        local card_deals = public_data.tbl_online_deals[card_type]
        if (not card_deals) then
            card_deals = {}
            public_data.tbl_online_deals[card_type] = card_deals
        end
        card_deals[nft_asset_id]=card_order[nft_asset_id]
        card_order[nft_asset_id]=nil
    else
        local card_order = public_data.tbl_bounty[card_type]
        assert(card_order and card_order[nft_asset_id],"nft does not exist for delivery")
        -- 写入卡密信息
        chainhelper:nht_describe_change(nft_asset_id, "redeem_code_memo", encrypted_memo, true)
        -- 转移卡密 NFT
        chainhelper:transfer_nht_from_owner(card_order[nft_asset_id],nft_asset_id,true)

        -- 将 NFT 资产从订单队列转移到 deals 队列
        local card_deals = public_data.tbl_online_deals[card_type]
        if (not card_deals) then
            card_deals = {}
            public_data.tbl_online_deals[card_type] = card_deals
        end
        card_deals[nft_asset_id]=card_order[nft_asset_id]        
    end

    -- 写入数据
    write_list = { public_data={tbl_online_deals=true,tbl_online_orders=true} }
    chainhelper:write_chain();
end

--[[ 兑换披萨    线下发货
参数:
    pissa_nft_id: 披萨 NFT 资产 id
    product_type: nft_logo
--]]
function redeem_pissa(pissa_nft_id,product_type)
    assert(pissa_nft_id, "Wrong NFT id")

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
    local tbl_nft_pissas0 = public_data.tbl_nfts[product_type]
    local tbl_nft_pissas1 = public_data.tbl_bounty[product_type]
    assert(func_array_has_item(tbl_nft_pissas0, pissa_nft_id) or func_array_has_item(tbl_nft_pissas1, pissa_nft_id), "Invalid NFT id");

    -- 确认尚未被兑换
    local tbl_redemptions = public_data.tbl_redemptions[product_type]
    if not tbl_redemptions then
        tbl_redemptions = {}
        public_data.tbl_redemptions[product_type] = tbl_redemptions
    end
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


--[[ 清空数据 --测试
参数:无
--]]
function clear()
    assert(chainhelper:is_owner(),"Unauthorized to close")

    -- 读出链上数据
    read_list = { public_data = {} }
    chainhelper:read_chain()

    public_data = {}
    -- 写入数据
    write_list = { public_data={} }
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

