
fastFrag
---

A simple JS library for making HTML from JavaScript, see below for samples and usage

UNLICENSE
-----


[unlicense](http://unlicense.org/) 

This is free and unencumbered software released into the public domain.

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

Overview
-----

Who, what when where why of fastFrag

What is this?
----------
A really, really simple JS helper library for making HTML from JavaScript. See Usage for examples.


Why do I want or need this?
----------

If you need to create HTML structure (somehow) with JavaScript, be that getting data from a server (AJAX) or rendering a button based on a certain state, this library is for you. As a benefit, it handles all the escaping worries you used to have. No more Regular Expressions to 'clean up' or escape data.


When is this useful?
----------

When you need to render / change the DOM from JavaScript. 

How does it work
----------

You give fastFrag JSON and it gives you back a HTML (a Docment Fragment) that is ready to be added to the DOM.

Syntax
----------
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


Usage
-----

// Let's start simple, how about a div with hello world

    fastFrag.create({ content : "hello world" })
    
// returns document fragment

    <div>hello world</div>
    
// create an empty div

    fastFrag.create({})

// return document fragment

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

I personally found myself needing to render HTML from JavaScript. Over the years, I have tried a variety of different techniques (fastFrag included) to do this. All previous iterations suffered from one of two fatal flaws. 

1.  It was potentially insecure, such as using regex or string matching to replace values, for example:

        var myTemplateString = "some value here $replacevalue"
    
    or this example

        var myTemplateString = "fo bar blah {{title}} and {{body}} etc"
    
1.  It was practically impossible to read or maintain, maybe it was something like this:
    
        jQuery("#someId").html('<div class="myClass"><div><ul><li><a href="">foo</a></li><li><a href="">bar</a></li></div></div>')
    
Just from trying to read that, you can see that while quick to write ( not that quick ) it's hard to read in the end, difficult to maintain is basically entirely specific to the project.

Since I like simple, easy to understand things. I wrote fastFrag in a few hours (weeks of testing). There are definitely other libraries out there, most have significantly more options or required some server side aspect to 'prep' the data and template. Since none of these did what I needed, I wrote this.


FAQ
-------
* Should I change my server JSON responses to work with fastFrag?

    No, it would be smarter to just changed the keys in fastFrag to work with your DATA if that is your intention. Since fastFrag is unlicensed (see top of README file or unlicense.org) you can fork this code and do just that. Otherwise, you probably already have 'middle' layer code to manipulate server data, that is where fastFrag comes in, it just makes the process of turning that data into HTML, well faster.



* How do I use this with other libraries?

    fastFrag always returns a document fragment when given a JSON object (even a poorly formed one). Any library should have tools for appending element to the DOM, here is a simple library free example.
    
        var fast_frag_response = fastFrag.create({ ... }) // pseudo code
        document.body.appendChild( fast_frag_response )
    

* Aren't there better tools already for this?

    Maybe, I haven't found one yet, please post an issue on github for this project if you find something. I am interested in learning about any simple tools that make life easier.


* Couldn't this be better?

    Yes, which is why it's open source and on github, please feel free to fork, or flag issues. The 'roadmap' is keeping this simple: very, very simple and FAST. If you make an change or improvement please send a Pull Request on github. 


* Why doesn't this do everything I ever wanted and needed?

    fastFrag has only two goals, be simple and fast. It currently has one method: .create() enough said.


* Why this syntax?

    It seemed simple and I wanted to avoid and possible conflicts or errors if the Object key is not quoted, for example 'class' is a keyword for some environments, css, is not.  I'm not married to it, any suggestions are welcome, please send me a note or file an issue: http://github.com/gregory80/fastFrag/issues

