const React = require("react");
const PodcastTile = require("./podcast-tile.jsx");

const PodcastGrid = React.createClass({
    render(){
        console.log("rendering podcast grid with podcasts:");
        console.log(this.props.podcasts);
        return (<div {...this.props}>
                {this.props.podcasts.map((podcast) => {
                    return <PodcastTile podcast={podcast} />
                })}
            </div>)
    }
});

module.exports = PodcastGrid;