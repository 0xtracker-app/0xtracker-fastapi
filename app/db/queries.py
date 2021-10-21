import time

def user_info_by_time(wallets, days):
    return [
{   
   '$match' : { "wallet" : {'$in' : wallets}, "timeStamp" : {"$gte" : time.time() - 86400*days}}
},
{
   '$addFields' : { 
      "date" : { '$toDate' : { '$multiply' : ["$timeStamp",1000] } },
   }
},
{
   '$group' : {
    "_id": {
      "$toDate": {
        "$subtract": [
          { "$toLong": "$date" },
          { "$mod": [ { "$toLong": "$date" }, 1000 * 60 * 60 ] }
        ]
      }
    },
     "average" : { '$avg' : "$dollarValue" }
   }
},
{
    '$sort' : {
    "_id" : 1.0
    }
}
]