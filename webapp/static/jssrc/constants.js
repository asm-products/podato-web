const km = require('keymirror')

module.exports = {
    actionTypes: km({
        LOGGED_IN:null,
        LOGGED_OUT:null,
        LOGGING_IN:null,
        PODCAST_FETCHED:null,
        SUBSCRIPTIONS_FETCHED: null,
        FETCHING_SUBSCRIPTIONS: null,
        POPULAR_PODCASTS_FETCHED: null
    })
}
