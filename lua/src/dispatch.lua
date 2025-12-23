local M = {}

local dynamic_dispatcher = {}

function dynamic_dispatcher.__call(tbl, arg1,  ...)
    local objType = type(arg1)
    if objType == "table" then
        local meta = getmetatable(arg1)
        while meta ~= nil do
            local method = tbl[meta]
            if method ~= nil then
                return method(arg1, ...)
            end
            meta = getmetatable(meta)
        end
    end
    
    local method = tbl[objType]
    if method ~= nil then
        return method(arg1, ...)
    end
    
    local fallback = tbl["any"]
    if fallback ~= nil then
        return fallback(arg1, ...)
    else
        error("Failed to find method")
    end
end

function M.new(init)
    init = init or {}
    setmetatable(init, dynamic_dispatcher)
    return init
end

function M.struct(supertype)
    local retval = {}
    retval.new = function (tbl)
        tbl = tbl or {}
        setmetatable(tbl, retval)
        return tbl
    end
    if supertype ~= nil then setmetatable(retval, supertype) end
    return retval
end


-----------------------------------------------------------------------------

local Array = M.struct()
local Dict = M.struct()

local iterate = M.new {
    [Array] = function (a)
        return ipairs(a)
    end,
    [Dict] = function (d)
        return pairs(d)
    end,
    ["any"] = function (...) return "hello fallback :-)" end,
}


local array = Array.new {2,5,7,9, foo = 12, asdf = 33}

print("iterate as array")
for _, i in iterate(array) do
    print(i)
end

print("")
print("iterate as dict")

local dict = Dict.new {2,5,7,9, foo = 12, asdf = 33}

for k, v in iterate(dict) do
    print(k, "-", v)
end

local sum = M.new {
    [Array] = function (a)
        local retval = 0
        for _, x in ipairs(a) do
            retval = retval + x
        end
        return retval
    end,
    number = function (x) return x end,
}

local UnitRange = M.struct(Array)

local function sumGauss(n) return n * (n + 1) / 2 end


sum[UnitRange] = function (unitRange)
    print("gaussRange")
    return sumGauss(unitRange.stop) - sumGauss(unitRange.start)
end

print("")
print("")
print("testing Sum")
print("")
print("")
print(sum(3))
print("")
print(sum(array))
print("")
print("unitrange:")

local unitrange = UnitRange.new {start = 1, stop = 5}
print(sum(unitrange))
print(iterate({5,6,7}))

local a = {}
local b = {}
b[a] = function (...) return "hi!" end

b.[a]()


