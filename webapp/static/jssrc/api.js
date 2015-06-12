var swagger = require("swagger-client");
var config = require("config");
var utils = require("./utils");
var merge = require("merge");
var EventEmitter = require("events").EventEmitter;

var API = new EventEmitter();
API.loaded = new Promise(function(resolve, reject){
    API.load = function(root, client_id, scopes) {
        console.log("loading API.");
        root = root || config.get("DOMAIN")[0]
        var client = new swagger({
            url: root + "/api/swagger.json",
            success: function () {
                merge(API, client.apis);
                resolve();
            }
        });
        initPodatoAuth(root, client, client_id, scopes);
    }
});


function initPodatoAuth(root, client, client_id, scopes) {
    API.PodatoAuth = function () {
        this.authData = JSON.parse(localStorage.getItem("authData")) || {};
        this.client = {
            client_id: client_id,
            scopes: scopes
        }
        if (this.isAuthenticated()) {
            console.log("Detected existing session");
            API.emit("authenticated");
        }
    }

    API.PodatoAuth.prototype.login = function (authProvider) {
        var authorizeEndpoint = root + "/api/oauth/authorize";
        var authorize_url = authorizeEndpoint + utils.encodeQueryString({
            redirect_uri: root + "/api/oauth/js" + utils.encodeQueryString({
                origin: location.origin
            }),
            client_id: this.client.client_id,
            scope: this.client.scopes,
            provider: authProvider,
            grant_type: "implicit",
            response_type: "token"
        });
        window.open(authorize_url, "Log In to Podato", "height=200,width=200")

        if (!this._loginCallbackAttached) {
            window.addEventListener("message", this.onMessage.bind(this), false);
            this._loginCallbackAttached = true;
        }
    }

    API.PodatoAuth.prototype.onMessage = function (event) {
        if (event.origin === root) {
            if (event.data.access_token) {
                this.authData = event.data;
                this.authData.expires = new Date().getTime() + this.authData.expires_in * 1000;
                localStorage.setItem("authData", JSON.stringify(this.authData))
                API.emit("authenticated");
            }
        } else{
            console.log("Message from unknown origin: " + event.origin);
        }
    }

    API.PodatoAuth.prototype.isAuthenticated = function () {
        return this.authData.access_token && this.authData.expires > new Date().getTime();
    }

    API.PodatoAuth.prototype.apply = function (req) {
        req.headers.Authorization = "Bearer " + this.authData.access_token;
    }

    API.asyncResultToPromise = (asyncResult) => {
        console.log("starting to check for async result: "+asyncResult.id);

        var pollInterval = 500;
        return new Promise((resolve, reject) => {
            var handleResponse = (resp) => {
                if(resp.obj.state == "SUCCESS"){
                    resolve(resp.obj);
                    return true;
                }else if(resp.obj.state == "FAILURE"){
                    reject(resp.obj);
                    return true;
                }
                return false;
            }

            if(handleResponse(asyncResult)){
                return;
            }

            var intervalId = setInterval(() => {
                API.async.getAsync({asyncId: asyncResult.id}, (resp) => {
                    console.log("Polling...");
                    if (handleResponse(resp)){
                        clearInterval(intervalId);
                    }
                });
            }, pollInterval);
        });
    };

    var instance = new API.PodatoAuth();
    client.clientAuthorizations.add("javascript", instance)
    API.login = instance.login.bind(instance);
    API.isLoggedIn = instance.isAuthenticated.bind(instance);
    console.log("auth initialized");
}
module.exports = window.API = API;
