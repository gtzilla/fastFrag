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
            base_frag=d.createDocumentFragment();
            return assembleHTML(params);
        },
        version : "1.1.3.1"

    };
    window.fastFrag = fastFrag;

    var d = document, base_frag=null;

    function assembleHTML( params ) {
        var el;
        if(params && params.length === undefined) {
            el = _singleNode( params );
            base_frag.appendChild( el );
        } else {
            var sub_frag=d.createDocumentFragment(), k;
            for(k in params) {
                el = _singleNode( params[k] );
                sub_frag.appendChild( el );
            }
            return sub_frag;
        }
        return base_frag;
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
        return el;
    }
    function _mke_attribute( el, attrs ) {
        for(var k in attrs) { 
            // yuck, setting disabled to false or none still breaks browsers, skip it instead
            if(k === "disabled" && !attrs[k]) { continue; }
            // IE7 barfs if you try to set style via a style attribute on the element
            // deprecate this in favor of top level?
            if(k.toLowerCase() === "style") { el.cssText = el.style.cssText = attrs[k];}
            if(k.toLowerCase() === "value") { el.value = attrs[k]; } // IE7
            else { el.setAttribute(k, _safe( attrs[k] ) ); }                                 
        }
    }
    function _make_element( o ) {
        var el_name, el;
        el_name = o.type || "div";
        el = _mke( el_name );
        // Starting in ver1.0.5, can use any mix of o.attributes || o.attr  || o.attrs
        if(o.attributes || o.attr || o.attrs) { _mke_attribute( el, o.attributes || o.attr  || o.attrs ); }
        el.id = (o.id) ? o.id : null;  el.className = (o.css) ? o.css : null;
        if(o.style) { el.cssText = el.style.cssText=o.style; } // add style attribute..
        if(o.value) { el.value = o.value; } // add value attr.
        return el;
    }

    function _process_node( o ) {
        var txt=null, cntnt=o.c || o.content, content_type = typeof cntnt, txt_value;
        // JS thinks both Object and Array are typeof object, let assembleHTML guide it 
        if( content_type === "object") {
            txt = assembleHTML( cntnt );
        } else if(content_type === "string") {
            txt = d.createTextNode( cntnt );
        } else {
            // this might be an intger or float or boolean, it's all text to HTML..
            txt_value = (cntnt !== undefined) ? (cntnt.toString() || "")  : "";
            txt = d.createTextNode( txt_value );
        }
        return txt        
    }
    // short cut / conveince methods
    function _mke(elem) {
        return d.createElement( elem );
    }    
    function _safe( string ) {
        var txt_node=d.createTextNode(string);
        var txt=(txt_node.nodeValue).toString();  // put in a text node, then grab it
        txt_node=null
        return txt;
    }    

})();