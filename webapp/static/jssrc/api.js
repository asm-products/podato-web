var swagger = require("swagger-client");
var config = require("config");
var merge = require("merge");
var EventEmitter = require("events").EventEmitter;
var utils = require("./utils");

var API = new EventEmitter();

var client = new swagger({
    url: config.get("DOMAIN")[0] + "/api/swagger.json",
    success: function(){
        API = merge(API, client.apis);
        API.emit("ready");
    }
});

API.PodatoAuth = function(){
    this.authData = {};
    this.client = {
        client_id: config.get("TRUSTED_CLIENTS[0].CLIENT_ID")[0],
        scopes: Object.keys(config.get("OAUTH_SCOPES")[0]).join(" ")
    }
}

API.PodatoAuth.prototype.login = function(authProvider){
    var authorizeEndpoint = config.get("DOMAIN")[0] + "/api/oauth/authorize";
    var authorize_url = authorizeEndpoint + utils.encodeQueryString({
        redirect_uri: config.get("DOMAIN") + "/api/oauth/js" + utils.encodeQueryString({
            origin: location.origin
        }),
        client_id:this.client.client_id,
        scope: this.client.scopes,
        provider: authProvider,
        grant_type: "implicit",
        response_type: "token"
    });
    window.open(authorize_url, "Log In to Podato", "height=200,width=200")

    if(!this._loginCallbackAttached){
        window.addEventListener("message", this.onMessage.bind(this), false);
        this._loginCallbackAttached = true;
    }
}

API.PodatoAuth.prototype.onMessage = function(event){
    if (event.origin === config.get("DOMAIN")[0]){
        console.log("authenticated: ");
        console.log(event);
        if(event.data.access_token){
            this.authData = event.data;
            this.authData.expires = new Date().getTime() + this.authData.expires_in*1000;
            API.emit("authenticated");
        }
    }
}

API.PodatoAuth.prototype.isAuthenticated = function(){
    return this.authData.access_token && this._authData.expires > new Date().getTime();
}

API.PodatoAuth.prototype.apply = function(req){
    req.headers.Authorization = "Bearer " + this.authData.access_token;
}

window.client = client;

var instance = new API.PodatoAuth();
client.clientAuthorizations.add("javascript", instance)
API.login = instance.login.bind(instance);
module.exports = API;