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
                <button disabled="true" className={className} onClick={this.subscribe} disabled={this.state.disabled}>Subscribe</button>
            )
        }
        className = "button bg-darken-2" + (this.props.className || "");
        return (
            <button className={className} onClick={this.unsubscribe} disabled={this.state.disabled}>Unsubscribe</button>
        )

    },
    makeState(){
        return {
            user: CurrentUserStore.getCurrentUser(),
            subscriptions: SubscriptionsStore.getSubscriptions("me"),
            fetching: SubscriptionsStore.isFetchingSubscriptions("me"),
            subscribed: SubscriptionsStore.isSubscribedTo("me", this.props.podcast),
        }
    },
    getInitialState(){
        return this.makeState();
    },
    subscribe(e){
        e.preventDefault();
        PodcastsActions.subscribe([this.props.podcast]);
        this.setState({disabled: true})
    },
    unsubscribe(e){
        e.preventDefault();
        PodcastsActions.unsubscribe([this.props.podcast]);
        this.setState({disabled: true})
    },
    componentWillMount(){
        PodcastsActions.fetchSubscriptions("me");
    },
    storeDidChange(){
        var newState = this.makeState();
        if(newState.subscribed !== this.state.subscribed){
            newState.disabled=false;
        }
        this.setState(newState);
    }
});

module.exports = SubscribeButton;
