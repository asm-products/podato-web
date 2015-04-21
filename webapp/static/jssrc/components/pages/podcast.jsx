const React = require("react");

const SubscribeButton  = require("../podcasts/subscribe-button.jsx");

const CurrentUserStore = require("../../stores/current-user-store");
const PodcastsStore = require("../../stores/podcasts-store");

const PodcastsActions = require("../../actions/podcast-actions");

const Podcast = React.createClass({
    mixins: [CurrentUserStore.mixin, PodcastsStore.mixin],
    contextTypes: {router: React.PropTypes.func},
    render(){
        console.log("state:");
        console.log(this.state);
        var episodes = this.state.podcast.episodes.map((e) => {
            return (
                <div className="sm-col sm-col-12 clearfix" key={e.guid}>
                    <div className="sm-col sm-col-1"><img src={e.image || this.state.podcast.image} /></div>
                    <div className="sm-col sm-col-11 p1">
                        <div className="bold">{e.title}</div>
                        <div>{e.subtitle}</div>
                    </div>
                </div>
            );
        });
        return (
            <div className="bg-white rounded p1">
                <div className="clearfix">
                    <div className="sm-col-12 p1">
                        <h1>{this.state.podcast.title}</h1>
                    </div>
                </div>
                <div className="clearfix">
                    <div className="sm-col sm-col-1 md-col-3 p1">
                        <img src={this.state.podcast.image} />
                        <p>by {this.state.podcast.author}</p>
                        <p><SubscribeButton podcast={this.state.podcast.id} /></p>
                    </div>
                    <div className="sm-col sm-col-11 md-col-9 clearfix">
                        <div className="sm-col sm-col-12 p1">
                            <p>{this.state.podcast.description}</p>
                        </div>
                        {episodes}
                    </div>
                </div>
                <div className="clearfix">
                    <div className="sm-col sm-col-12 p1">
                        <p className="gray">{this.state.podcast.copyright}</p>
                    </div>
                </div>
            </div>
        );
    },
    getInitialState(){
        return {currentUser: CurrentUserStore.getCurrentUser(), podcast:{
            title: "Loading ...",
            image: "/img/logo.png",
            episodes: []
        }};
    },
    componentWillMount(){
        this.setPodcast();
    },
    componentWillReceiveProps(){
        this.setPodcast();
    },
    storeDidChange(){
        console.log("store did change.");
        this.setPodcast();
        this.setState({currentUser:CurrentUserStore.getCurrentUser()});
    },
    setPodcast(){
        var podcastId = this.context.router.getCurrentParams().splat;
        var podcast = PodcastsStore.getPodcast(podcastId);
        console.log("podcastId: "+podcastId);
        console.log(this.context.router.getCurrentParams())

        if (!podcast){
            console.log("fetching the podcast...");
            PodcastsActions.fetchPodcast(podcastId);
        }else{
            console.log("updated state with podcast.");
            this.setState({podcast:podcast});
        }
    }
});

module.exports = Podcast;
