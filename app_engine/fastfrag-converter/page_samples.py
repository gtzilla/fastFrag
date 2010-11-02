

page_samples = {

    'user_injection_attack' : """{
        "content": [{
            "attrs": {
                "href": "/"
            }, 
            "content": {
                "text": "fastFrag neat JSON"
            }, 
            "css": "my_class", 
            "type": "a"
        },{ 
            "content" : "<script>alert('pwned');</script>"
        }], 
        "css": "my_class", 
        "id": "my_id"
    }""",
    
    'user_script_execute' : """{
        "content": [{
            "attrs": {
                "href": "/"
            }, 
            "content": {
                "text": "fastFrag neat JSON"
            }, 
            "css": "my_class", 
            "type": "a"
        },{  
            "type" : "script", 
            "content" : "alert('not so pwned');"
        }], 
        "css": "my_class", 
        "id": "my_id"
    }""",
    
    'basic_sample' : """{
        "css" : "mainClass",
        "content" : [{
            "type" : "a",
            "content" : "fastFrag Repo",
            "attrs" : {
                "href" : "http://github.com/gregory80/fastFrag"
            }
        },{
            "text" : " | "
        },{
            "type" : "a",
            "content" : "converter home",
            "attrs" : {
                "href" : "/"
            }
        }]
    }"""

}