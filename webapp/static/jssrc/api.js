var swagger = require("swagger-client");
var config = require("config");
var utils = require("./utils");
var merge = require("merge");
var EventEmitter = require("events").EventEmitter;

var API = new EventEmitter();
API.loaded = new Promise(function(resolve, reject){
    API.load = function(root) {
        console.log("loading API.");
        root = root || config.get("DOMAIN")[0]
        var client = new swagger({
            url: root + "/api/swagger.json",
            success: function () {
                merge(API, client.apis);
                resolve();
            }
        });
        initPodatoAuth(root, client);
    }
});


function initPodatoAuth(root, client) {
    API.PodatoAuth = function () {
        this.authData = JSON.parse(localStorage.getItem("authData")) || {};
        this.client = {
            client_id: config.get("TRUSTED_CLIENTS[0].CLIENT_ID")[0],
            scopes: Object.keys(config.get("OAUTH_SCOPES")[0]).join(" ")
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

    var instance = new API.PodatoAuth();
    client.clientAuthorizations.add("javascript", instance)
    API.login = instance.login.bind(instance);
    API.isLoggedIn = instance.isAuthenticated.bind(instance);
    console.log("auth initialized");
}
module.exports = window.API = API;
