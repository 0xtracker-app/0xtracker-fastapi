import time
import datetime

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

def get_user_records(wallet, timestamp):

    gte = int(datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=datetime.timezone.utc).timestamp())

    return     { 
        "$and" : [
            { 
                "wallet" : wallet.lower()
            }, 
            { 
                "timeStamp" : { 
                    "$gte" : gte
                }
            }, 
            { 
                "timeStamp" : { 
                    "$lte" : gte - 1
                }
            }
        ]
    }

def addresses_per_day():
    return     [
        { 
            "$addFields" : { 
                "date" : { 
                    "$toDate" : { 
                        "$subtract" : [
                            { 
                                "$toLong" : { 
                                    "$toDate" : { 
                                        "$multiply" : [
                                            "$timeStamp", 
                                            1000.0
                                        ]
                                    }
                                }
                            }, 
                            { 
                                "$mod" : [
                                    { 
                                        "$toLong" : { 
                                            "$toDate" : { 
                                                "$multiply" : [
                                                    "$timeStamp", 
                                                    1000.0
                                                ]
                                            }
                                        }
                                    }, 
                                    86400000.0
                                ]
                            }
                        ]
                    }
                }
            }
        }, 
        { 
            "$group" : { 
                "_id" : { 
                    "date" : "$date", 
                    "wallet" : "$wallet"
                }
            }
        }, 
        { 
            "$group" : { 
                "_id" : "$_id.date", 
                "total" : { 
                    "$sum" : 1.0
                }
            }
        }, 
        { 
            "$sort" : { 
                "_id" : -1.0
            }
        }
    ] 

def farms_over_last_30_days():
    return     [
        { 
            "$addFields" : { 
                "date" : { 
                    "$toDate" : { 
                        "$subtract" : [
                            { 
                                "$toLong" : { 
                                    "$toDate" : { 
                                        "$multiply" : [
                                            "$timeStamp", 
                                            1000.0
                                        ]
                                    }
                                }
                            }, 
                            { 
                                "$mod" : [
                                    { 
                                        "$toLong" : { 
                                            "$toDate" : { 
                                                "$multiply" : [
                                                    "$timeStamp", 
                                                    1000.0
                                                ]
                                            }
                                        }
                                    }, 
                                    86400000.0
                                ]
                            }
                        ]
                    }
                }
            }
        }, 
        { 
            "$match" : { 
                "farm" : { 
                    "$ne" : "wallet"
                }, 
                "timeStamp" : { 
                    "$gte" : time.time() - 86400*30
                }
            }
        }, 
        { 
            "$group" : { 
                "_id" : { 
                    "farm" : "$farm"
                }, 
                "total" : { 
                    "$sum" : 1.0
                }
            }
        }, 
        { 
            "$sort" : { 
                "total" : -1.0
            }
        },
        { 
            "$limit" : 20.0
        }
    ] 