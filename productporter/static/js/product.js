/**
 * product.js
 */
$(document).ready(function () {
    // Translate
    $('.tagline-content .btn.btn-primary.btn-translate').click(function () {
        var postid = $(this).attr('data-postid');
        console.log('translate button click postid=' + postid);
        $('.tagline-translate').hide();
        $('.tagline-content').show();
        $('.tagline-translate[data-postid=' + postid + ']').show();
        $('.tagline-content[data-postid=' + postid + ']').hide();
        var tagline = $('.tagline-content-data[data-postid=' + postid + ']').text();
        $('textarea#ctagline[data-postid=' + postid + ']').text($.trim(tagline));
    });
});
