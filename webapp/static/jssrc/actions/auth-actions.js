const mcfly = require("../mcfly");
const api = require("../api");
const constants = require("../constants");

const AuthActions = mcfly.createActions({
    login(authProvider){
        return new Promise((resolve, reject) => {
            api.login(authProvider);
            AuthActions.loggingIn();
        });
    },
    loggingIn(){
        return {actionType: constants.actionTypes.LOGGING_IN}
    },
    loggedIn(user){
        return {
            actionType: constants.actionTypes.LOGGED_IN,
            user: user
        };
    }
});

var authListener = () => {
    AuthActions.loggingIn();
    api.loaded.then(() => {
        api.users.getUser({userId: "me"}, function(resp){
            AuthActions.loggedIn(resp.obj)
        });
    });
};

api.addListener("authenticated", authListener);
if(api.isLoggedIn()){
    authListener();
}

module.exports = AuthActions;
