(function(){
    
    
    /*
            Just a little template that takes javascript and uses doc frag...
                Nothing fancy or new, and maybe a little bit dangerous
            
            only works with host environments that support document.createDocumentFragment()

            
            usage
            
            // element 'type' is always assumed to be a div unless otherwise noted via 'type' attr
            fastFrag.create({
                css : "a_class_name",
                content : "string here"
            })
            content is REQUIRED, set to empty string or element is skipped (when === undefined )
            
            //returns <div class="a_class_name">string here</div>
            
            Get more complex with with nested elements:
            
            fastFrag.create({
                css : "a_class_name",
                content : [{
                    type : "a"
                    content : "child one",
                    attributes : {
                        href : "http://whatever.com"
                    }
                }, {
                    content : "child two"
                }]
            })
            
            // returns
            <div class="a_class_name">
                <a href="http://whatever.com">child one</a>
                <div>child two</div>
            </div>

    
    */
    
    var fastFrag = {
        
        create : function( params ) {
            return drawHTML(params);
        },
        
        extend : function( orig, params ) {
            // extend an existing object or frag... umm the latter seems really hard.
            console.log("orig", orig);
            console.log("update", params)
        },
        
        search : function(term) {
            console.log("yeah, we're looking... dont't hold your breath")
            // perform a search against a fast frag
            // 1. determine if object or doc frag
            // 2. fork
            //      json walk for oject
            //      dom walk for frag
            // return appropriate, object data or element
        }
    
    };
    window.fastFrag = fastFrag;

    
    var safe_el = ["script","img","a","link","li","ul","canvas","div","input","select","options",
                    "option","form","textarea", "span", "i", "body", "head", "p", "dl", "em", "dd",
                    "h1","h2","h3","h4","h5","h6","b","strong"],
        d = document, reg1, reg2, reg3, reg4, reg5;
    
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
        var attr_value;
        for(var k in attrs) {
            if(k === "value") {
                attr_value = attrs[k];
            } else {
                attr_value = _safe( attrs[k] )
            }
            //attr_value = drawHTML({ text : attrs[k] })
            el.setAttribute(k, attr_value );
        }
        
        return el;
    }
    function _make_element( o ) {
        var el_name, el;
        el_name = ( safe_el.indexOf( o.type ) > -1 ) ? o.type : "div";
        el = _mke( el_name );
        if(o.attributes) { _mke_attribute(el, o.attributes); }
        // null trick, setting to null explicitly won't add it, undefined withh made attr set to empty string
        el.id = (o.id) ? o.id : null;
        el.className = (o.css) ? o.css : null;
        
        return el;
    }
    
    function _safe( string ) {
        // make a make node, then use inner Text to pull the value?
        var txt = d.createTextNode(string)
        return (txt.nodeValue).toString();
        
        // leaving this in for now... haven't really tested yet...
        // to turn back on, call init_regexp
        // return (string && string.replace(reg1, "&amp;").replace(reg2, "&quot;").replace(reg3, "&#39;")
        //              .replace(reg4, "&gt;").replace(reg5, "&lt;") ) || "";
    }
    function _singleNode( o ) {
        var frag = d.createDocumentFragment(), el, content_type = typeof o.content, txt, txt_value;
        
        if( o.text !== undefined ) {
            el = d.createTextNode( _safe( o.text.toString() || "" ) );
        } else {
            el = _make_element( o );
            txt=null;
            if( content_type === "object") {
                txt = drawHTML( o.content );
            } else if(content_type === "string") {
                //_safe(
                    // take this out for a bit... think about all this shit
                txt = d.createTextNode( o.content );
            } else {
                txt_value = (o.content !== undefined) ? _safe( o.content.toString() || "")  : "";
                txt = d.createTextNode( txt_value );
            }
            el.appendChild( txt );
        }
        
        frag.appendChild(el);
        return frag;
    }
    
    function init_regexp() {
        reg1=new RegExp('&', 'mgi');
        reg2=new RegExp('"', 'mgi');
        reg3 = new RegExp("'", 'mgi');
        reg4=new RegExp('>', 'mgi');
        reg5= new RegExp('<', 'mgi');
    }

})();