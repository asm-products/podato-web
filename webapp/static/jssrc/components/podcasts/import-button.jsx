const React = require("react");

const PodcastsActions = require("../../actions/podcast-actions");
const Spinner = require("../common/spinner.jsx");
const Dialog = require("../common/dialog.jsx");
const CheckboxList = require("../common/checkbox-list.jsx");
const parseXML = require("../../xml");

const ImportButton = React.createClass({
    render(){
        return (
        <span>
            <a className="button-transparent" onClick={this.toggleModal}>Import</a>
            <Dialog isOpen={this.state.dialogOpen} title="Import podcasts" onRequestClose={this.toggleModal}>
                <div className="px2">
                    <p>Export an OPML file from your podcast app. More info on how to do this will be added here soon.</p>
                    <p>
                        <label htmlFor="opmlFile">Select an OPML file.</label>
                        <input type="file" name="opmlFile" id="opmlFile" className="field" onChange={this.onFileChange}/>
                        {this.state.podcasts ? <CheckboxList ref="checklist" data={this.state.podcasts}/> : null}
                    </p>
                    <p><a className="button bg-red white" onClick={this.onDone}>Done</a></p>
                </div>
            </Dialog>
        </span>
        )
    },
    getInitialState(){
        return {
            dialogOpen: false,
            podcasts: []
        }
    },
    toggleModal(){
        console.log("open:" + this.state.dialogOpen);
        this.setState({dialogOpen: !this.state.dialogOpen});
    },
    onFileChange(e){
        var file = e.target.files[0];
        var reader = new FileReader();
        if(file.type !== "text/x-opml"){
            //TOO present some kind of error message.
            return;
        }
        reader.onload = this.onFileLoaded;
        reader.readAsText(file);
    },
    onFileLoaded(e){
        var doc = parseXML(e.target.result);
        var outlines = doc.querySelectorAll("outline");
        var podcasts = [];
        for(var i=0; i<outlines.length; i++){
            window.outline = outlines[i];
            podcasts.push({
                key: outlines[i].attributes.xmlUrl.value,
                label: outlines[i].attributes.title.value,
                default: true
            });
        }
        console.log(podcasts);
        this.setState({podcasts: podcasts});
    },
    onDone(){
        var values = this.refs.checklist.getValues()
        var urls = this.state.podcasts.filter(function(podcast){
            return values[podcast.key];
        }).map(function(podcast){
            return podcast.key
        });
        PodcastsActions.subscribe(urls);
        this.setState({podcasts: []});
        this.toggleModal();
    }
});

module.exports = ImportButton;
