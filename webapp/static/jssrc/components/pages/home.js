const React = require("react");

const Home = React.createClass({
    render(){
        return (
        <div className="bg-white rounded p1">
            <h1 className="center">Podato</h1>
            <h2 className="center">Enjoy Podcasts Together</h2>
            <p className="center">
                <a className="button not-rounded m1">Sign in with Facebook</a>
                <a className="button not-rounded m1">Sign in with Twitter</a>
                <a className="button not-rounded m1">Sign in with Google</a>
            </p>
        </div>
        )
    }
});

module.exports = Home