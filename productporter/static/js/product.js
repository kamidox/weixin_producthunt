/**
 * product.js
 */
$(document).ready(function () {
    // Translate & Review
    $("button[name='translate']").click(function () {
        var postid = $(this).attr('data-postid');
        var url = getTranslateUrl($(this).attr('data-url'), postid, 'translate');
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
        var url = getTranslateUrl($(this).attr('data-url'), postid, 'translate');
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
        var url = getTranslateUrl($(this).attr('data-url'), postid, 'translate');
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
                var contributor = data['contributors'];
                var tagline_content = $('.tagline-content[data-postid=' + postid + ']');
                var tagline_content_data = $('.tagline-content-data[data-postid=' + postid + ']');
                $("button[name='translate']").show();
                $('.tagline-translate[data-postid=' + postid + ']').hide();
                $('.translaters-list[data-postid=' + postid + ']').remove();
                tagline_content_data.empty();
                tagline_content_data.prepend(content);
                tagline_content.append(contributor)
                tagline_content.show();
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('Content-Type', 'application/json');
            }
        };
        $.ajax(settings);
    });

    // detailed introduce article
    $("button[name='introduce']").click(function () {
        var postid = $(this).attr('data-postid');
        var url = getTranslateUrl($(this).attr('data-url'), postid, 'introduce');
        var settings = {
            type: "GET",
            url: url,
            dataType: "json",
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var content = data['cintro'];
                $("button[name='introduce']").hide();
                $('.cintro-translate').hide();
                $('.cintro-content').show();
                $('.cintro-translate[data-postid=' + postid + ']').show();
                $('.cintro-content[data-postid=' + postid + ']').hide();
                $('textarea[name="cintro"][data-postid=' + postid + ']').val(content);
            }
        };
        $.ajax(settings);
    });

    // Cancel Translate
    $("button[name='cancel-cintro']").click(function() {
        var postid = $(this).attr('data-postid');
        var jsondata = {
            postid: postid,
            operate: 'introduce',
            canceled: 'true'
        };
        var url = getTranslateUrl($(this).attr('data-url'), postid, 'introduce');
        var settings = {
            type: "PUT",
            url: url,
            dataType: "json",
            data: JSON.stringify(jsondata),
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var content = data['cintro'];
                $("button[name='cintro']").show();
                $('.cintro-translate[data-postid=' + postid + ']').hide();
                $('.cintro-content[data-postid=' + postid + ']').show();
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('Content-Type', 'application/json');
            }
        };
        $.ajax(settings);
    });

    // Submit introduction
    $("button[name='commit-cintro']").click(function() {
        var postid = $(this).attr('data-postid');
        var cintro = $("textarea[name='cintro'][data-postid=" + postid + "]").val();
        var jsondata = {
            postid: postid,
            operate: 'introduce',
            cintro: $.trim(cintro)
        };
        var url = getTranslateUrl($(this).attr('data-url'), postid, 'introduce');
        var settings = {
            type: "PUT",
            url: url,
            dataType: "json",
            data: JSON.stringify(jsondata),
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var content = data['cintro'];
                var contributor = data['contributors'];
                var cintro_content = $('.cintro-content[data-postid=' + postid + ']');
                var cintro_content_data = $('.cintro-content-data[data-postid=' + postid + ']');
                $("button[name='introduce']").show();
                $('.cintro-translate[data-postid=' + postid + ']').hide();
                $('.translaters-list[data-postid=' + postid + ']').remove();
                cintro_content_data.empty();
                cintro_content_data.prepend(content);
                cintro_content.append(contributor)
                cintro_content.show();
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
        return url.concat("?postid=").concat(postid)
            .concat("&operate=").concat(operate);
    }
});
