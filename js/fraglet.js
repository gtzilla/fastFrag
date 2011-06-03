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
    var fraglet,Fraglet,FEvent,F,_F,__ns; // declare, don't set
    
    
    /*
        A single template, stored at __ns is an F object
        
        Fraglet tracks the combination of all template
    */
    Fraglet=function() {
        // essentially on script load
        __ns={};
    }
    
    Fraglet.prototype = {
        
        lnk : function( href, txt ) {
            return {
                'type' : 'a',
                'attr' : {
                    'href' : href
                },
                'c' : txt || href
            }
        },
        inpt : function( opts ) {
            return [{
                'type' : 'label',
                'c' : opts.label_text || ""
            },{
                'type' : "input",
                'attr' : {
                    'type' : opts.type || "text",
                    'name' : opts.name || null,
                    'value' : opts.value || null
                }
            }]
        },  
        
        // do stuff to the general management of templates      
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
        // args (key, action, p,a,y,l,o,a,d) where p,a,y,l,o,a,d is N args needs for the fn_method
        t : function( key, fn_method ) {
            var payload=[], ns=this.__create(key);
            if(!key && !action) { throw("Name and method required"); }
            if(arguments.length > 2) { payload=Array.prototype.slice.call(arguments, 2); } 
            ns[fn_method].apply( ns, payload );
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
        this.__listeners=[]; // for { el : "#whatever", type : "click mousedown", method : function(e) { ... } }
        this.dom_reference=true;       
    };
    
    F.prototype={
        /*
            Holds data representation for fastFrag
        */
        // JS method overloading? sorta
        event : function( fn ) {
            fn.apply(this, Array.prototype.slice.call(arguments, 1) || []  );
        },
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
            // todo, check the listeners
            el.appendChild( fastFrag.create( this.__t ) );
            if(this.dom_reference) this.__active_dom.push( el );
        },
        iterator : function( list, fn, opts ) {
            // 'event'ish methods
            /*
                opts = {
                    before : function(){ ... }
                    complete : function(){ ... }
                }
            */
            var i=0;
            if(opts && opts.before && (typeof opts.before).toLowerCase() === "function") opts.before.call(this);
            for(; i<list.length; i+=1) {
                fn.apply( this, [list[i]] );
            }
            if(opts && opts.complete && (typeof opts.complete).toLowerCase() === "function") opts.complete.call(this);            
        },
        // a basic list
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
        
        list_links : function(type, data, opts) {
            
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
    
    FEvent=function( el, opts ){
        this.el=el;
        // todo, use extend for opts...
        if(opts&&opts.method&&(typeof opts.method).toLowerCase() === "function") { this.method=opts.method; }
        this.opts=opts;
    }
    FEvent.prototype={
        'el' : null,
        'type' : "click",
        'method' : function(){},
        'add' : function() {
            // iterate over this sucker, use something to attach the methods
            // maybe just use jquery??
            // hrm
        }
    }
    
    
    // setup the fraglet
    global_frame['fraglet'] = new Fraglet();
        
})(this);