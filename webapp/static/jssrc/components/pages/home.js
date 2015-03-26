const React = require("react");

const LoginButton = require("../auth/login-button")

const Home = React.createClass({
    render(){
        return (
        <div className="bg-white rounded p1">
            <h1 className="center">Podato</h1>
            <h2 className="center">Enjoy Podcasts Together</h2>
            <p className="center">
                <LoginButton authProvider="Facebook" className="m1" />
                <LoginButton authProvider="Twitter" className="m1" />
                <LoginButton authProvider="Google" className="m1" />
            </p>
        </div>
        )
    }
});

module.exports = Home