const React = require("react");
const PodcastTile = require("./podcast-tile.jsx");

const PodcastGrid = React.createClass({
    render(){
        return (<div {...this.props}>
                {this.props.podcasts.map((podcast) => {
                    return <PodcastTile podcast={podcast} key={podcast.id} />
                })}
            </div>)
    }
});

module.exports = PodcastGrid;
