/**
 * product.js
 */
$(document).ready(function () {
    // Translate & Review
    $("button[name='translate']").click(function () {
        var postid = $(this).attr('data-postid');
        var url = addTranslateParam($(this).attr('data-url'), postid, 'ctagline');
        var settings = {
            type: "GET",
            url: url,
            dataType: "json",
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var content = data['value'];
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
            field: 'ctagline',
            canceled: 'true'
        };
        var url = addTranslateParam($(this).attr('data-url'), postid, 'ctagline');
        var settings = {
            type: "PUT",
            url: url,
            dataType: "json",
            data: JSON.stringify(jsondata),
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
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

    // Commit Translate
    $("button[name='commit-translate']").click(function() {
        var postid = $(this).attr('data-postid');
        var ctagline = $("textarea[name='ctagline'][data-postid=" + postid + "]").val();
        var jsondata = {
            postid: postid,
            field: 'ctagline',
            value: $.trim(ctagline)
        };
        var url = addTranslateParam($(this).attr('data-url'), postid, 'ctagline');
        var settings = {
            type: "POST",
            url: url,
            dataType: "json",
            data: JSON.stringify(jsondata),
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var content = data['value'];
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

    // aquire translate for cintro
    $("button[name='introduce']").click(function () {
        var postid = $(this).attr('data-postid');
        var url = addTranslateParam($(this).attr('data-url'), postid, 'cintro');
        var settings = {
            type: "GET",
            url: url,
            dataType: "json",
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var content = data['value'];
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
            field: 'cintro',
            canceled: 'true'
        };
        var url = addTranslateParam($(this).attr('data-url'), postid, 'cintro');
        var settings = {
            type: "POST",
            url: url,
            dataType: "json",
            data: JSON.stringify(jsondata),
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
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

    // Commit cintro
    $("button[name='commit-cintro']").click(function() {
        var postid = $(this).attr('data-postid');
        var cintro = $("textarea[name='cintro'][data-postid=" + postid + "]").val();
        var jsondata = {
            postid: postid,
            field: 'cintro',
            value: $.trim(cintro)
        };
        var url = addTranslateParam($(this).attr('data-url'), postid, 'cintro');
        var settings = {
            type: "POST",
            url: url,
            dataType: "json",
            data: JSON.stringify(jsondata),
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var content = data['value'];
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

    // lock and unlock ctagline
    $("button[name='lock']").click(function () {
        var postid = $(this).attr('data-postid');
        var op = $(this).attr('op');
        var url = addLockParam($(this).attr('data-url'), postid, 'ctagline', op);
        var settings = {
            type: "GET",
            url: url,
            dataType: "json",
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var translate_btn = data['translate']
                var lock_btn = data['lock']
                var div_translate = $('div[name="translate-btn"][data-postid=' + postid + ']');
                var div_lock = $('div[name="lock-btn"][data-postid=' + postid + ']');
                div_translate.empty();
                div_lock.empty();
                div_translate.append(translate_btn);
                div_lock.append(lock_btn);
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

    function addTranslateParam(url, postid, field) {
        return url.concat("?postid=").concat(postid)
            .concat("&field=").concat(field);
    }

    function addLockParam(url, postid, field, op) {
        return url.concat("?postid=").concat(postid)
            .concat("&field=").concat(field)
            .concat("&op=").concat(op);
    }
});
