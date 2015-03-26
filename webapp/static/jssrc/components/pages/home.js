const React = require("react");

const LoginButton = require("../auth/login-button")
const CurrentUserStore = require("../../stores/current-user-store");

const Home = React.createClass({
    mixins: [CurrentUserStore.mixin],
    render(){
        var auth = [
            (<LoginButton authProvider="Facebook" className="m1" />),
            (<LoginButton authProvider="Twitter" className="m1" />),
            (<LoginButton authProvider="Google" className="m1" />)
        ];
        if(this.state.authState === "progress") {
            auth = (<img src="/img/loading_bar.gif" />)
        }
        if(this.state.authState === "done") {
            auth = (<a>Get started</a>)
        }

        return (
            <div className="bg-white rounded p1">
                <h1 className="center">Podato</h1>
                <h2 className="center">Enjoy Podcasts Together</h2>
                <p className="center">
                    {auth}
                </p>
            </div>
        );
    },
    getInitialState(){
        return {authState: null};
    },
    storeDidChange(){
        var authState = null;
        if(CurrentUserStore.getCurrentUser() == null){
            if (CurrentUserStore.getLoggingIn()) {
                authState = "progress";
            }
        }else{
            authState = "done";
        }
        this.setState({authState});
    }
});

module.exports = Home