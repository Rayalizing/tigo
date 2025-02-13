
--万象为了降低1位辅助码权重保证分词，提升2位辅助码权重为了4码高效，但是有些时候单字超越了词组，如自然码中：jmma 睑 剑麻，于是调序 剑麻 睑
--abbrev下根据辅助码提权匹配编码的单字，并且根据编码调整了中文、英文、数字候选之间的关系
local M = {}

-- **获取辅助码**
function M.run_fuzhu(cand, env, initial_comment)
    local patterns = {
        moqi = "[^;]*;([^;]*);",
        flypy = "[^;]*;[^;]*;([^;]*);",
        zrm = "[^;]*;[^;]*;[^;]*;([^;]*);",
        jdh = "[^;]*;[^;]*;[^;]*;[^;]*;([^;]*);",
        cj = "[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;([^;]*);",
        tiger = "[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;([^;]*);",
        wubi = "[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;([^;]*);",
        hanxin = "[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;([^;]*);"
    }

    local pattern = patterns[env.settings.fuzhu_type]
    if not pattern then return {}, {} end  

    local full_fuzhu_list, first_fuzhu_list = {}, {}

    for segment in initial_comment:gmatch("[^%s]+") do
        local match = segment:match(pattern)
        if match then
            for sub_match in match:gmatch("[^,]+") do
                table.insert(full_fuzhu_list, sub_match)
                local first_char = sub_match:sub(1, 1)
                if first_char and first_char ~= "" then
                    table.insert(first_fuzhu_list, first_char)
                end
            end
        end
    end

    return full_fuzhu_list, first_fuzhu_list
end

-- **初始化**
function M.init(env)
    local config = env.engine.schema.config
    env.settings = {
        fuzhu_type = config:get_string("pro_comment_format/fuzhu_type") or ""
    }
end
-- **判断是否为字母或数字**
local function is_alnum(text)
    return text:match("^[%w]+$") ~= nil
end

-- **主逻辑**
function M.func(input, env)
    local input_code = env.engine.context.input
    local input_len = utf8.len(input_code)

    if input_len > 4 then
        for cand in input:iter() do yield(cand) end
        return
    end

    local single_char_cands, alnum_cands, other_cands = {}, {}, {}

    if input_len >= 3 and input_len <= 4 then
        -- **分类候选**
        for cand in input:iter() do
            if is_alnum(cand.text) then
                table.insert(alnum_cands, cand)
            elseif utf8.len(cand.text) == 1 then
                table.insert(single_char_cands, cand)
            else
                table.insert(other_cands, cand)
            end
        end

        local last_char = input_code:sub(-1)
        local last_two = input_code:sub(-2)
        local has_match = false
        local moved, reordered = {}, {}

        -- **如果 `other_cands` 为空，说明所有非字母数字候选都是单字，除了英文只有单字就认为是编码只有1-2个，
		--这样来替代造词的时候先提交一个字后面的码长缩短导致的基于输入码长度的逻辑失效（显示的2码，但是input码长还是4），可能出现造词第二个字抛出英文单词影响体验**
        if #other_cands == 0 then
            for _, cand in ipairs(single_char_cands) do
                table.insert(moved, cand)  -- 视为匹配成功的候选
                has_match = true
            end
        else
            -- **正常匹配 `first` 和 `full`**
            for _, cand in ipairs(single_char_cands) do
                local full, first = M.run_fuzhu(cand, env, cand.comment or "")
                local matched = false

                if input_len == 4 then
                    for _, code in ipairs(full) do
                        if code == last_two then
                            matched = true
                            has_match = true
                            break
                        end
                    end
                else
                    for _, code in ipairs(first) do
                        if code == last_char then
                            matched = true
                            has_match = true
                            break
                        end
                    end
                end

                if matched then
                    table.insert(moved, cand)
                else
                    table.insert(reordered, cand)
                end
            end
        end

        -- **动态排序逻辑**
        if has_match then
            for _, v in ipairs(other_cands) do yield(v) end
            for _, v in ipairs(moved) do yield(v) end
            for _, v in ipairs(reordered) do yield(v) end
            for _, v in ipairs(alnum_cands) do yield(v) end
        else
            for _, v in ipairs(other_cands) do yield(v) end
            for _, v in ipairs(alnum_cands) do yield(v) end
            for _, v in ipairs(moved) do yield(v) end
            for _, v in ipairs(reordered) do yield(v) end
        end

    else  -- **处理 input_len < 3 的情况**
        -- **清空分类表**
        single_char_cands, alnum_cands, other_cands = {}, {}, {}

        for cand in input:iter() do
            local len = utf8.len(cand.text)
            if is_alnum(cand.text) then
                table.insert(alnum_cands, cand)
            else
                table.insert(other_cands, cand)
            end
        end

        -- **按照既定顺序输出**
        for _, cand in ipairs(other_cands) do yield(cand) end
        for _, cand in ipairs(alnum_cands) do yield(cand) end
    end
end

return M