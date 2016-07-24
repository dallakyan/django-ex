//This was pretty much taken from http://www.w3schools.com/jquery/jquery_selectors.asp


//$(document).ready(
//    function () {
//        $("#okay").click(function () {
//            //$("#okay").hide();
//            alert("Yo you ");

//        });
//    });

//
//Taken from Stack Overflow : also I have taken other things
function toTitleCase(str) {
    return str.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });
}

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


function private_or_public_checkbox(obj) {

        //alert("Hello!");

        //  if(this.class==".privateVpublic.other")
    var primarykey = obj.id.toString();
   // alert(primarykey);
        var isPublic = 1;
        //$('#a.b.c')
        var query = '#' + primarykey + ".privateVpublic";

        //not checked means that the the page is in fact private
        if ($(query).is(':checked')) {
            //alert('it is now checked');
            isPublic = 1;
        } else {
            isPublic = 0;
        }

        $.ajax({
            type: "POST",
            url: "/eHealth/Privacy",
            data: { pk: primarykey, status: isPublic },
            success: function (data) {
                //include below?
                //$(".privateVpublic").removeAttr('checked');
            }
        });


}

function private_public_checkbox() {


    $(".privateVpublic.other").click(function () {
        //alert("Hello!");

        //  if(this.class==".privateVpublic.other")
        var primarykey = this.id.toString();
        var isPublic = 1;
        //$('#a.b.c')
        var query = '#' + primarykey + ".privateVpublic";
        
        //not checked means that the the page is in fact private
        if($(query).is(':checked')){
            //alert('it is now checked');
            isPublic = 1;
        } else {
            isPublic = 0;
        }
        
        $.ajax({
            type: "POST",
            url: "/eHealth/Privacy",
            data: {pk:primarykey, status:isPublic},
            success: function(data){
                //include below?
                //$(".privateVpublic").removeAttr('checked');
            }
        });



    });
}

function apply_bootstrapSwitches_page_slider() {
    $(".page_deletions.other").data("on-text", "Delete");
    $(".page_deletions.other").data("off-text", "Keep");
    $(".page_deletions.other").bootstrapSwitch();
     private_public_checkbox() 
    $(".privateVpublic.other").data("on-text", "Public");
    $(".privateVpublic.other").data("off-text", "Private");
    $(".privateVpublic.other").bootstrapSwitch();
}


function apply_checks_privacy_of_pages() {
    $.ajax({
        type: "POST",
        url: "/eHealth/gpages",
        data: {},
        success: function (message) {
            data = $.parseJSON(message);
            key = "";

            for (page = 0; page < data.meta.length; page++) {
                key = "#"+data.meta[page].pagepk.toString();
                key = key + ".privateVpublic";
                //alert(key);
                if (data.meta[page].pagestatus === "true") {
                    $(key).attr('checked', true); 
                } else {
                    $(key).attr('checked', false);
                }
           }

        }
    });
}

