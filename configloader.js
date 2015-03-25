var staticModule = require('static-module');
var jsonpath = require("JSONPath");
var resolve = require("resolve");
var path = require("path");
var quote = require("quote");

module.exports= function(file, opts){
    var vars = {
        __filename: file,
        __dirname: path.dirname(file),
    };

    return staticModule({
        config: {
            get: function(path){
                var obj = require("./webapp/config/settings.json");
                return JSON.stringify(jsonpath.eval(obj, path));
            }
        }
    },{vars: vars});
}

