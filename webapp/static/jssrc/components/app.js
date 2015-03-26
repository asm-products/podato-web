const React = require("react");
const RouteHandler = require("react-router").RouteHandler;
const Navbar = require("./navbar/navbar.js");


const App = React.createClass({
    render() {
        return (
            <div className="clearfix">
                <Navbar />
                <div className="container mt4">
                    <RouteHandler />
                </div>
            </div>
        );
    }
});

module.exports = App