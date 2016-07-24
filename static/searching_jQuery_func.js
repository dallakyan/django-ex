function popup() {

    $(".openNewWindow").click(function (e) {
        e.preventDefault();
        //took this online
        var url = $(this).attr('href');
        window.open(url, '_blank');

        $.ajax({
            type: "POST",
            url: "/eHealth/pageClick",
            data: "primarykey=" + this.id,
            success: function () { }
        });

    });
}

$(document).ready(function () {
    popup();
    //Got this from Stack Overflow - a lot of knowlege/things from there
    //http://stackoverflow.com/questions/15093112/keyup-event-not-triggered-inside-twitter-bootstrap-modal-form
   // $("body").on('keyup', "#query", suggestions());

});




//function suggestions() {

//        //alert("Hello!");
//        var constant_string2 = 'Do you mean? ';
//        var constant_string = "(click me to search)";

//        //$("#adding_suggestion").text(function () { return constant_string2 + $("#query").val() + constant_string; });

     

//        //$.ajax({
//        //    type: "POST",
//        //    url: "/eHealth/Privacy",
//        //    data: { pk: primarykey, status: isPublic },
//        //    success: function (data) {
//        //        //include below?
//        //        //$(".privateVpublic").removeAttr('checked');
//        //    }
//        //});

//}




//for Adding Pages
$(function () {
    var url = "";
    var title = "";
    var catry = "";
    var category_slug = "";
    //var visits = "";
    //is_public = "";
    //var flesch_score ="";
    //var polarity_score ="";
    //var subjectivity_score ="";



    $(".btn-primary.dropdown-toggle.mybtn.savePage").click(function () {

         url = this.id;

       
                jPrompt('Enter Title', 'Value goes here!', 'Adding a Page', function (r) {
                    if (r) {
                        title = r;
                        jPrompt('Enter Category Name. If exact name does not exist, new category added!', 'Value goes here!', 'Adding a Page', function (r) {
                            if (r) {
                                catry = r.toString();
                                alert(catry)
                                $.ajax({
                                    type: "POST",
                                    url: "/eHealth/Page",
                                    data: { link: url, titl: title, categor: catry },
                                    success: function(message){}
                                    
                                });


                            }
                        });
                    }
                });
            
        });
});


//THIS CODE WAS TAKEN FOR GITHUB CSRF TOKENS!!!!  There was a website that referred to it.
$(function () {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});









//success: function (message) {
//    $("#pages_on_the_fly").empty();
//    data = $.parseJSON(message);
//    category_slug = data.meta[0].category_slug

//    //repopulate list
//    var link_a1 = "<a href=\"#\" class=\"list-group-item \"><input type=\"checkbox\" class=\"page_deletions other\" id=\"";//+{{savedPage.pk}}+        //changed
//    var link_a2 = "\" name=\"delete\" value=\"".concat(category_slug);//+{{category_slug}}+
//    link_a2 = link_a2.concat("\"/>");
//    var jaw = ' <h4 class="openNewWindow" id="';                   //changed           //
//    var jaw2 = "\" href=\""                                        //


//    var link_a = link_a2.concat(jaw);
//    // link_a = "<li><a href=\"";
//    var link_b = "\">";
//    var link_c = "</h4>";                                          //changed
//    var stringer = "";
//    var privacyAdder = "";                                          //changed
//    // $("#saved_pages_list").append("<ul id=\"pages_on_the_fly\"></ul>");
//    var xyz = "";
//    var placeHolder1 = "";
//    var placeHolder2 = "";
//    var placeHolder0 = "";
//    var placeHolder3 = "</a>";
//    for (page = 0; page < data.meta.length; page++) {
//        stringer = link_a;
//        link_a = link_a + data.meta[page].pagepk.toString();           //
//        link_a = link_a + jaw2;                                         //
//        link_a = link_a1.concat(data.meta[page].pagepk.toString()).concat(link_a);
//        // alert(link_a);

//        //alert("status of page"+data.meta[page].pagestatus.toString());
//        if (data.meta[page].pagestatus.toString() === "true") {
//            privacyAdder = " <input type=\"checkbox\" id=\"" + data.meta[page].pagepk.toString() + "\" class=\"privateVpublic other\" name=\"private_v_public\" value=\"public\" checked /> " + privacyAdder;
//        } else {
//            privacyAdder = " <input type=\"checkbox\" id=\"" + data.meta[page].pagepk.toString() + "\" class=\"privateVpublic other\" name=\"private_v_public\" value=\"public\" /> " + privacyAdder;
//        }
//        link_c = link_c + privacyAdder;

//        xyz = link_a.concat(data.meta[page].linkurl).concat(link_b).concat(data.meta[page].name).concat(link_c).concat('</a>');
//        // alert(xyz);
//        placeHolder1 = xyz.substring(xyz.indexOf('<input type="checkbox" class'), xyz.indexOf("<h4"));
//        placeHolder2 = xyz.substring(xyz.indexOf("<h4"), xyz.indexOf("</a>"));
//        placeHolder0 = xyz.substring(0, xyz.indexOf('<input type="checkbox" class'));



//        //placeHolder1 = placeHolder2.substring(0, '<input type="checkbox"') + placeHolder1 + placeHolder2.substring('<input type="checkbox"', placeHolder2.length);
//        //alert(placeHolder1);
//        $("#pages_on_the_fly").append(placeHolder0 + placeHolder2 + placeHolder1 + placeHolder3);   //changed
//        link_c = "</h4>";                      //changed
//        privacyAdder = "";                   //changed 
//        link_a = stringer;
//        //console.log(data.meta[page].name);
//        //console.log(data.meta[page].linkurl);
//        //console.log(link_a.concat(data.meta[page].linkurl).concat(link_b).concat(data.meta[page].name).concat(link_c));
//    }
//    popup();
//    private_public_checkbox();
//    apply_bootstrapSwitches_page_slider();

//    if (data.meta[0].created === "true") {
//        var a = data.meta[0].categorypk;//pk
//        var b = category_slug;//slug
//        var c = data.meta[0].categoryname;//name

//        var htML = ' <a href="#" class="list-group-item ">' +
//'<h4 class="list-group-item-heading category_link" id="' + b + '">' + c + '</h4>' +
//'<input type="checkbox" class="category_deletions other" id="' + a + '" name="delete" value="' + a + '" /> </a>';





//        //var htML='<li><input type="checkbox" class="category_deletions" id="'+a+'" name="delete" value="'+a+'"/> <a class="category_link" id="'+b+'" href="#">'+c+'</a></li>';

//        $("#list_of_categories").append(htML);
//        $(".category_deletions").data("on-text", "Delete");
//        $(".category_deletions").data("off-text", "Keep");
//        $(".category_deletions").bootstrapSwitch();
//    }

//}//,
////  dataType: JSON
