var utils = require("./utils.js");
var config = require("config");
var merge = require("merge");
var EventEmitter = require('events').EventEmitter;

var APIError = function(message){
    this.name = "PodatoApiError";
    this.message = (message || "");
}

APIError.prototype = Error.prototype;

var PodatoAPI = {
    apiBase: config.get("DOMAIN") + "/api",

    //configurable
    client: {},
    autoRefreshAuth: true,

    _authData: {},
    _loginCallbackAttached: false,

    authenticate: function(auth_provider){
        if (this.isAuthenticated()){
            this.emit("authenticated");
            return;
        }

        if(!this.client.client_id || !this.client.scopes) throw new APIError("client.client_id and client.scopes have to be defined before calling authenticate().")

        var authorizeEndpoint = this.apiBase + "/oauth/authorize";
        var authorize_url = authorizeEndpoint + utils.encodeQueryString({
            redirect_uri: this.apiBase + "/oauth/js" + utils.encodeQueryString({
                origin: location.origin
            }),
            client_id:this.client.client_id,
            scope: this.client.scopes,
            provider: auth_provider,
            grant_type: "implicit",
            response_type: "token"
        });
        window.open(authorize_url, "Log In to Podato", "height=200,width=200")

        if(!this._loginCallbackAttached){
            window.addEventListener("message", this.onMessage.bind(this), false);
            this._loginCallbackAttached = true;
        }
    },

    onMessage: function(event){
        if (event.origin === config.get("DOMAIN")){
            if(event.data.access_token){
                this._authData = event.data;
                this._authData.expires = new Date().getTime() + this._authData.expires_in*1000;
                this.emit("authenticated");
            }
        }
    },

    isAuthenticated: function(){
        return this._authData.access_token && this._authData.expires > new Date().getTime();
    },

    request: function(options, callback){
        var xhr = new XMLHttpRequest();
        xhr.responseType = options.responseType || "json";

        if(!options.path) throw new APIError("options.path is required for request()");
        var url = this.apiBase + options.path;

        if(!options.method) throw new APIError("options.method is required for request()");
        xhr.open(options.method, url)

        var _this = this;
        var sendRequest = function(){
            if(_this._authData.access_token){
                xhr.setRequestHeader("Authorization", "Bearer "+_this._authData.access_token);
            }
            xhr.send(options.data);
            xhr.onreadystatechange = function(event){
                if(xhr.readyState === 4){
                    callback(xhr);
                }
            }
        }

        if (options.requireAuthentication && !this.isAuthenticated()){
            this.addEventListener("authenticate", sendRequest)
            this.authenticate()
        }else{
            sendRequest();
        }
    }
}


module.exports = merge(PodatoAPI, new EventEmitter());