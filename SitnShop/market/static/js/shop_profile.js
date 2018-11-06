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


 $(document).ready(function() {
  	var action = $('.followProfile').attr('action')
  	var shop_id = $('.followProfile').attr('shop_id')
	$.ajax({
	        type:"POST",
			url: "/check_follow_status/",
			data: {
			  id: shop_id
			},
			success: function(data){
			console.log(data)
			action = data.action
			console.log(action)
			   $('.followProfile').attr('action', action)
		       $('#follow_text').html(action)
			   <!--alert(data.message);-->
        	}
        });
  });

  $(document).ready(function() {
	$('.followProfile').on('click', function(){
    	console.log("here " + $(this).attr('shop_id') + " " + $(this).attr('action'))
    	var action = $('.followProfile').attr('action')
		var shop_id = $('.followProfile').attr('shop_id')
		$.ajax({
		    type:"POST",
		    url: "/follow_shop/",
			data: {
			  id: shop_id,
			  action: action
			},
			success: function(data){
			console.log(data)
			action = data.action
			console.log(action)
			   $('.followProfile').attr('action', action)
			   $('#follow_text').html(action)
			   <!--alert(data.message);-->
			}
		});
    });
  });