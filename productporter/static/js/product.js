/**
 * product.js
 */
$(document).ready(function () {
    // Translate & Review
    $("button[name='translate']").click(function () {
        var postid = $(this).attr('data-postid');
        var field = $(this).attr('field');
        var url = addTranslateParam($(this).attr('data-url'), postid, field);
        var settings = {
            type: "GET",
            url: url,
            dataType: "json",
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var content = data['value'];
                $('button[name="lock"]').hide();
                $('.tagline-translate[field=' + field + ']').hide();
                $('.tagline-content[field=' + field + ']').show();
                $('.tagline-translate[data-postid=' + postid + '][field=' + field + ']').show();
                $('.tagline-content[data-postid=' + postid + '][field=' + field + ']').hide();
                $('textarea[name=' + field + '][data-postid=' + postid + ']').val(content);
            }
        };
        $.ajax(settings);
    });

    // Cancel Translate
    $("button[name='cancel']").click(function() {
        var postid = $(this).attr('data-postid');
        var field = $(this).attr('field');
        var jsondata = {
            postid: postid,
            field: field,
            canceled: 'true'
        };
        var url = addTranslateParam($(this).attr('data-url'), postid, field);
        var settings = {
            type: "POST",
            url: url,
            dataType: "json",
            data: JSON.stringify(jsondata),
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                $('button[name="lock"]').show();
                $('.tagline-translate[data-postid=' + postid + '][field=' + field + ']').hide();
                $('.tagline-content[data-postid=' + postid + '][field=' + field + ']').show();
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('Content-Type', 'application/json');
            }
        };
        $.ajax(settings);
    });

    // Commit Translate
    $("button[name='commit']").click(function() {
        var postid = $(this).attr('data-postid');
        var field = $(this).attr('field');
        var value = $("textarea[name=" + field + "][data-postid=" + postid + "]").val();
        var tags = $('input[name="tag"][data-postid=' + postid + ']').val();
        var jsondata = {
            postid: postid,
            field: field,
            value: $.trim(value),
            tags: $.trim(tags)
        };
        var url = addTranslateParam($(this).attr('data-url'), postid, field);
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
                var tagline_content = $('.tagline-content[data-postid=' + postid + '][field=' + field + ']');
                var tagline_content_data = $('.tagline-content-data[data-postid=' + postid + '][field=' + field + ']');
                $('button[name="lock"]').show();
                $('.tagline-translate[data-postid=' + postid + '][field=' + field + ']').hide();
                $('.translaters-list[data-postid=' + postid + '][field=' + field + ']').remove();
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

    // lock and unlock ctagline
    $("button[name='lock']").click(function () {
        var postid = $(this).attr('data-postid');
        var op = $(this).attr('op');
        var field = $(this).attr('field');
        var url = addLockParam($(this).attr('data-url'), postid, field, op);
        var settings = {
            type: "GET",
            url: url,
            dataType: "json",
            error: function(XHR,textStatus,errorThrown) {
                alert ("textStatus="+textStatus+"\nerrorThrown=" + errorThrown);
            },
            success: function(data,textStatus) {
                var translate_btn = $('button[name="translate"][data-postid=' + postid + '][field=' + field + ']');
                var lock_btn = $('button[name="lock"][data-postid=' + postid + '][field=' + field + ']');
                if(op.toLowerCase() == 'lock') {
                    translate_btn.attr('class', 'btn btn-primary fix-width hide');
                    lock_btn.attr('op', 'unlock');
                    lock_btn.text('Unlock');
                } else {
                    translate_btn.attr('class', 'btn btn-primary fix-width show');
                    lock_btn.attr('op', 'lock');
                    lock_btn.text('Lock');
                }
                var translaters_list = $('.translaters-list[data-postid=' + postid + '][field=' + field + ']');
                translaters_list.remove();
                var contributors = data['contributors'];
                $('.tagline-content[data-postid=' + postid + '][field=' + field + ']').append(contributors);
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

    // tags
    $("span[name='build-in-tag']").click(function () {
        var postid = $(this).attr('data-postid');
        var tags = $('input[name="tag"][data-postid=' + postid + ']');
        var tagnames = tags.val();
        if (tagnames) {
            tags.val(tagnames + "; " + $(this).attr('data-name'));
        } else {
            tags.val($(this).attr('data-name'));
        }
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
