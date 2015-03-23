var swagger = require("swagger-client");
var config = require("config");
var merge = require("merge");
var EventEmitter = require("events").EventEmitter;

var API = new EventEmitter();

var client = new swagger({
    url: config.get("DOMAIN") + "/api/swagger.json",
    success: function(){
        API = merge(API, client.apis);
        API.emit("ready");
    }
});


module.exports = API;