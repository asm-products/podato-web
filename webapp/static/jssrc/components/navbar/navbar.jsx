const React = require("react");
const Link = require("react-router").Link;

const CurrentUserStore = require("../../stores/current-user-store");
const AuthActions = require("../../actions/auth-actions");

const Navbar = React.createClass({
    mixins: [CurrentUserStore.mixin],
    render(){
        var logout = ""
        if(this.state.user){
            logout = <a onClick={AuthActions.logout} className="button button-red">Log out</a>
        }
        return (
            <nav className="fixed top-0 left-0 right-0 bg-red white px4" style={{height:"2.5rem"}}>
                <div className="container flex flex-stretch" style={{height:"100%"}}>
                    <Link to="home" style={{height:"100%"}}><img src="/img/logo.png" style={{height:"100%"}}/></Link>
                    <Link to="home" className="button button-red">Home</Link>
                    <div style={{padding:"0.5rem"}}><input type="search" name="search" style={{height:"1.5rem"}} /></div>
                    {logout}
                </div>
            </nav>
        )
    },
    getInitialState(){
        return {user: CurrentUserStore.getCurrentUser()}
    },
    storeDidChange(){
        this.setState({user: CurrentUserStore.getCurrentUser()})
    }
});

module.exports = Navbar;
