    const mcfly = require("../mcfly");
const api = require("../api");
const constants = require("../constants");

const PodcastActions = mcfly.createActions({
    fetchPodcast(podcastId){
        console.log("fetchPodcast action called.");
        return new Promise((resolve, reject) => {
            api.loaded.then(() => {
                api.podcasts.getPodcast({podcastId: podcastId}, (resp) => {
                    console.log("getpodcast response for " + podcastId);
                    console.log(resp);
                    if(resp.status !== 200){
                        reject(resp.statusText);
                        return
                    }
                    resolve({
                        actionType: constants.actionTypes.PODCAST_FETCHED,
                        podcast: resp.obj
                    });
                });
            });
        });
    },
    fetchSubscriptions(userId){
        userId = userId || "me"
        return new Promise((resolve, reject) => {
            api.loaded.then(() => {
                api.users.getSubscriptions({userId: userId}, (resp) => {
                    if(resp.status !== 200){
                        reject(resp.statusText);
                        return
                    }
                    resolve({
                        actionType: constants.actionTypes.SUBSCRIPTIONS_FETCHED,
                        subscriptions: resp.obj,
                        userId: userId
                    })
                })
            });
        });
    },
    fetchingSubscriptions(userId){
        return {
            actionType: constants.actionTypes.FETCHING_SUBSCRIPTIONS,
            userId: userId
        }
    },
    fetchPopularPodcasts(){
        return new Promise((resolve, reject) => {
            api.loaded.then(() => {
                api.podcasts.query({order:"subscribers"}, (res) => {
                    resolve({
                        actionType: constants.actionTypes.POPULAR_PODCASTS_FETCHED,
                        podcasts: res.obj
                    });
                });
            });
        });
    }
});

module.exports = PodcastActions;
