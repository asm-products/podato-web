const React = require("react");

const Image = React.createClass({
    render(){
        var className = "button not-rounded " + (this.props.className || "");
        return (
            <img {...this.props} src={this.state.src} ref="image" />
        );
    },
    getInitialState(){
        return {
            src:"data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
        }
    },
    componentDidMount(){
        const width = this.refs.image.getDOMNode().offsetWidth;
        this.setState({src: "https://4hmnownffauj.firesize.com/"+width+"x/"+this.props.src});
    }
});

module.exports = Image;
