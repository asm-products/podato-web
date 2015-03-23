var api = require("./api.js");

window.api = api;

api.addListener("ready", function(){
    console.log("api loaded");
    console.log(api);
})