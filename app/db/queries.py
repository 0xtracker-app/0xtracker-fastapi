import time

def user_info_by_time(wallets, days, farms):
    return [
{   
   '$match' : { "wallet" : {'$in' : wallets}, "farm" : { "$in" if farms else "$nin" : farms}, "timeStamp" : {"$gte" : time.time() - 86400*days}}
},
{
   '$addFields' : { 
      "date" : { "$toDate" : { "$subtract" : [{ "$toLong": { "$toDate" : { "$multiply" : ["$timeStamp",1000] } } },{ "$mod": [ { "$toLong": { "$toDate" : { "$multiply" : ["$timeStamp",1000] } } }, 1000 * 60 * 60 ] } ] }},
   }
},
{
   "$group" : {
    "_id": { "farm" : '$farm',
             "date" : '$date',
             "network" : '$farm_network',
         },

     "average" : { "$avg" : "$dollarValue" }
   }
},
{
   "$group" : {
    "_id": '$_id.date',

     "average" : { "$sum" : "$average" }
   }
},
{
    '$sort' : {
    "_id" : 1.0
    }
}
]

def get_terra_pool(token0, token1):
   return     { 
        "$and" : [
            { 
                "all_tokens" : { 
                    "$in" : [
                        token0
                    ]
                }
            }, 
            { 
                "all_tokens" : { 
                    "$in" : [
                        token1
                    ]
                }
            }
        ]
    }