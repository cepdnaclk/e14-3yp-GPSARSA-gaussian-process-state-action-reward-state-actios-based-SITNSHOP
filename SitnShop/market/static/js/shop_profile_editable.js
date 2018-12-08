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

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
    }
});

function get_hash_tags() {
   var hash_tags_list = $("#hash_tags_list");
    var shop_id = $("#hash_tags_list").attr('shop_id')
    console.log(shop_id)
	$.ajax({
	        type:"POST",
			url: "/get_hash_tags/",
			data: {
			  id: shop_id
			},
			success: function(data) {
			    pending_tags = data.pending_tags
			    for (let i = 0; i < pending_tags.length; i++) {
                   var tag = $('<br /><input id='+pending_tags[i].pk+' type="checkbox" name="tags[]" value='+pending_tags[i].tag_name+'>'+
                            '<label for='+pending_tags[i].pk+'>'+pending_tags[i].tag_name+'</label>');
                    hash_tags_list.append(tag);
                }
                shop_hash_tags = data.shop_hash_tags
			    for (let i = 0; i < shop_hash_tags.length; i++) {
                   var tag = $('<br /><input id='+shop_hash_tags[i].pk+' type="checkbox" name="tags[]" checked="true" value='+shop_hash_tags[i].tag_name+'>'+
                            '<label for='+shop_hash_tags[i].pk+'>'+shop_hash_tags[i].tag_name+'</label>');
                    hash_tags_list.append(tag);
                }
			    console.log(data)
//                selectMembers.multiSelect('refresh');
//                alert("test3");
            }
        });
}



$(document).ready(function() {
get_hash_tags();
});

$(document).ready(function() {
    $("#save_tags").click(function(){
        var tag_list = {};
        var i = 0;
        var shop_id = $("#hash_tags_list").attr('shop_id')
        $("input[name='tags[]']:checked").each(function ()
        {
//            console.log($(this).attr('id'))
            tag_list[i++] = parseInt($(this).attr('id'));
        });
        console.log(tag_list)
        var tags_list = JSON.stringify(tag_list);
//        console.log(tags_list)
        var data = {}
        data["id"] = shop_id;
        data["tags"] = tags_list;

        $.ajax({
	        type:"POST",
			url: "/set_hash_tags/",
			data:data,
			success: function(data) {
			    console.log(data)
            }
        });
    });
});