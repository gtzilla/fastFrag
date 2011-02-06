
fastFrag
=====

A simple JS library for making HTML from JSON. Include fastFrag.js and you're ready to use fastFrag.


UNLICENSE
-----

[unlicense](http://unlicense.org/) 

This is free and unencumbered software released into the public domain.

see complete UNLICENSE Information below, or at [unlicense.org](http://unlicense.org/) 


Overview
-----

Who, what when where why of fastFrag.

You give fastFrag JSON and it gives you back HTML (a Document Fragment) that is ready to be added to the DOM.

Convert your existing HTML to fastFrag JSON in less than a second visit [fastFrag converter](http://json.fastfrag.org), paste in HTML and get fastFrag JSON back.

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
        attr : {
            rel : "nofollow",
            made_up : "some_attributevalue"
        },                              // attributes for the element, optional
        text : "a string"              // optional, creates a text only node. All other attributes ignored, see usage
    }

Note: Starting in version 1.0.5 the following can be used for attributes, attr and attrs for brevity

    attributes : { .. }
    attr : { .. } 
    attrs : { .. }



What is fastFrag?
----------

An extremely simple **JS helper library** for making HTML (a document fragment) from JavaScript. 

        var frag_results = fastFrag.create( { id : "my_id" }  ); // return <div id="my_id"></div>
        
For more complete examples see Usage below, or [convert html now](http://json.fastfrag.org).


Why do I want or need this?
----------

If you need to create HTML structure (somehow) with JavaScript, be that getting data from a server (AJAX) or rendering a button based on a certain state, injecting user data into the DOM, this library is for you. 

As a benefit, it handles all the escaping worries you used to have. No more Regular Expressions to 'clean up' or escape data.


When is this useful?
----------

When you need to render / change the DOM [Document Object Model] via JavaScript.

Do I need all this stuff?
------------

Nope, you only need [fastFrag.js](http://github.com/gregory80/fastFrag/blob/master/js/fastFrag.js) or [fastFrag.min.js](http://github.com/gregory80/fastFrag/blob/master/js/fastFrag.min.js) to use fastFrag. That's it. 

The remaining portion of the has been moved to fastFrag-utils and comprises samples, tests, a markdown extension, Textmate snippets, jQuery plugin sample, and finally, app engine code for converting HTML to fastFrag JSON, use it [here](http://json.fastfrag.org).  

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
            type : "a",
            content : "child one",
            attrs : {
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
    
    
Note: Starting in version 1.0.5 the following can be used for attributes, attr and attrs for brevity

    attributes : { .. }
    attr : { .. } 
    attrs : { .. }    
    
    
// create the below html with fastFrag

    <div class="mainClass">
        <a href="http://github.com/gregory80/fastFrag">fastFrag Repos</a> | <a href="#">link two</a>
    </div>    
    
// the code:
    
    fastFrag.create({
        css : "mainClass",
        content : [{
            type : "a",
            content : "fastFrag Repo",
            attrs : {
                href : "http://github.com/gregory80/fastFrag"
            }
        },{
            text : " | "
        },{
            type : "a",
            content : "link two",
            attrs : {
                href : "#"
            }
        }]
    })
    

More information on usage can be found [here](http://fastfrag.org/post/4cd354958803a42ed3000000)
    


What happened to all the other stuff?
---------
Most (if not all) non core files has been split out into their own repository. <https://github.com/gregory80/fastFrag-utils>


FAQ
-------

The Contents of the FAQ can not be found [here](http://fastfrag.org/post/4cd35c898803a434fb000000), on the new fastfrag.org *blog*
    
    

Why Does this exist?
-----------

I personally found myself needing to render HTML from JavaScript. Over the years, I have tried a variety of different techniques (fastFrag-like included) to do this. All previous iterations suffered from one of two fatal flaws. 

1.  It was potentially insecure, such as using a regular expression or string matching to replace values, for example:

        var myTemplateString = "some value here $replacevalue"
    
    or this example

        var myTemplateString = "fo bar blah {{title}} and {{body}} etc"
    
1.  It was practically impossible to read or maintain, maybe it was something like this:
    
        jQuery("#someId").html('<div class="myClass"><div><ul><li><a href="">foo</a></li><li><a href="">bar</a></li></div></div>')
    
That's hard to read, difficult to maintain is basically entirely specific to the project. Recovering that string of 'text' would provide very little value.

Since I like simple, easy to understand things. I wrote fastFrag in a few hours (weeks of testing). There are definitely other libraries out there, most have significantly more options or required some server side aspect to *prepare* the data and template. Since none of the existing options did what I needed, I wrote this. A purely client-side JavaScript template powered by JSON and returning valid Document Fragments for DOM insertion. 

Some Stats, Is it actually fast?
--------------

Testing for innerHTML method on sample_inner_html_complex.html showed:

    5ms for layout, 5ms for paint

fastFrag showed:

    4ms for layout, 1ms for paint. 

Graphs and data to come, you can run your own tests by loading the HTML files found in samples/ folder. 

I am highly skeptical that any JS template library would be faster than a simple string and inner HTML across the variety of browsers on the market: Chrome, Safari, FireFox, Internet Explorer etc. 

However, it is impossible to deny the expense incurred to escape data when using inner HTML methods directly, or risk possible serious attacks to your website if you accept any user-content. 

When comparing both the speed of inner HTML, and it's absolute need for regular expressions to attempt and catch anything *dangerous*, with fastFrag, fastFrag has so far demonstrated itself to be faster, but again graphs to come as soon as possible. 

If you have found otherwise, please tell us about it here, <http://github.com/gregory80/fastFrag/issues>. If you're skilled in creating this type of graphical data and testing, __please__ contact me info < at > fastfrag < dot > org. I would love your help!


    
Benefits
--------

I find the primary benefit of fastFrag, over concatenated strings specifically, is the end of unbalanced 'divs' or other elements. Each element is properly closed. Any 'errors' in the JSON show up clearly with a line number, 'Unexpected Identifier' for example, which means a comma is missing. This makes debugging even the most complex HTML structures very, very fast.

In addition, the speed benefits of the library have been shocking to me. After repeatedly finding 'innerHTML' to be fast in any environment, fastFrag beats that. I'm working on a stats chart and example to demonstrate this. Again, if you're skilled in creating this type of graphical data and testing, __please__ contact me info < at > fastfrag < dot > org. I would love your help!

fastFrag minimizes manipulation of the DOM API, which is generally considered to be *slow*. fastFrag allows for infinitely complex JSON structures, that can be appended to the DOM in a single line of code. This reduces the number of times the DOM is accessed. Updating the DOM require the browser to update its layout and paint events in order to display the new content.
    
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


Changelog
-------
1.1.2.2
performance release. remove excessive DOM fragment creation.

1.1.1.01
remove extra (uneeded dom frag creation)

1.1.1
Rename functions, re-organize file, group method types

1.1
JavaScript change: move to try/catch based sub node append to handle IE errors regarding appending nodes to IMG, INPUT, BR, HR or other 'self' closed tags via the DOM.


1.0.5

Note: Starting in version 1.0.5 the following can be used for attributes, attr or attrs for brevity. A mix of any possible of the below is possible. In other words, it's fully backward compatible, future versions may deprecate the identifier property 'attributes' in favor of a more compact syntax.

    attributes : { .. }
    attr : { .. } 
    attrs : { .. }
    
    
Who's Using It?
---------

If you are using fastFrag -[tell use about it](http://github.com/gregory80/fastFrag/issues)! We will list your project and a link to the project homepage here. As well as a brief description, <fastfrag.org> has also been acquired and will feature people using the template, in the future.

Currently, this project is limited to a handful of projects where I have been directly involved to some degree, for instance the bit.ly Chrome extension and fic.ly writes like as well as several projects I have yet to make public. See a list of my open projects [here on github](http://github.com/gregory80)





