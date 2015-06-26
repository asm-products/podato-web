const React = require("react");

const SubscribeButton  = require("../podcasts/subscribe-button.jsx");

const CurrentUserStore = require("../../stores/current-user-store");
const PodcastsStore = require("../../stores/podcasts-store");

const PodcastsActions = require("../../actions/podcast-actions");

const Image = require("../common/image.jsx");

const Podcast = React.createClass({
    mixins: [CurrentUserStore.mixin, PodcastsStore.mixin],
    contextTypes: {router: React.PropTypes.func},
    render(){
        var episodes = this.state.podcast.episodes.map((e) => {
            return (
                <div className="clearfix mxn1 py2 border-bottom border-silver" key={e.guid}>
                    <div className="sm-col sm-col-3 md-col-1 px1">
                        <Image src={e.image || this.state.podcast.image} className="full-width" />
                    </div>
                    <div className="sm-col sm-col-9 md-col-11 px1 lh1">
                        <span className="h5 bold">{e.title}</span>
                        <span className="silver inline-block"><i className="ml1 el el-calendar"/> {new Date(e.published).toLocaleDateString()} <i className="ml1 el el-time" /> {e.duration}</span><br/>
                        <span>{e.subtitle}</span>
                    </div>
                </div>
            );
        });
        return (
            <div className="bg-white rounded p2 px4">
                <div className="clearfix mxn2">
                    <div className="sm-col-12 p2">
                        <h1>{this.state.podcast.title}</h1>
                    </div>
                </div>
                <div className="clearfix mxn2">
                    <div className="sm-col sm-col-1 md-col-3 p2">
                        <Image src={this.state.podcast.image} className="full-width" />
                        <p><SubscribeButton podcast={this.state.podcast.id} /></p>
                        <p><strong>by:</strong> {this.state.podcast.author}</p>
                        <p><strong>subscribers:</strong> {this.state.podcast.subscribers}</p>
                    </div>
                    <div className="sm-col sm-col-11 md-col-9 p2">
                        <p>{this.state.podcast.description}</p>
                        {episodes}
                    </div>
                </div>
                <div className="clearfix mxn2">
                    <div className="sm-col sm-col-12 p2">
                        <p className="gray">{this.state.podcast.copyright}</p>
                    </div>
                </div>
            </div>
        );
    },
    getInitialState(){
        return {currentUser: CurrentUserStore.getCurrentUser(), podcast:{
            title: "Loading ...",
            image: "https://podato.herokuapp.com/img/logo.png",
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
        this.setState({currentUser:CurrentUserStore.getCurrentUser()});
        this.setPodcast();
    },
    setPodcast(){
        var podcastId = this.context.router.getCurrentParams().splat;
        var podcast = PodcastsStore.getPodcast(decodeURIComponent(podcastId));

        if (!podcast){
            PodcastsActions.fetchPodcast(podcastId);
        }else{
            this.setState({podcast:podcast});
        }
    }
});

module.exports = Podcast;
