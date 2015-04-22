    const mcfly = require("../mcfly");
const api = require("../api");
const constants = require("../constants");

const PodcastsActions = mcfly.createActions({
    subscribe(podcastIds){
        return new Promise((resolve, reject) => {
            api.loaded.then(() => {
                api.users.subscribe({userId: "me", podcast:podcastIds}, (resp) => {
                    if(resp.status !== 200){
                        reject(resp.statusText);
                        return
                    }
                    resolve({
                        actionType: constants.actionTypes.SUBSCRIBED,
                        podcasts: podcastIds
                    })
                });
            });
        });
    },
    unsubscribe(podcastIds){
        return new Promise((resolve, reject) => {
            api.loaded.then(() => {
                api.users.unsubscribe({userId: "me", podcast: podcastIds}, (resp) => {
                    if(resp.status !== 200){
                        reject(resp.statusText);
                        return
                    }
                    resolve({
                        actionType: constants.actionTypes.UNSIBSCRIBED,
                        podcasts: podcastIds
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
        PodcastsActions.fetchingSubscriptions(userId);
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
    }
});

module.exports = PodcastsActions;;
