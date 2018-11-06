function readURL(input)
{
    if (input.files && input.files[0]) 
    {
        var reader = new FileReader();

        reader.onload = function (e) 
        {
            $('#Uimage').attr('src', e.target.result).width(250).show();
            $('#drop').hide();
            $('#or').hide();
            $('#image_icon').hide();
            $('#cancel').show();
            $('#browse').hide();
        };

        reader.readAsDataURL(input.files[0]);
    }
}