/**
 * product.js
 */
$(document).ready(function () {
    // Translate & Review
    $("button[name='translate']").click(function () {
        var postid = $(this).attr('data-postid');
        var url = getTranslateUrl(window.location.href, postid, 'translate');
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
        var jsondata = {
            postid: postid,
            operate: 'translate',
            canceled: 'true'
        };
        var url = getTranslateUrl(window.location.href, postid, 'translate');
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
                $('.tagline-translate[data-postid=' + postid + ']').hide();
                $('.tagline-content[data-postid=' + postid + ']').show();
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('Content-Type', 'application/json');
            }
        };
        $.ajax(settings);
    });

    // Submit Translate
    $("button[name='commit-translate']").click(function() {
        var postid = $(this).attr('data-postid');
        var ctagline = $("textarea[name='ctagline'][data-postid=" + postid + "]").val();
        var jsondata = {
            postid: postid,
            operate: 'translate',
            ctagline: $.trim(ctagline)
        };
        var url = getTranslateUrl(window.location.href, postid, 'translate');
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

    function getTranslateUrl(url, postid, operate) {
        if (postid) {
            return getUrlParent(url).concat("/translate?postid=").concat(postid)
                .concat("&operate=").concat(operate);
        } else {
            return getUrlParent(url).concat("/translate")
        }
    }

    function getUrlParent(url) {
        var index = url.lastIndexOf("/");
        return url.substring(0, index);
    }
});
