var utils = {
    encodeQueryString(obj) {
        var pairs = [];
        for(var key in obj){
            if(obj.hasOwnProperty(key) && obj[key] !== void(0)) {
                pairs.push(key + "=" + encodeURIComponent(obj[key]));
            }
        }
        return "?" + pairs.join("&");
    },
    unique(a){
        return a.filter(function(item, pos, self) {
            return self.indexOf(item) == pos;
        })
    }
};

module.exports = utils;