const React = require("react");

const LoginButton = React.createClass({
    render(){
        var className = "button not-rounded " + (this.props.className || "");
        return (
            <a className={className} onclick={this.login} >Sign in with {this.props.authProvider}</a>
        )
    },
    login(e){
        e.preventDefault();

    }
});

module.exports = LoginButton;