$(document).ready(function(){
    //set up
    $(function () {
        private_public_checkbox();

        // $('.category_link').click(function () { alert("Hello");});
        $(".category_deletions.other").removeAttr('checked');
        $(".category_deletions").data("on-text", "Delete");
        $(".category_deletions").data("off-text", "Keep");
        $(".category_deletions").bootstrapSwitch();
        
        //$(".category_deletions").attr("auto-complete", "off");
       // $(".page_deletions").attr("auto-complete", "off");
      
        $(".page_deletions").removeAttr('checked');
        $("#profile_form").hide();
        popup();
        apply_checks_privacy_of_pages();

        $(".privateVpublic.other").removeAttr('checked');
    });//
    
    //on form submissions for the User Profile
    $(function () {
        $('#button_submit_user_info').click(function () {
            // validateForm();
            var info = ""; 
            var random = "";
            random = $('#ageinp').val().toString();
            info = info.concat(random);
            info = info.concat(",");

            random = $('#firstnameinp').val().toString();
            info = info.concat(random);
            info = info.concat(",");

            random = $('#lastnameinp').val();
            info = info.concat(random);
            info = info.concat(",");

            random = $('#usernameinp').val();
            //alert("random is : " + random);
            info = info.concat(random);
            info = info.concat(",");

            random = $('#emailinp').val()
            info = info.concat(random);
            info = info.concat(",");

            random = $('#genderinp').val();
            info = info.concat(random);
            
            //alert(info);
            $.ajax({
                type: "POST",
                url: "/eHealth/changeUserInfo",
                data: "information="+info,
                success: function () {
                    //$('#ageinp').val(data.meta[0].ageinp);
                    //$('#firstnameinp').val(data.meta[0].firstnameinp);
                    //$('#lastnameinp').val(data.meta[0].lastnameinp);
                    //$('#usernameinp').val(data.meta[0].usernameinp);
                    //$('#emailinp').val(data.meta[0].emailinp);
                    //$('#genderinp').val(data.meta[0].genderinp);

                    
                    //$('#userINFO').hide();
                   
                    //$('#name_li').text('Name: ' + data.meta[0].firstnameinp + ' ' + data.meta[0].lastnameinp);
                    //$('#username_li').text('Username: ' + data.meta[0].usernameinp);
                    //$('#age_li').text('Age: ' + data.meta[0].ageinp);
                    //$('#email_li').text('Email: ' + data.meta[0].emailinp);
                    //$('#gender_li').text('Gender: ' + data.meta[0].genderinp);
                    $('#profile_form').toggle();
                    location.reload()
                    //try{

                    //} catch (error) {

                    //}
                }
            });

        });
    });

    //for form visibility
    $(function () {
        $('#button_toggle').click(function () {
            var random = "";
            if($('#profile_form').is(':visible')){
                $('#profile_form').toggle();
            }
            else {
                $.ajax({
                    type: "POST",
                    url: "/eHealth/getUserInfo",
                    data: "random="+random,
                    success: function (message) {
                        data = $.parseJSON(message);
                        
                        $('#ageinp').val(data.meta[0].ageinp);
                        $('#firstnameinp').val(data.meta[0].firstnameinp);
                        $('#lastnameinp').val(data.meta[0].lastnameinp);
                        $('#usernameinp').val(data.meta[0].usernameinp);
                        $('#emailinp').val(data.meta[0].emailinp);
                        $('#genderinp').val(data.meta[0].genderinp);
                        $('#profile_form').toggle();
                    }//end of success
                });
             }//end of else
        });
    });
    
    //for deleting pages
    $(function () {
        $('#delete_pages_button.btn-primary').click(function () {
            var information = "";
            var categoryInfo = "";
            var counter = 0;
            var category_slug = "";
            //alert("here");
            $('.page_deletions.other').each(function () {
                
                categoryInfo = this.value;//document.getElementById(this.id).getElementsByClassName("page_deletions")[0].value;
              //  alert(categoryInfo);
                if (this.checked) {
                    
                    information = information.concat(this.id.toString()).concat(",");
                    //disable visibility 
                }
            });
            category_slug = categoryInfo;
            information = information.substring(0, information.length - 1);
            categoryInfo = categoryInfo.concat(",").concat(information);
            //alert(information + "is the information");
           // alert(categoryInfo);

            $.ajax({
                type: "POST",
                url: "/eHealth/deletePage",
                data: "information=" + categoryInfo,
                success: function (message) {
                    $("#pages_on_the_fly").empty();
                    //add in new html code with the JSON Object 
                    data = $.parseJSON(message);

                   //' <a href="#" class=\"list-group-item \">
                   //                <h4 class="list-group-item-heading category_link" id="{{category.slug}}">{{category.name}}</h4>
                   //                <input type="checkbox" class="category_deletions other" id="{{category.pk}}" name="delete" value="{{category.pk}}" />
                    //               <input type="checkbox" class="page_deletions other" id="{{category.pk}}" name="delete" value="{{category.pk}}" />
                   //            </a>'


                    // <h4 class="openNewWindow" id="{{savedPage.pk}}" href="{{savedPage.linkURL}}"> {{savedPage.title}} </h4>

                  //  alert('okay');

                    var link_a1 = "<a href=\"#\" class=\"list-group-item \"><input type=\"checkbox\" class=\"page_deletions other\" id=\"";//+{{savedPage.pk}}+        //changed
                    var link_a2 = "\" name=\"delete\" value=\"".concat(category_slug);//+{{category_slug}}+
                    link_a2 = link_a2.concat("\"/>");
                    var jaw = ' <h4 class="openNewWindow" id="';                   //changed 
                    var jaw2 = "\" href=\""                                        //


                    var link_a = link_a2.concat(jaw);                                //
                    // link_a = "<li><a href=\"";
                    var link_b = "\">";
                    var link_c = "</h4>";                                          //changed
                    var stringer = "";
                    var privacyAdder = "";                                          //changed
                    // $("#saved_pages_list").append("<ul id=\"pages_on_the_fly\"></ul>");
                    var xyz = "";
                    var placeHolder1 = "";
                    var placeHolder2 = "";
                    var placeHolder0 = "";
                    var placeHolder3 = "</a>";
                    for (page = 0; page < data.meta.length; page++) {
                        stringer = link_a;
                        link_a = link_a + data.meta[page].pagepk.toString();           //
                        link_a = link_a + jaw2;                                         //
                        link_a = link_a1.concat(data.meta[page].pagepk.toString()).concat(link_a);
                        // alert(link_a);


                        //alert("status of page"+data.meta[page].pagestatus.toString());
                        if (data.meta[page].pagestatus.toString() === "true") {
                            privacyAdder = " <input type=\"checkbox\" id=\"" + data.meta[page].pagepk.toString() + "\" class=\"privateVpublic other\" name=\"private_v_public\" value=\"public\" checked /> " + privacyAdder;
                        } else {
                            privacyAdder = " <input type=\"checkbox\" id=\"" + data.meta[page].pagepk.toString() + "\" class=\"privateVpublic other\" name=\"private_v_public\" value=\"public\" /> " + privacyAdder;
                        }
                        link_c = link_c + privacyAdder;


                        xyz = link_a.concat(data.meta[page].linkurl).concat(link_b).concat(data.meta[page].name).concat(link_c).concat('</a>');
                        // alert(xyz);
                        //placeHolder1 = xyz.substring(xyz.indexOf('<input type="checkbox" class'), xyz.indexOf("<h4")).replace("page_deletions","privateVpublic").replace("delete","private_v_public");
                        //placeHolder2 = xyz.substring(xyz.indexOf("<h4"), xyz.indexOf("</a>")).replace( "privateVpublic","page_deletions").replace( "private_v_public","delete");
                        placeHolder1 = xyz.substring(xyz.indexOf('<input type="checkbox" class'), xyz.indexOf("<h4"));
                        placeHolder2 = xyz.substring(xyz.indexOf("<h4"), xyz.indexOf("</a>"));
                        placeHolder0 = xyz.substring(0, xyz.indexOf('<input type="checkbox" class'));


                        //Got many things from other places: this one: http://stackoverflow.com/questions/3197702/html-checkbox-onclick-called-in-javascript for the onchange
                        placeHolder2 = placeHolder2.replace('name="private_v_public"', 'onchange="private_or_public_checkbox(this);" name="private_v_public"');

                        //KCalert(placeHolder1);
                        $("#pages_on_the_fly").append(placeHolder0 +  placeHolder2 + placeHolder1+placeHolder3);   //changed
                       
                        link_c = "</h4>";                      //changed
                        privacyAdder = "";                   //changed 
                        link_a = stringer;
                        //console.log(data.meta[page].name);
                        //console.log(data.meta[page].linkurl);
                        //console.log(link_a.concat(data.meta[page].linkurl).concat(link_b).concat(data.meta[page].name).concat(link_c));
                    }
                    popup();
                    private_public_checkbox();
                    apply_bootstrapSwitches_page_slider();
                    console.log("We are here again!");
                    // alert(category_slug)
                }
            });

            



        });

    });
    
    //for deleting categories
    $(function () {
        $("#delete_categories_button.btn-primary").click(function () {
            //  e.preventDefault();
            var categories_for_deletion = "";
            //below taken from StackOverflow user113716
            $('.category_deletions').each(function () {
                if (document.getElementById(this.id).checked) {
                    categories_for_deletion= categories_for_deletion.concat(this.id.toString()).concat(",");
                    //disable visibility 
                }
            });
            categories_for_deletion = categories_for_deletion.substring(0, categories_for_deletion.length - 1);
            // alert(categories_for_deletion);
            //copied from jQuery.com
            $.ajax({
                type: "POST",
                url: "/eHealth/deleteCategory",
                data: "cats_for_deletion=" + categories_for_deletion,
                success: function (data) {
                    //the new list of categories for population
                    message = $.parseJSON(data);
                   
                   //// $("#list_of_categories").empty();
                   // //delete the list of pages, and basically user should click on it again
                   // //$("#div_containing_list_of_categories").empty();
                   // //alert(data);
                   // var insertion = "";
                   // var pk = "";
                   // var name = "";
                   // var slug = "";
                   // $("#div_containing_list_of_categories").append("<ul id=\"list_of_categories\"></ul>");
                   //// alert(message.meta.length);
                   // for (cate = 0; cate < message.meta.length; cate++) {
                   //     //add the html back again
                   //     pk = message.meta[cate].categpk.toString();
                   //     name = message.meta[cate].categname;
                   //     slug = message.meta[cate].categslug;
                   //     insertion.concat("<li><input type=\"checkbox\" class=\"category_deletions\" id=\"");
                   //     insertion.concat(pk);
                   //     insertion.concat("\" name=\"delete\" value=\"");
                   //     insertion.concat(pk);
                   //     insertion.concat("\"/> <a class=\"category_link\" id=\"");
                   //     insertion.concat(slug);
                   //     insertion.concat("\" href=\"#\">");
                   //     insertion.concat(name);
                   //     insertion.concat("</a></li>");
                        
                   //    // insertion = "";
                   // }
                   // $("#list_of_categories").append(insertion);
                    location.reload();
                    //$('.category_deletions').each(function () {
                    //    if (document.getElementById(this.id).checked) {
                    //        //categories_for_deletion = categories_for_deletion.concat(this.id.toString()).concat(";");
                    //        this.hide()
                    //        //disable visibility 
                    //    }
                    //});

                    
                }
            });

        });

    });
         
    //for Adding Categories
    $(function () {
        $('#add_category_button.btn-primary').click(function () {
            jPrompt('Type In The Category Name:', '...', 'Prompt Dialog', function (r) {
                //validateCategory(R);
                console.log(r);
                if (r) {
                    $.ajax({
                        type: "POST",
                        url: "/eHealth/addCategory",
                        data: "categoryName=" + r,
                        success: function (message) {
                            //data = $.parseJSON(message);
                            if (message === r) {
                                jAlert('The category was added!', 'Confirmation');
                            }
                            location.reload();
                        }
                    });
                }
            });
        });
    });
    



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

        $("#add_page_button.btn-primary").click(function () {
            jPrompt('Enter URL', 'Value goes here!', 'Adding a Page', function (r) {
                if (r) {
                    url = r;
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
                                        success: function (message) {
                                            $("#pages_on_the_fly").empty();
                                            data = $.parseJSON(message);
                                            category_slug = data.meta[0].category_slug
                                           
                                            //repopulate list
                                            var link_a1 = "<a href=\"#\" class=\"list-group-item \"><input type=\"checkbox\" class=\"page_deletions other\" id=\"";//+{{savedPage.pk}}+        //changed
                                            var link_a2 = "\" name=\"delete\" value=\"".concat(category_slug);//+{{category_slug}}+
                                            link_a2 = link_a2.concat("\"/>");
                                            var jaw = ' <h4 class="openNewWindow" id="';                   //changed           //
                                            var jaw2 = "\" href=\""                                        //


                                            var link_a = link_a2.concat(jaw);
                                            // link_a = "<li><a href=\"";
                                            var link_b = "\">";
                                            var link_c = "</h4>";                                          //changed
                                            var stringer = "";
                                            var privacyAdder = "";                                          //changed
                                            // $("#saved_pages_list").append("<ul id=\"pages_on_the_fly\"></ul>");
                                            var xyz = "";
                                            var placeHolder1 = "";
                                            var placeHolder2 = "";
                                            var placeHolder0 = "";
                                            var placeHolder3 = "</a>";
                                            for (page = 0; page < data.meta.length; page++) {
                                                stringer = link_a;
                                                link_a = link_a + data.meta[page].pagepk.toString();           //
                                                link_a = link_a + jaw2;                                         //
                                                link_a = link_a1.concat(data.meta[page].pagepk.toString()).concat(link_a);
                                                // alert(link_a);

                                                //alert("status of page"+data.meta[page].pagestatus.toString());
                                                if (data.meta[page].pagestatus.toString() === "true") {
                                                    privacyAdder = " <input type=\"checkbox\" id=\"" + data.meta[page].pagepk.toString() + "\" class=\"privateVpublic other\" name=\"private_v_public\" value=\"public\" checked /> " + privacyAdder;
                                                } else {
                                                    privacyAdder = " <input type=\"checkbox\" id=\"" + data.meta[page].pagepk.toString() + "\" class=\"privateVpublic other\" name=\"private_v_public\" value=\"public\" /> " + privacyAdder;
                                                }
                                                link_c = link_c + privacyAdder;

                                                xyz = link_a.concat(data.meta[page].linkurl).concat(link_b).concat(data.meta[page].name).concat(link_c).concat('</a>');
                                                // alert(xyz);
                                                placeHolder1 = xyz.substring(xyz.indexOf('<input type="checkbox" class'), xyz.indexOf("<h4"));
                                                placeHolder2 = xyz.substring(xyz.indexOf("<h4"), xyz.indexOf("</a>"));
                                                placeHolder0 = xyz.substring(0, xyz.indexOf('<input type="checkbox" class'));



                                                //placeHolder1 = placeHolder2.substring(0, '<input type="checkbox"') + placeHolder1 + placeHolder2.substring('<input type="checkbox"', placeHolder2.length);
                                                //alert(placeHolder1);

                                                //Got many things from other places: this one: http://stackoverflow.com/questions/3197702/html-checkbox-onclick-called-in-javascript for the onchange
                                                placeHolder2 = placeHolder2.replace('name="private_v_public"', 'onchange="private_or_public_checkbox(this);" name="private_v_public"');

                                                $("#pages_on_the_fly").append(placeHolder0 + placeHolder2 + placeHolder1+ placeHolder3);   //changed
                                                link_c = "</h4>";                      //changed
                                                privacyAdder = "";                   //changed 
                                                link_a = stringer;
                                                //console.log(data.meta[page].name);
                                                //console.log(data.meta[page].linkurl);
                                                //console.log(link_a.concat(data.meta[page].linkurl).concat(link_b).concat(data.meta[page].name).concat(link_c));
                                            }
                                            popup();
                                            private_public_checkbox();
                                            apply_bootstrapSwitches_page_slider();

                                            if (data.meta[0].created === "true") {
                                                var a=data.meta[0].categorypk;//pk
                                                var b=category_slug;//slug
                                                var c = data.meta[0].categoryname;//name

                                                var htML = ' <a href="#" class="list-group-item ">' +
                                    '<h4 class="list-group-item-heading category_link" id="' + b + '">' + c + '</h4>' +
                                    '<input type="checkbox" class="category_deletions other" id="' + a + '" name="delete" value="' + a + '" /> </a>';





                                                //var htML='<li><input type="checkbox" class="category_deletions" id="'+a+'" name="delete" value="'+a+'"/> <a class="category_link" id="'+b+'" href="#">'+c+'</a></li>';

                                                $("#list_of_categories").append(htML);
                                                $(".category_deletions").data("on-text", "Delete");
                                                $(".category_deletions").data("off-text", "Keep");
                                                $(".category_deletions").bootstrapSwitch();
                                            }

                                        }//,
                                      //  dataType: JSON
                                    });


                                }
                            });
                        }
                    });
                }
            });
        });
    });
    
    //for showing saved pages for a category
    $(function () {
        $(".category_link").click(function () {
            //$("#okay").hide();
            //alert(this.id);
            var category_slug = this.id;
            var xSlug = toTitleCase(category_slug);
            $(".add_the_category_name").text(xSlug + " Page(s)!");
            //console.log("We are here!");

            //alert('okay');
            //window.location.href = "http://127.0.0.1:8000/eHealth/category/";

            //$.get('/eHealth/user/category', { categoryslug: category_slug }, function (data) {
            //    alert(data);
            //});

            $.ajax({
                type: "POST",
                url: "/eHealth/category",
                //below was from Stack Overflow 
                // "category_slug=" + category_slug,
                data: "category_slug=" + category_slug,
                //csrfmiddlewaretoken: getCookie('csrftoken'),
                //dataType:"json",
                success: function (message) {
                    $("#pages_on_the_fly").empty();
                    //add in new html code with the JSON Object 
                    data = $.parseJSON(message);
                    //alert(data.meta[0].name)



                    var link_a1 = "<a href=\"#\" class=\"list-group-item \"><input type=\"checkbox\" class=\"page_deletions other\" id=\"";//+{{savedPage.pk}}+        //changed
                    var link_a2="\" name=\"delete\" value=\"".concat(category_slug);//+{{category_slug}}+
                    link_a2 = link_a2.concat("\"/>");

                    var jaw = ' <h4 class="openNewWindow" id="';                   //changed               //
                    var jaw2 = "\" href=\""                                        //


                    var link_a = link_a2.concat(jaw);
                     // link_a = "<li><a href=\"";
                    var link_b = "\">";
                    var link_c = "</h4>";                                          //changed
                    var stringer = "";
                    var privacyAdder = "";                                          //changed
                    var xyz = "";
                    var placeHolder1 = "";
                    var placeHolder2 = "";
                    var placeHolder0 = "";
                    var placeHolder3 = "</a>";
                   // $("#saved_pages_list").append("<ul id=\"pages_on_the_fly\"></ul>");
                    for (page = 0; page < data.meta.length; page++) {
                        stringer = link_a;
                        link_a = link_a + data.meta[page].pagepk.toString();           //
                        link_a = link_a + jaw2;                                         //
                        link_a= link_a1.concat(data.meta[page].pagepk.toString()).concat(link_a);
                        // alert(link_a);

                        //alert("status of page"+data.meta[page].pagestatus.toString());
                        if (data.meta[page].pagestatus.toString() === "true") {
                            privacyAdder = " <input type=\"checkbox\" id=\"" + data.meta[page].pagepk.toString() + "\" class=\"privateVpublic other\" name=\"private_v_public\" value=\"public\" checked /> " + privacyAdder;
                        } else {
                            privacyAdder = " <input type=\"checkbox\" id=\"" + data.meta[page].pagepk.toString() + "\" class=\"privateVpublic other\" name=\"private_v_public\" value=\"public\" /> " + privacyAdder;
                        }
                        link_c = link_c + privacyAdder;


                        xyz = link_a.concat(data.meta[page].linkurl).concat(link_b).concat(data.meta[page].name).concat(link_c).concat('</a>');
                       // alert(xyz);
                        placeHolder1 = xyz.substring(xyz.indexOf('<input type="checkbox" class'), xyz.indexOf("<h4"));
                        placeHolder2 = xyz.substring(xyz.indexOf("<h4"), xyz.indexOf("</a>"));
                        placeHolder0 = xyz.substring(0, xyz.indexOf('<input type="checkbox" class'));
                        

                        //alert(placeHolder0 + "       is Place Holder0");
                        //alert(placeHolder1 + "       is Place Holder1");
                       // alert(placeHolder2 + "       is Place Holder2");
                        //alert(placeHolder3 + "       is Place Holder3");


                       // //alert(placeHolder2 + "         place")
                      //  placeHolder1 = placeHolder2.substring(0, '<input type="checkbox"') + " <br/>"+ placeHolder1 + placeHolder2.substring('<input type="checkbox"', placeHolder2.length);
                        //// alert(placeHolder1);
                        // alert(placeHolder0 + placeHolder1 + placeHolder2 + placeHolder3);

                        //Got many things from other places: this one: http://stackoverflow.com/questions/3197702/html-checkbox-onclick-called-in-javascript for the onchange
                        placeHolder2 = placeHolder2.replace('name="private_v_public"', 'onchange="private_or_public_checkbox(this);" name="private_v_public"');
                       // alert(placeHolder2);
                        $("#pages_on_the_fly").append(placeHolder0 + placeHolder2+ placeHolder1+ placeHolder3);   //changed
                        //private_public_checkbox();
                        link_c = "</h4>";                      //changed
                        privacyAdder = "";                   //changed 
                        link_a = stringer;


                        //console.log(data.meta[page].name);
                        //console.log(data.meta[page].linkurl);
                        //console.log(link_a.concat(data.meta[page].linkurl).concat(link_b).concat(data.meta[page].name).concat(link_c));
                    }
                    popup();
                    private_public_checkbox();
                    apply_bootstrapSwitches_page_slider();
                    console.log("We are here again!");
                   // alert(category_slug)
                },
                error: function (xhr, errmsg, err) {

                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }

            });

        });
    });


});

function doAlert(message) {
    alert(message);
}


////NOT OUR CODE THIS WAS ON THE DJANGO WEBSITE
////the below function was taken from another place
//    function getCookie(name) {
//        var cookieValue = null;
//        if (document.cookie && document.cookie != '') {
//            var cookies = document.cookie.split(';');
//            for (var i = 0; i < cookies.length; i++) {
//                var cookie = jQuery.trim(cookies[i]);
//                // Does this cookie string begin with the name we want?
//                if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                    break;
//                }
//            }
//        }
//        return cookieValue;
//    }

//THIS CODE WAS TAKEN FOR GITHUB CSRF TOKENS!!!! There was a website that referred to it.
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