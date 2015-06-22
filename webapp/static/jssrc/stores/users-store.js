const mcfly = require("../mcfly");
const constants = require("../constants");

var users = {}

const UsersStore = mcfly.createStore({
    getUser(id){return users[id]}
}, function(data){
    switch(data.actionType){
        case constants.actionTypes.USER_FETCHED:
            users[data.user.id] = data.user;
            break;
        default:
            return
    }
    UsersStore.emitChange();
});

module.exports = UsersStore;
