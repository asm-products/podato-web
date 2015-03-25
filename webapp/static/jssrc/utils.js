var utils = {
    encodeQueryString: function(obj){
        var pairs = [];
        for(var key in obj){
            if(obj.hasOwnProperty(key) && obj[key] !== void(0)) {
                pairs.push(key + "=" + encodeURIComponent(obj[key]));
            }
        }
        return "?" + pairs.join("&");
    }
};

module.exports = utils;