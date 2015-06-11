const React = require("react");
const Link = require("react-router").Link;

var truncate = function(s){
    if (s.length > 500){
        return s.substring(0, 497)+"...";
    }
    return s
}

const PodcastTile = React.createClass({
    render(){
        return (<div className="sm-col sm-col-2 px2 overflow-hidden" style={{"text-overflow": "ellipsis", "white-space": "nowrap"}}>
                    <Link to="podcast" params={{splat: this.props.podcast.id}} title={this.props.podcast.title}>
                        <div className="center">
                            <img src={this.props.podcast.image} alt="" />
                        </div>
                        <p>{truncate(this.props.podcast.title)}</p>
                    </Link>
                </div>);
    }
});

module.exports = PodcastTile;
