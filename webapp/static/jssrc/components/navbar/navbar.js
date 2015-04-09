const React = require("react");
const Link = require("react-router").Link;

const Navbar = React.createClass({
    render(){
        return (
            <nav className="fixed top-0 left-0 right-0 bg-red white px4" style={{height:"2.5rem"}}>
                <div className="container flex flex-stretch" style={{height:"100%"}}>
                    <img src="/img/logo.png" style={{height:"100%"}}/>
                    <Link to="home" className="button button-red">Home</Link>
                    <div style={{padding:"0.5rem"}}><input type="search" name="search" style={{height:"1.5rem"}} /></div>
                </div>
            </nav>
        )
    }
});

module.exports = Navbar;