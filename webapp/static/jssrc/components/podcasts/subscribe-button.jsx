const React = require("react");

const PodcastsActions = require("../../actions/podcast-actions");
const CurrentUserStore = require("../../stores/current-user-store");
const SubscriptionsStore = require("../../stores/subscriptions-store");
const Spinner = require("../common/spinner.jsx");

const SubscribeButton = React.createClass({
    mixins: [CurrentUserStore.mixin, SubscriptionsStore.mixin],
    render(){
        if(!this.state.user) return (<span>Log in to subscribe.</span>);
        if(!this.state.subscriptions){
            if(this.state.fetching){
                return (<Spinner></Spinner>);
            }
            return (<span>Something went wrong while trying to fetch your subscriptions..</span>);
        }

        var className = "button " + (this.props.className || "");
        if(!this.state.subscribed){
            return (
                <a className={className} onClick={this.subscribe} >Subscribe</a>
            )
        }
        className = "button bg-darken-2"
        return (
            <a className={className} onClick={this.unsubscribe}>Unsubscribe</a>
        )

    },
    makeState(){
        return {
            user: CurrentUserStore.getCurrentUser(),
            subscriptions: SubscriptionsStore.getSubscriptions("me"),
            fetching: SubscriptionsStore.isFetchingSubscriptions("me"),
            subscribed: SubscriptionsStore.isSubscribedTo("me", this.props.podcast)
        }
    },
    getInitialState(){
        return this.makeState()
    },
    subscribe(e){
        e.preventDefault();
        PodcastsActions.subscribe(this.props.podcast);
    },
    unsubscribe(e){
        e.preventDefault();
        PodcastsActions.unsubscribe(this.props.podcast);
    },
    componentWillMount(){
        PodcastsActions.fetchSubscriptions("me");
    },
    storeDidChange(){
        this.setState(this.makeState());
    }
});

module.exports = SubscribeButton;
