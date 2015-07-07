const React = require("react");

const CheckboxList = React.createClass({
    render(){
        var self = this;
        var items = this.props.data.map(function(data){
            return (
                <li key={"cb"+data.key} className="p1 border-bottom border-silver">
                    <input type="checkbox" defaultChecked={data.default} ref={data.key} name={data.key} id={data.key} className="field" onChange={self.handleChange}/>
                    <label htmlFor={data.key} className="ml1">{data.label}</label>
                </li>
            )
        });
        return (
            <ul className="list-reset">
                {items}
            </ul>
        );
    },
    getValues(){
        var values = {}
        for(var i=0; i<this.props.data.length; i++){
            var d = this.props.data[i];
            values[d.key] = this.refs[d.key].getDOMNode().checked;
        }
        return values;
    }
});

module.exports = CheckboxList;;
