$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
    }
});

$(document).ready(function() {
	$.ajax({
	        type:"POST",
			url: "/get_quick_adds/",
			data: {
			  id: "test_id"
			},
			success: function(data){
			    console.log(data.quick_adds)
			    initDemo(data.quick_adds)
        	}
        });
  });

var initDemo = function(data_from_django){
    var timeIndex = 0;
    var shifts = [35, 60, 60*3, 60*60*2, 60*60*25, 60*60*24*4, 60*60*24*10];
    var timestamp = function() {
        var now = new Date();
        var shift = shifts[timeIndex++] || 0;
        var date = new Date( now - shift*1000);

        return date.getTime() / 1000;
    };
    console.log(data_from_django)
    var stories = new Zuck('stories', {
        backNative: true,
        previousTap: true,
        autoFullScreen: false,
        skin: 'Snapssenger',
        avatars:false,
        list: false,
        cubeEffect: false,
        localStorage: true,
        stories:data_from_django,
    });
    document.body.style.display = 'block';
};
