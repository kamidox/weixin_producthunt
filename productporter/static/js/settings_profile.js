/**
 * settings_profile.js
*/

$(document).ready(function() {
    $('input#birthday').datepicker({
        format: "yyyy-mm-dd",
        todayBtn: "linked",
        language: "zh-CN",
        autoclose: true,
        todayHighlight: true
    });
});
