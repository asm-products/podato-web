const React = require("react");
const Link = require("react-router").Link;

const Image = require("../common/image.jsx");

const PodcastTile = React.createClass({
    render(){
        return (<div className="sm-col sm-col-2 px2">
                    <Link to="podcast" params={{splat: this.props.podcast.id}} title={this.props.podcast.title} className="block fit mx-auto">
                        <Image src={this.props.podcast.image} alt="" className="full-width "/>
                        <p className="center fit overflow-hidden" style={{textOverflow: "ellipsis", whiteSpace: "nowrap"}}>{this.props.podcast.title}</p>
                    </Link>
                </div>);
    }
});

module.exports = PodcastTile;
