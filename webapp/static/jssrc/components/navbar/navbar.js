const React = require("react");

const Navbar = React.createClass({
    render(){
        return (
            <nav className="fixed top-0 left-0 right-0 bg-red white px4" style={{height:"2.5rem"}}>
                <div className="container flex flex-stretch" style={{height:"100%"}}>
                    <img src="/img/logo.png" style={{height:"100%"}}/>
                    <a href="/" className="button button-red">Home</a>
                    <a href="/" className="button button-red">Explore</a>
                    <a href="/" className="button button-red">Settings</a>
                </div>
            </nav>
        )
    }
});

module.exports = Navbar;