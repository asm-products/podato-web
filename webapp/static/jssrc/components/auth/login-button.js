const React = require("react");

const AuthActions = require("../../actions/auth-actions");

const LoginButton = React.createClass({
    render(){
        var className = "button not-rounded " + (this.props.className || "");
        return (
            <a className={className} onClick={this.login} >Sign in with {this.props.authProvider}</a>
        )
    },
    login(e){
        e.preventDefault();
        AuthActions.login(this.props.authProvider.toLowerCase());
    }
});

module.exports = LoginButton;