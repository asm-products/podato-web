const mcfly = require("../mcfly");
const constants = require("../constants");

var loggingIn = false;

const CurrentUserStore = mcfly.createStore({
    getLoggingIn(){return loggingIn},
    getCurrentUser(){return JSON.parse(localStorage.currentUser)}
}, function(data){
    switch(data.actionType){
        case constants.actionTypes.LOGGING_IN:
            loggingIn = true;
            break;
        case constants.actionTypes.LOGGED_IN:
            loggingIn = false;
            localStorage.currentUser = JSON.stringify(data.user);
            break;
        case constants.actionTypes.LOGGED_OUT:
            loggingIn = false;
            localStorage.currentUser = null;
            break;
        case constants.actionTypes.LOGIN_CANCELLED:
            loggingIn = false;
            break;
        default:
            return
    }
    CurrentUserStore.emitChange();
});

module.exports = CurrentUserStore;
