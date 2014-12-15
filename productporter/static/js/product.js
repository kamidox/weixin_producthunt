/**
 * product.js
 */
$(document).ready(function () {
    // Translate & Review
    $("button[name='translate']").click(function () {
        var postid = $(this).attr('data-postid');
        console.log('translate button click postid=' + postid);
        $('.tagline-translate').hide();
        $('.tagline-content').show();
        $('.tagline-translate[data-postid=' + postid + ']').show();
        $('.tagline-content[data-postid=' + postid + ']').hide();
        var tagline = $('.tagline-content-data[data-postid=' + postid + ']').text();
        $('textarea[name="ctagline"][data-postid=' + postid + ']').val($.trim(tagline));
    });

    // Cancel Translate
    $("button[name='cancel']").click(function() {
        var postid = $(this).attr('data-postid');
        $('.tagline-translate[data-postid=' + postid + ']').hide();
        $('.tagline-content[data-postid=' + postid + ']').show();
    });

    // Submit Translate
    $("button[name='update']").click(function() {
        var postid = $(this).attr('data-postid');
        var ctagline = $("textarea[name='ctagline'][data-postid=" + postid + "]").val();
        var jsondata = {
            postid: postid,
            ctagline: $.trim(ctagline)
        };
        var settings = {
            type: "PUT",
            url: window.location.href,
            dataType: "json",
            data: JSON.stringify(jsondata),
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var content = data['ctagline'];
                $('.tagline-content-data[data-postid=' + postid + ']').empty();
                $('.tagline-content-data[data-postid=' + postid + ']').prepend(content);
                $('.tagline-translate[data-postid=' + postid + ']').hide();
                $('.tagline-content[data-postid=' + postid + ']').show();
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('Content-Type', 'application/json');
            }
        };
        $.ajax(settings);
    });
});
