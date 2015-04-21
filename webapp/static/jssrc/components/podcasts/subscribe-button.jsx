const React = require("react");

const PodcastsActions = require("../../actions/podcast-actions");
const CurrentUserStore = require("../../stores/current-user-store");
const SubscriptionsStore = require("../../stores/subscriptions-store");
const Spinner = require("../common/spinner.jsx");

const LoginButton = React.createClass({
    render(){
        if(!CurrentUserStore.getCurrentUser()) return;
        if(!SubscriptiosStore.getSubscriptions("me")){
            if(SubscriptionsStore.isFetchingSubscriptions("me")){
                return "<Spinner></Spinner>"
            }
            return;
        }

        var className = "button " + (this.props.className || "");
        return (
            <a className={className} onClick={this.handleClick} >Subscribe</a>
        )
    },
    handleClick(e){
        e.preventDefault();
        //TODO implement subscribe action
    }
});

module.exports = LoginButton;
