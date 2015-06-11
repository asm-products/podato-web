const api = require("./api.js");
var config = require("config");

var apiRoot = void(0)
if(location.hostname === "localhost"){
    apiRoot = location.origin;
}
api.load(apiRoot, config.get("TRUSTED_CLIENTS[0].CLIENT_ID")[0], Object.keys(config.get("OAUTH_SCOPES")[0]).join(" "));


const docReady = require("doc-ready");

const React = require("react");
const Router = require("react-router");
const Route = Router.Route;
const DefaultRoute = Router.DefaultRoute;

const App = require("./components/app.jsx");
const Home = require("./components/pages/home.jsx");
const Podcast = require("./components/pages/podcast.jsx");


api.loaded.then(() =>{
    console.log("api loaded");
    console.log(api);
})

var routes = (
    <Route name="app" path="/" handler={App}>
        <DefaultRoute name="home" handler={Home} />
        <Route name="podcast" path="podcasts/*" handler={Podcast} />
    </Route>
)

docReady(() => {
    Router.run(routes, (Handler) => {
        React.render(<Handler />, document.body);
    });
});
