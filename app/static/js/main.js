$(function() {

    // display words count
    countwords = function() {
      var text = $('#text').val();
      if (text) {
        var wordcount = text.match(/\S+/g).length
        $('#wordcount').val(wordcount)
      }
    }

    countwords()
    $('#text').keyup(countwords);

    // process form
    $('.error').hide();
    $('.subbutton').click(function() {

      // validate and process form here

      $('.error').hide();
      var name = $("#name").val();
        if (name == "") {
          $("#name_error").show();
          $("#name_error").html('Name field can not be empty');
          $("#name").focus();
          return false;
        }

      var email = $("#email").val();
      if (email == "") {
        $("#email_error").show();
        $("#email_error").html('Email field can not be empty');
        $("#email").focus();
        return false;
      }

      var email = $("#email").val();
      if ( !isValidEmailAddress( email ) ) {
        $("#email_invalid_error").show();
        $("#email_invalid_error").html('This email address is not valid');
        $("#email").focus();
        return false;
      }

      var phone = $("#phone").val();
      if (phone == "") {
        $("#phone_error").show();
        $("#phone_error").html('Phone field can not be empty');
        $("#phone").focus();
        return false;
      }

      var organization = $("#organization").val();
      if (organization == "") {
        $("#organization_error").show();
        $("#organization_error").html('Company field can not be empty');
        $("#organization").focus();
        return false;
      }

      var text = $("#text").val();
      if (text == "") {
        $("#text_error").show();
        $("#text_error").html('Text field can not be empty');
        $("#text").focus();
        return false;
      }

      /*
      var accept = $("#accept");
      console.log(accept);
      if (!$(accept).is(':checked')) {
        $("#accept_error").show();
        $("#accept_error").html('You must accept our Master Service Agreement');
        $("#accept_error").focus();
        return false;
      }
      */

      /*
      var dataString = '<p><strong>Name: </strong> '+ name + '</p><p><strong>Email: </strong> ' + email + '</p><p><strong>Message: </strong> ' + message + '</p>';
      $.ajax({
        type: "POST",
        url: "/jobs/submit/",
        data: $('#request').serialize(),
        success: function() {
          // show a success message to your visitors
          //$('.message').html('Your request had been sent. We will contact you shortly.');
          window.location = '/jobs/confirm/';

         // clear input field values
          $("#name").val('');
          $("#email").val('');
          $("#company").val('');
          $("#text").val('');
        }
      });
      return false;
      */

      return true;

    });
});


// Validate the email address
function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
    return pattern.test(emailAddress);
};
