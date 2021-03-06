/**
 * @module profile_module/profile_password
 * @description handles the change password.
 * @listens click
 * @fires ajax post
 */

/**
 * Check if password and retype password are the same.
 * @param {String} password
 * @param {String} retype_password
 * @returns {boolean}
 */

// check if password and retype password are the same and not empty
function passwordCheck(password, retype_password) {
     return !(password.length === 0) && (password === retype_password);
}

/**
 * @external ".click()"
 * @see {@link http://api.jquery.com/click/}
 */

/**
 * @external ".on()"
 * @see {@link http://api.jquery.com/on/}
 */

/**
 * @external "jQuery.ajax"
 * @see {@link http://api.jquery.com/category/ajax/global-ajax-event-handlers/}
 */


// main function
$(function() {
    $("#stage").on("click", "#submit_password", function (event){

        event.preventDefault();

        //get token from cookie
        Cookies.json = true;  // important
        var token = Cookies.get("session_token");

        var current_password = $('#current_password').val();
        var new_password = $('#new_password').val();
        var retype_new_password = $('#retype_new_password').val();

        // password check
        if(!passwordCheck(new_password, retype_new_password)){

            // Show a friendly event_section
            errorDialog("The passwords do not match");
            throw error;
        }

        //show loading page
        showLoading();

        // ajax post request
        $.ajax({
            url: 'http://127.0.0.1:5000/modProfilePassword',
            dataType: 'text',
            contentType: "application/json; charset=utf-8",
            type: 'post',
            data: JSON.stringify( { "token" : token,
                "current_password": current_password, "new_password": new_password} ),

            success: function(response) {

                // redirect if token is null
                sessionExpired(response);

                // hide loading page
                hideLoading();

                // Show a friendly event_section
                submitDialog("Password updated correctly.", "");
            },
            error: function(error) {
                window.location = "html/server_down.html"
            }
        });
    });
});