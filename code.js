var count_ = API.users.getFollowers({});
var i = 0;var user_list = [];
var users = [];
var cycles = count_.count/1000 + 1;
while (i < cycles){user_list = user_list + API.users.getFollowers({"offset":i *1000,"count":1000,"fields":"country,city,bdate,deactivated,followers_count,sex"}).items;
i = i+1;
}
return {"count" : count_.count, "users" : user_list};