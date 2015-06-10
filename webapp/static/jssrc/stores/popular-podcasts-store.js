const mcfly = require("../mcfly");
const constants = require("../constants");

var popular_podcasts = [];

const PopularPodcastsStore = mcfly.createStore({
    get(){return popular_podcasts}
}, function(data){
    switch(data.actionType){
        case constants.actionTypes.POPULAR_PODCASTS_FETCHED:
            popular_podcasts = data.podcasts;
            break;
        default:
            return
    }
    PopularPodcastsStore.emitChange();
});

module.exports = PopularPodcastsStore;
