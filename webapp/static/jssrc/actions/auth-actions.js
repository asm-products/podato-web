const mcfly = require("../mcfly");
const api = require("../api");
const constants = require("../constants");

const AuthActions = mcfly.createActions({
    login(authProvider){
        return new Promise((resolve, reject) => {
            api.login(authProvider);
            AuthActions.loggingIn();
            const listener = () => {
                resolve({actionType: constants.actionTypes.LOGGED_IN})
                api.removeListener(listener);
            }
            api.addListener("authenticated", listener);
        });
    },
    loggingIn(){
        return {actionType: constants.actionTypes.LOGGING_IN}
    }
});

module.exports = AuthActions;