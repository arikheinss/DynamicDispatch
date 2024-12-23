
const poly = {
    "new" : function (initvalues = null) {
        let methodTable = new Map()
        if (initvalues != null) {
            console.log("")
        }
        let fn = function (obj, ...args){
            let objType = typeof(obj)
            if (objType == "object"){
                let meta = Object.getPrototypeOf(obj)
                while (meta != null){
                    method = methodTable.get(meta)
                    if (!(method === undefined)){
                        return method(obj, ...args)
                    }
                }
                objType = "any"
            } else {
                method = methodTable.get(objType)
                if (!(method === undefined)){
                    return method(obj, ...args)
                } else {
                    throw Error("No methods found")
                }
            }

        }
        fn.methodTable = methodTable
        fn.setmethod = function (type, method){
            this.methodTable.set(type, method)
        }
        return fn
    },
    "register" : function (fn, type, method){
        fn.methodTable.set(type, method)
    },
}


const _Array = Object.create(null)

let array = Object.create(_Array)
array.data = [3,5,7]

const UnitRange = Object.create(_Array)
let range = Object.create(UnitRange)
range.length = 5

let iterate = poly.new()
iterate.setmethod( _Array, function (a){return a.data})
iterate.setmethod(UnitRange, function (u){return Array(u.length).keys()})

for (let x of iterate(array)){console.log(x)}

let sum = poly.new()
sum.setmethod( _Array, function (a){
    let res = 0
    for (let x of iterate(a)){ res = res + x}
    return res
    }
)
sum.setmethod("number", function (x){ return x})


console.log("sum array: ", sum(array))
console.log("sum number: ", sum(12))






