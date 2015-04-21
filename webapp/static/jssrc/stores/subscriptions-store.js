    const mcfly = require("../mcfly");
const constants = require("../constants");

var subscriptions = {}
var fetching = []

const SubscriptionsStore = mcfly.createStore({
    getSubscriptions(userId){return subscriptions[userId]},
    isFetchingSubscriptions(userId){return (fetching.indexOf(userId) >= 0)}
}, function(data){
    switch(data.actionType){
        case constants.actionTypes.SUBSCRIPTIONS_FETCHED:
            subscriptions[data.userId] = data.subscriptions;
            if (fetching.indexOf(data.userId) >= 0){
                fetching.splice(fetching.indexOf(data.userId), 1);
            }
            break;
        case constants.actionTypes.FETCHING_SUBSCRIPTIONS:
            fetching.push(data.userId);
        default:
            return
    }
    SubscriptionsStore.emitChange();
});

module.exports = SubscriptionsStore;
