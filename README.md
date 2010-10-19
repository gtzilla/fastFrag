
fastFrag
=====

A simple JS library for making HTML from JSON. 


UNLICENSE
-----


[unlicense](http://unlicense.org/) 

This is free and unencumbered software released into the public domain.

see complete UNLICENSE Information below, or at [unlicense.org](http://unlicense.org/) 


Overview
-----

Who, what when where why of fastFrag.

You give fastFrag JSON and it gives you back HTML (a Docment Fragment) that is ready to be added to the DOM.

Convert your existing HTML to fastFrag JSON in less than a second visit [fastFrag converter](http://fastfrag-converter.appspot.com/), paste in HTML and get fastFrag JSON back.

How does it work
----------

By using existing, stable DOM methods, fastFrag quickly converts JSON to HTML a Docment Fragment), handling all escaping concerns, making it both safe and fast.

Syntax
----------

A basic example of syntax is below, more complete examples and instructions are available below under Usage:

    {
        id : "myElemId",
        content : "hello wolrd"
    }


Complex / More Complete Options

    {
        css : "myclass1 myclass2",       // optional
        id : "the_elem_id",              // optional
        type : "span",                  // optional: any html element, defaults to DIV
        content : "the inner HTML part" // optional, string, object, boolean, array accepted (create nested structures)
        attributes : {
            rel : "nofollow",
            made_up : "some_attributevalue"
        },                              // attributes for the element, optional
        text : "a string"              // optional, creates a text only node. All other attributes ignored, see usage
    }



What is fastFrag?
----------
A really, really simple JS helper library for making HTML (a document fragment) from JavaScript. See Usage for examples.


Why do I want or need this?
----------

If you need to create HTML structure (somehow) with JavaScript, be that getting data from a server (AJAX) or rendering a button based on a certain state, this library is for you. 

As a benefit, it handles all the escaping worries you used to have. No more Regular Expressions to 'clean up' or escape data.


When is this useful?
----------

When you need to render / change the DOM [Document Object Model] from JavaScript.

Usage
-----

// Let's start simple, how about a div with hello world

    fastFrag.create({ content : "hello world" })
    
// returns document fragment

    <div>hello world</div>
    
// create an empty div

    fastFrag.create({})

// return document fragment:

    <div></div>


// element 'type' is always assumed to be a div unless otherwise noted via 'type' attr

    fastFrag.create({
        type : "p",
        css : "a_class_name",
        content : "string here"
    })


//returns Document Fragment

    <p class="a_class_name">string here</p>


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

// returns Document Fragment

    <div class="a_class_name">
        <a href="http://whatever.com">child one</a>
        <div>child two</div>
    </div>
    
    
    
// create the below html with fastFrag

    <div class="mainClass">
        <a href="http://github.com/gregory80/fastFrag">Fast Frag Repos</a> | <a href="#">link two</a>
    </div>    
    
// the code:
    
    fastFrag.create({
        css : "mainClass",
        content : [{
            type : "a",
            content : "Fast Frag Repos"
            attributes : {
                href : "http://github.com/gregory80/fastFrag"
            }
        },{
            text : " | "
        },{
            type : "a",
            content : "link two"
            attributes : {
                href : "#"
            }
        }]
    })
    
    
    

Why Does this exist?
-----------

I personally found myself needing to render HTML from JavaScript. Over the years, I have tried a variety of different techniques (fastFrag-like included) to do this. All previous iterations suffered from one of two fatal flaws. 

1.  It was potentially insecure, such as using a regular expression or string matching to replace values, for example:

        var myTemplateString = "some value here $replacevalue"
    
    or this example

        var myTemplateString = "fo bar blah {{title}} and {{body}} etc"
    
1.  It was practically impossible to read or maintain, maybe it was something like this:
    
        jQuery("#someId").html('<div class="myClass"><div><ul><li><a href="">foo</a></li><li><a href="">bar</a></li></div></div>')
    
That's hard to read, difficult to maintain is basically entirely specific to the project.

Since I like simple, easy to understand things. I wrote fastFrag in a few hours (weeks of testing). There are definitely other libraries out there, most have significantly more options or required some server side aspect to 'prep' the data and template. Since none of these did what I needed, I wrote this. A purely client-side JavaScript template powered by JSON and returning valid Document Fragments for DOM insertion. 

Some Stats
--------------

Testing for innerHTML method on sample_inner_html_complex.html showed 5ms for layout, 5ms for paint

fastFrag shows 4ms for layout, 1ms for paint. For graphs and data to come, you can run your own tests by loading the HTML files found in samples/


FAQ
-------

* I already wrote my HTML, converting it seems annoying, got anything to make it less so?
    
    Absolutely, you have two options, first: visit [fastFrag converter](http://fastfrag-converter.appspot.com/), paste in HTML and get fastFrag JSON back.
    
    
    Second, in the python folder, there is a script that takes a variety of formats and returns fastFrag JSON, ready to go
    
        python converter.py -s '<div class="myClass"><a href="#link"><img src="image/image.src" border="0" /></a></div>'
        
    This will return a fastFrag ready JSON structure, any text is currently omitted, providing structure only (looking for help adding text support via a flag)
    
        {"content": [{"content": [{"attributes": {"src": "image/image.src", "border": "0"}, "type": "img"}], "attributes": {"href": "#link"}, "type": "a"}], "css": "myClass"}
        
        
    There are additional options to -s (a string), including -f (a file) or -r the URL or a remote source. Suggestions and improvements are welcome. Currently setup for python 2.6. 
    

* Should I change my server JSON responses to work with fastFrag?

    No, it would be smarter to just change the keys in fastFrag to work with your DATA if that is your intention. Since fastFrag is unlicensed (see top of README file or http://unlicense.org) you can fork this code and do just that. Otherwise, you probably already have 'middle' layer code to manipulate server data, that is where fastFrag comes in, it just makes the process of turning that DATA into HTML, well faster.



* How do I use this with other libraries?

    fastFrag always returns a document fragment when given a JSON object (even a poorly formed one). Any library should have tools for appending elements to the DOM, here is a simple library free example.
    
        var fast_frag_response = fastFrag.create({ ... }) // pseudo code
        document.body.appendChild( fast_frag_response )
        
    You could also easily use fastFrag with jQuery, for instance, you can append fastFrag results to an element widh id:someElement, using the following: 
        
        var fast_frag_response = fastFrag.create({ ... });
        $('#someElement').append( fast_frag_response )
    

* Aren't there better tools already for this?

    Maybe, I haven't found one yet, please post an issue on [github for this project](http://github.com/gregory80/fastFrag/issues) if you find something cooler or better, or even just similar. I am interested in learning about any simple tools that make life easier.


* Couldn't this be better?

    Yes, which is why it's open source and on github, please feel free to fork, or [flag issues](http://github.com/gregory80/fastFrag/issues). The 'roadmap' is keeping this simple: very, very simple and FAST. If you make an change or improvement please send a Pull Request on github. 


* Why doesn't this do everything I ever wanted and needed?

    fastFrag has only two goals, be simple and fast. It currently has one method: .create() enough said.


* Can I use it to create XML
    
    Yes, though namespace may be an issue, as it is untested. If you do use fastFrag to create namespaced XML, I would sincerely be interested in learning if it works.

* Why this syntax?

    It seemed simple and I wanted to avoid and possible conflicts or errors if the Object key is not quoted, for example 'class' is a keyword for some environments, css, is not.  I'm not married to it, any suggestions are welcome, please send me a note or file an issue: http://github.com/gregory80/fastFrag/issues
    
    Though there are still some cases where this is unavoidable, the 'for=""' attribute on labels comes to mind, 'for' must be quoted. For example
    
        var structure = {
            type : "label",
            content : "My label",
            attributes : {
                'for' : 'the_input_id'
            }
        }
 
* Aren't we mixing form and function
    
    Well, sort of, it's an improvement over using strings, now your 'data' is in JSON, which is a highly structured data transport vehicle. Since, it's native to JavaScript, it's simple to convert JSON. Converting strings on the other hand... well, how are your regular expression skills?
    
    Beyond the above, yes, in order to use fastFrag, you either have to change to its syntax, or change the syntax of fastFrag, which you are welcome to do, please [tell use about it](http://github.com/gregory80/fastFrag/issues) if so.  Since fastFrag needs JSON to operate, getting the data out of fastFrag 'syntax' is an simple as writing, the below, so it's doesn't seem like a bad thing.
    
        for(var k in obj) { ... }
    
    
Benefits
--------

I find the primary benefit of fastFrag, over concatenated strings specifically, is the end of unbalanced 'divs' or other elements. Each element is properly closed. Any 'errors' in the JSON show up clearly with a line number, 'Unexpected Identifier' for example, which means a comma is missing. This makes debugging even the most complex HTML structures very, very fast.

In addition, the speed benefits of the library have been shocking to me. After repeatedly finding 'innerHTML' to be fast in any environment, fastFrag beats that. I'm working on a stats chart and example to demonstrate this.

fastFrag minimizes manipulation of the DOM api, which is generally considered to be 'slow'. fastFrag allows for infinitely complex JSON structures, that can be appended to the DOM in a single line of code. 
    
    document.body.appendChild( fastFrag.create({ content : [...] }) );
    
or, better yet, just give it a list of elements and skip the 'wrapper'

    document.body.appendChild( fastFrag.create([....]) );
    
    

UNLICENSE
-----


[unlicense](http://unlicense.org/) 

This is free and unencumbered software released into the public domain.

see complete UNLICENSE Information below

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to http://unlicense.org/

