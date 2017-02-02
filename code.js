var count_ = API.users.getFollowers({});
var i = 0;var user_list = [];
var users = [];
var cycles = count_.count/1000 + 1;
while (i < cycles){user_list.push(API.users.getFollowers({"offset":i *1000,"count":1000,"fields":"country,city,online,bdate,deactivated,followers_count,counters,sex"}))@.users;
i = i+1;
}
return {"count" : count_.count, "users" : user_list@.items};