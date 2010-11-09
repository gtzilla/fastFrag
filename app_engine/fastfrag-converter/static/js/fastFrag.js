(function(){
    /*
            fastFrag
                Turn JSON into HTML, http://github.com/gregory80/fastFrag
                
            Usage: fastFrag.create( { content : "hello world" });
            // creates Document Fragment: <div>hello world</div>
            
            Learn more: http://github.com/gregory80/fastFrag/blob/master/README.md or http://fastfrag.org
            
            Convert HTML to fastFrag (fast!): http://json.fastfrag.org/
    */

    var fastFrag = {
        create : function( params ) {
            return assembleHTML(params);
        },
        version : "1.1.1.01"

    };
    window.fastFrag = fastFrag;

    var d = document;

    function assembleHTML( params ) {
        var frag = d.createDocumentFragment(), k, el;
        if(params && params.length === undefined) {
            el = _singleNode( params );
            frag.appendChild( el );
        } else {
            for(k in params) {
                el = _singleNode( params[k] );
                frag.appendChild( el );
            }
        }
        return frag;
    }

    // helpers
    function _singleNode( o ) {
        var el, txt;
        if( o.text !== undefined ) {
            el = d.createTextNode( o.text || "" );
        } else {
            el = _make_element( o );
            txt = _process_node( o );                                            
            try{
                el.appendChild( txt );                        
            } catch(e){}
        }
        
        //if(el){ frag.appendChild(el); }
        return el;
    }
    function _mke_attribute( el, attrs ) {
        for(var k in attrs) { 
            // yuck, setting disabled to false or none still breaks browsers, skip it instead
            if(k === "disabled" && !attrs[k]) { continue; }
            el.setAttribute(k, _safe( attrs[k] ) );                                         
        }
        return el;
    }
    function _make_element( o ) {
        var el_name, el;
        el_name = o.type || "div";
        el = _mke( el_name );
        // Starting in ver1.0.5, can use any mix of o.attributes || o.attr  || o.attrs
        if(o.attributes || o.attr || o.attrs) { _mke_attribute( el, o.attributes || o.attr  || o.attrs ); }
        el.id = (o.id) ? o.id : null;  el.className = (o.css) ? o.css : null;
        return el;
    }

    function _process_node( o ) {
        var txt=null, content_type = typeof o.content, txt_value;
        // JS thinks both Object and Array are typeof object, let assembleHTML guide it 
        if( content_type === "object") {
            txt = assembleHTML( o.content );
        } else if(content_type === "string") {
            txt = d.createTextNode( o.content );
        } else {
            // this might be an intger or float or boolean, it's all text to HTML..
            txt_value = (o.content !== undefined) ? (o.content.toString() || "")  : "";
            txt = d.createTextNode( txt_value );
        }
        return txt        
    }
    // short cut / conveince methods
    function _mke(elem) {
        return document.createElement( elem );
    }    
    function _safe( string ) {
        return (d.createTextNode(string).nodeValue).toString();  // put in a text node, then grab it
    }    

})();