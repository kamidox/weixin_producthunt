/**
 * product.js
 */
$(document).ready(function () {
    // Translate & Review
    $("button[name='translate']").click(function () {
        var postid = $(this).attr('data-postid');
        var url = getPostUrl(window.location.href, postid);
        var settings = {
            type: "GET",
            url: url,
            dataType: "json",
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var content = data['ctagline'];
                $("button[name='translate']").hide();
                $('.tagline-translate').hide();
                $('.tagline-content').show();
                $('.tagline-translate[data-postid=' + postid + ']').show();
                $('.tagline-content[data-postid=' + postid + ']').hide();
                $('textarea[name="ctagline"][data-postid=' + postid + ']').val(content);
            }
        };
        $.ajax(settings);
    });

    // Cancel Translate
    $("button[name='cancel']").click(function() {
        var postid = $(this).attr('data-postid');
        $('.tagline-translate[data-postid=' + postid + ']').hide();
        $('.tagline-content[data-postid=' + postid + ']').show();
    });

    // Submit Translate
    $("button[name='commit-translate']").click(function() {
        var postid = $(this).attr('data-postid');
        var ctagline = $("textarea[name='ctagline'][data-postid=" + postid + "]").val();
        var jsondata = {
            postid: postid,
            ctagline: $.trim(ctagline)
        };
        var url = getPostUrl(window.location.href, postid);
        var settings = {
            type: "PUT",
            url: url,
            dataType: "json",
            data: JSON.stringify(jsondata),
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var content = data['ctagline'];
                $("button[name='translate']").show();
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

    // Show or Hide sreenshot
    // $("button#btn-show-screenshot").click(function() {
    //     if ($(this).text().indexOf('Show') >= 0) {
    //         $('tr.post-screenshot').show();
    //         $('td.post-index').attr('rowspan', 3);
    //         $(this).text('Hide screenshot');
    //     } else {
    //         $('tr.post-screenshot').hide();
    //         $('td.post-index').attr('rowspan', 2);
    //         $(this).text('Show screenshot');
    //     }
    // });

    // datepicker
    $('#input-select-day input').datepicker({
        format: "yyyy-mm-dd",
        todayBtn: "linked",
        language: "zh-CN",
        autoclose: true,
        todayHighlight: true
    }).on('changeDate', function(e) {
        var day = e.format('yyyy-mm-dd');
        var url = window.location.origin + window.location.pathname + '?day=' + day;
        window.location.href = url;
    });

    function getPostUrl(url, postid) {
        if (postid) {
            return getUrlParent(url).concat("/post?postid=").concat(postid);
        } else {
            return getUrlParent(url).concat("/post")
        }
    }

    function getUrlParent(url) {
        var index = url.lastIndexOf("/");
        return url.substring(0, index);
    }
});
