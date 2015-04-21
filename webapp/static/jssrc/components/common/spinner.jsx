const React = require("react");

const Spinner = React.createClass({
    render(){
        var className = "button not-rounded " + (this.props.className || "");
        return (
            <img src="/img/loading_mini.gif" />
        );
    }
});

module.exports = Spinner;
