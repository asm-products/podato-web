const React = require("react");

const Spinner = React.createClass({
    render(){
        return (
            <img src="/img/loading_mini.gif" />
        );
    }
});

module.exports = Spinner;
