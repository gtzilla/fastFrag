(function(){
    /*
            fastFrag
                Turn JSON into HTML, http://github.com/gregory80/fastFrag
    */
    
    var fastFrag = {
        create : function( params ) {
            return drawHTML(params);
        },
        version : "1.0.1"
    
    };
    window.fastFrag = fastFrag;

    var d = document;
    
    function drawHTML( params ) {
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
    
    function _mke(elem) {
        return document.createElement( elem );
    }
    function _mke_attribute( el, attrs ) {
        var safe_value;
        for(var k in attrs) { 
            // yuck
            if(k === "disabled" && !attrs[k]) { continue; }
            el.setAttribute(k, _safe( attrs[k] ) ); 
        }
        return el;
    }
    function _make_element( o ) {
        var el_name, el;
        el_name = o.type || "div";
        el = _mke( el_name );
        if(o.attributes) { _mke_attribute(el, o.attributes); }
        el.id = (o.id) ? o.id : null;  el.className = (o.css) ? o.css : null;
        return el;
    }
    function _safe( string ) {
        return (d.createTextNode(string).nodeValue).toString();  // put in a text node, then grab it
    }
    function _singleNode( o ) {
        var frag = d.createDocumentFragment(), el, content_type = typeof o.content, txt, txt_value;
        if( o.text !== undefined ) {
            el = d.createTextNode( o.text || "" );
        } else {
            el = _make_element( o );
            txt=null;
            if( content_type === "object") {
                txt = drawHTML( o.content );
            } else if(content_type === "string") {
                txt = d.createTextNode( o.content );
            } else {
                txt_value = (o.content !== undefined) ? (o.content.toString() || "")  : "";
                txt = d.createTextNode( txt_value );
            }
            el.appendChild( txt );
        }
        
        frag.appendChild(el);
        return frag;
    }
})();