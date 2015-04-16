const mcfly = require("../mcfly");
const constants = require("../constants");

var podcasts = {}

const PodcastsStore = mcfly.createStore({
    getPodcast(id){return podcasts[id]}
}, function(data){
    switch(data.actionType){
        case constants.actionTypes.PODCAST_FETCHED:
            podcasts[data.podcast.id] = data.podcast;
            break;
        default:
            return
    }
    PodcastsStore.emitChange();
});

module.exports = PodcastsStore;
