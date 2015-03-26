const React = require("react");

const Navbar = React.createClass({
    render(){
        return (
            <nav className="fixed top-0 left-0 right-0 bg-red white px4">
                <div className="container">
                    <a href="/" className="button button-red">Home</a>
                    <a href="/" className="button button-red">Explore</a>
                    <a href="/" className="button button-red">Explore</a>
                </div>
            </nav>
        )
    }
});

module.exports = Navbar;