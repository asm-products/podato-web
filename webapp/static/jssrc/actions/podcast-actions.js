    const mcfly = require("../mcfly");
const api = require("../api");
const constants = require("../constants");

const PodcastActions = mcfly.createActions({
    subscribe(podcastIds){
        return new Promise((resolve, reject) => {
            api.loaded.then(() => {
                api.users.subscribe({userId: "me", podcast:podcastIds}, (resp) => {
                    API.asyncResultToPromise(resp).then((result) => {
                        resolve({
                            actionType: constants.actionTypes.SUBSCRIBED,
                            podcasts: podcastIds
                        });
                    });
                });
            });
        });
    },
    unsubscribe(podcastIds){
        return new Promise((resolve, reject) => {
            api.loaded.then(() => {
                api.users.unsubscribe({userId: "me", podcast: podcastIds}, (resp) => {
                    API.asyncResultToPromise(resp).then((res) => {
                        resolve({
                            actionType: constants.actionTypes.UNSUBSCRIBED,
                            podcasts: podcastIds
                        });
                    });
                });
            });
        });
    },
    fetchPodcast(podcastId){
        return new Promise((resolve, reject) => {
            api.loaded.then(() => {
                api.podcasts.getPodcast({podcastId: podcastId}, (resp) => {
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
        PodcastActions.fetchingSubscriptions(userId);
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
