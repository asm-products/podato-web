const mcfly = require("../mcfly");
const constants = require("../constants");

var loggingIn = false;
var currentUser = null;

const CurrentUserStore = mcfly.createStore({
    getLoggingIn(){return loggingIn},
    getCurrentUser(){return currentUser}
}, function(data){
    switch(data.actionType){
        case constants.actionTypes.LOGGING_IN:
            loggingIn = true;
            break;
        case constants.actionTypes.LOGGED_IN:
            loggingIn = false;
            currentUser = data.user;
            break;
        default:
            return
    }
    CurrentUserStore.emitChange();
});

module.exports = CurrentUserStore;