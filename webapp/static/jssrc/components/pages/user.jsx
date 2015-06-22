const React = require("react");

const UsersStore = require("../../stores/users-store");
const AuthActions = require("../../actions/auth-actions");

const User = React.createClass({
    mixins: [UsersStore.mixin],
    contextTypes: {router: React.PropTypes.func},
    render(){
        return (
            <div className="bg-white rounded p2 px4">
                <div className="clearfix mxn2">
                    <div className="sm-col-12 p2">
                        <h1>{this.state.user.username}</h1>
                    </div>
                </div>
                <div className="clearfix mxn2">
                    <div className="sm-col sm-col-1 md-col-3 p2">
                        <img src={this.state.user.avatar_url} />
                    </div>
                    <div className="sm-col sm-col-11 md-col-9 clearfix p2">
                        <div className="sm-col sm-col-12">
                            <p>More stuff here.</p>
                        </div>
                    </div>
                </div>
            </div>
        );
    },
    getInitialState(){
        return {user:{
            username: "Loading ...",
            avatar_url: "/img/logo.png"
        }};
    },
    componentWillMount(){
        this.setUser();
    },
    componentWillReceiveProps(){
        this.setUser();
    },
    storeDidChange(){
        this.setUser();
    },
    setUser(){
        var userId = this.context.router.getCurrentParams().userId;
        var user = UsersStore.getUser(userId);

        if (!user){
            AuthActions.fetchUser(userId);
        }else{
            this.setState({user:user});
        }
    }
});

module.exports = User;
