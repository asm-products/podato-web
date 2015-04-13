const api = require("./api.js");
const docReady = require("doc-ready");

const React = require("react");
const Router = require("react-router");
const Route = Router.Route;
const DefaultRoute = Router.DefaultRoute;

const App = require("./components/app.js");
const Home = require("./components/pages/home.js");

api.addListener("ready", function(){
    console.log("api loaded");
    console.log(api);
})

var routes = (
    <Route name="app" path="/" handler={App}>
        <DefaultRoute name="home" handler={Home}/>
    </Route>
)

docReady(() => {
    Router.run(routes, (Handler) => {
        React.render(<Handler />, document.body);
    });
});