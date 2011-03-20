// 
//  fraglet.js
//  fastFrag
//  
//  Created by gregory tomlinson on 2011-03-20.
//  Copyright 2011 the public domain. All rights reserved.
//          requires fastFrag 1.1.3.1
/*
    filename : fraglet.js
    http://unlicense.org/
    author: gregory tomlinson
    Sun Mar 20 10:10:16 EDT 2011
*/

(function(global_frame) {
    var fraglet,F,_F,__ns; // declare, don't set
    
    Fraglet=function() {
        // essentially on script load
        __ns={};
    }
    
    Fraglet.prototype = {
        all : function( key ) {
            return __ns;
        },
        c : function( key ) {
            
            return this.__create(key);
        },
        d : function( key  ) {
            // direct access
            return this.__create(key);       
        },
        t : function( key, action, payload ) {
            var ns=this.__create(key), type=(typeof payload).toLowerCase();
            if(type==="string") { payload=[payload] }
            ns[action].apply( ns, payload );
        },
        r : function( key, el ) {
            var ns=this.__create(key);
            if(!el) { 
                throw("Element Required");
            }
            ns.draw(el);
        },

        render : function(key, el, frag ) {
            var type = typeof el, ns=this.__create(key), item;
            if( type.toLowerCase === "object" ) {
                
            } else if (type.toLowerCase === "string") {
                
            } else {
                // this is an actual dom element??
            }
            if(ns) {
                item=__ns[ns]
            } else {
               // item=el.appendChild( fastFrag.create(frag) );
               ns.append(frag);
               ns.draw(el);
            }
        },
        
        //
        __create : function( key ) {
            // todo, manage for periods and other special chars in key
            if(!__ns[key]) { __ns[key]=new F( key ); }
            return __ns[key]
        },
    };
    
    F=function( ns ){
        this.__t=[];
        this.ns=ns;
        this.__active_dom=[];
        this.__root=null;        
    };
    
    F.prototype={
        // commands?? like a string of things to do??
        //
        add_root : function( clss, opts ) {
            // basically take the current list at __t
            // and make a new content node and put it in an array
            var n_frag={
                'type' : opts && opts.type || "div",
                'c' : this.__t.concat([]),
                'css' : clss
            }
            this.__t=[];
            this.__t.push(n_frag);
        },
        preprend : function( frag_item ) {
            this.__t.shift(frag_item);
            return this;
        },
        append : function( frag_item, opts ) {
            this.__t.push( frag_item  );
            return this;
        },
        insert : function(frag_item, pos ) {
            var howmany=1;
            if(pos>this.__t.length-1) {  
                this.append( frag_item ); 
                return;
            }
            if(frag_item.length) {
                howmany=frag_item.length;
            }
            this.__t.splice(pos,howmany,frag_item);
            return this;
        },
        css : function( opts, set ) {
            var type=typeof opts;
            // if(type.toLowerCase() === "string") {
            //     
            // }
        },
        extend : function() {
            // which element to extend??
        },
        extend_all : function() {
            // 
            var f,i;
            for(i=0;i<this.__t.length; i++) {
                f=this.__t[i];
            }
        },
        draw : function( el ) {
            this.__active_dom.push( el.appendChild( fastFrag.create( this.__t ) ) );
        },
        iterator : function( list, fn ) {
            var i=0;
            for(; i<list.length; i+=1) {
                fn( list[i] );
            }
        },
        /// this is neat..
        list_basic : function( type, data, opts ) {
            var frag, i=0, items=[], f_items=[], wrapper_type="ul", t=(typeof data).toLowerCase();
            if(t === "object" && t.length) {
                
            } else if (t === "object" ) {
                // this is a regular object
            } else if (t !== "string" ) {
                // number
                data=new Array(data);
            } else {
                // nope..
                throw("Non valid type for data");
            }
            
            for( ; i<data.length; i++) {
                frag = {
                    'type' : type,
                    'c' : data[i] || "",
                    'css' : opts && opts.css || null
                }
                items.push(frag)
            }
            f_items=items;
            if(type.toLowerCase() !== "li") {  wrapper_type="div"; }
            f_items={ 
                'c' : items,
                'type' : wrapper_type
            };
            this.__t.push(f_items);
            return this;
        },
        
        find : function( opts ) {
            var key = opts && opts.key || null,
                value=opts && opts.value || null;
                
            if(!key && !value) {
                return this.__t;
            }
            
            if(key) {
                // okay, loop over the object
                var t=this.__t, k;
                for(k in t) {
                    if(k===key) {
                        // match...
                    }
                }
            }
        }
    }
    // setup the fraglet
    global_frame['fraglet'] = new Fraglet();
        
})(this);