/*
     Update personal user information module.
*/

// format correctly the text showed on the screen
function render_text(string){
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase()
}

// main function
$(function() {

    // Update the input field information value quering the database
    $("#profile").click(function(event){
        event.preventDefault();

        $('document').ready(function(){

            // create Profile Header
            loadProfileHeader();

            //get token from cookie
            Cookies.json = true;  // important
            var token = Cookies.get("session_token");

            // Post request
            $.ajax({
                url: 'http://127.0.0.1:5000/getProfile?token='+token,
                success: function(response) {

                    var profile = response['profile'];
                    $("#first_name_textfield")[0].MaterialTextfield.change(profile['first_name']);
                    $("#last_name_textfield")[0].MaterialTextfield.change(profile['last_name']);
                    $("#email_textfield")[0].MaterialTextfield.change(profile['email']);
                    $("#cellphone_textfield")[0].MaterialTextfield.change(profile['cellphone']);

                    switch (profile['gender']) {
                        case "male":
                            document.querySelector('#gender_radio_male').MaterialRadio.check();
                            break;
                        case "female":
                            document.querySelector('#gender_radio_female').MaterialRadio.check();
                            break;
                        default:
                            document.querySelector('#gender_radio_male').MaterialRadio.uncheck();
                            document.querySelector('#gender_radio_female').MaterialRadio.uncheck();
                    }
                    (profile['notify_tel'])?  document.querySelector('#notificate_tel_checkbox').MaterialCheckbox.check() :
                                              document.querySelector('#notificate_tel_checkbox').MaterialCheckbox.uncheck();

                    //update profile image
                    if(profile['image']) {
                        document.querySelector('#avatar_image').src = profile['image'];
                    }
                    componentHandler.upgradeDom();
                },
                error: function(error) {
                    errorDialog(error);
                }
            });

        });
    });

    // Submit new profile information -- delegate to descendants
    $("#stage").on("submit", "#information-panel", function (event){

        event.preventDefault();

        //get token from cookie
        Cookies.json = true;  // important
        var token = Cookies.get("session_token");

        var first_name = render_text($('#first_name').val());
        var last_name = render_text($('#last_name').val());
        var cellphone = $('#cellphone').val();
        var gender = $('input[name = gender]:checked').val();

        // NOT IMPLEMENTED YET
        // var email = $('#email').val();
        //  var notify_tel = $('input[id = notificate-tel]').prop("checked");
        // var notify_email = $('input[id = notificate-email]:checked').val();

        // Post request to /modProfile
        $.ajax({
            url: 'http://127.0.0.1:5000/modProfile',
            dataType: 'text',
            contentType: "application/json; charset=utf-8",
            type: 'post',
            data: JSON.stringify( { "token" : token,
                                    "first_name": first_name, "last_name": last_name,
                                    "cellphone" : cellphone, "gender" : gender} ),

            success: function(response) {

                // Show a friendly event_section
                submitDialog("Informations updated correctly.");
            },
            error: function(error) {
                errorDialog(error);
            }
        });
    });
});