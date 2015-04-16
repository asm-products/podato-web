const mcfly = require("../mcfly");
const api = require("../api");
const constants = require("../constants");

const AuthActions = mcfly.createActions({
    fetchPodcast(podcastId){
        console.log("fetchPodcast action called.");
        return new Promise((resolve, reject) => {
            api.loaded.then(function(){
                api.podcasts.getPodcast({podcastId: podcastId}, function(resp){
                    console.log("getpodcast response for " + podcastId);
                    console.log(resp);
                    if(resp.status !== 200){
                        reject(resp.statusText);
                    }
                    resolve({
                        actionType: constants.actionTypes.PODCAST_FETCHED,
                        podcast: resp.obj
                    });
                });
            });
        });
    }
});

module.exports = AuthActions;
