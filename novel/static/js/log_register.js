$(document).ready(function(){

    $('.submit_login').on('click',submit_login_fun);

    $('.submit_register').on('click',submit_register_fun);

    $('.submit_change').on('click',submit_change_fun);


    function submit_login_fun(){
        var tel = $("#telephone_num").val().trim(); //获取手机号
        // var telReg = !!tel.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[06789]|18[0-9]|14[57])[0-9]{8}$/);
        if(tel=='') {
            $('#err_m').html('请输入用户名');
            $('#telephone_num').addClass('border-error');
            // .css({'border':'1px solid #FFA524'})
        }
        else if($('#password').val()==''){
            $('#err_m').html('请输入密码');
            $('#password').addClass('border-error');
        }
        else{
            $('.submit_login').html('正在登录...');
            // $('#password').attr('value',$.md5($('#password').val()));
            //document.form1.password.value=$.md5(document.form1.password.value);
            $('#form1').submit();
        }
    }

    function cleanChangeInput() {
        $('.change img').trigger('click');
        $('.change input').val('');
    }

    function cleanErrorMsg(){
		$('#err_m')[0].innerHTML = ''
		$('#err_m2')[0].innerHTML = ''
		$('#err_m3')[0].innerHTML = ''
        $('#telephone_num2')[0].innerHTML = ''
        $('.num_error2')[0].innerHTML = ''
        $('.password_error2')[0].innerHTML = ''
        $('.repassword_error2')[0].innerHTML = ''
    }
    function submit_register_fun(){
        var tel = $("#telephone_num2").val().trim(); //获取手机号
        // var telReg = !!tel.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[06789]|18[0-9]|14[57])[0-9]{8}$/);
        //先清除所有error
        cleanErrorMsg()

        if(tel=='') {
            $('#err_m2').html('请输入用户名');
            $('#telephone_num2').addClass('border-error');
        }

        else if($('#password2').val()==''){
            $('#err_m2').html('请输入密码');
            $('#password2').addClass('border-error');
        }

        else if($('#repassword2').val()==''){
            $('#err_m2').html('请确认密码');
            $('#repassword2').addClass('border-error');
        }

        else if($('#repassword2').val()!=$('#password2').val()){
            $('#err_m2').html('两次密码不一致');
            $('#repassword2').addClass('border-error');
        }
		
        else{
            //var md5_password=$.md5($('#password2').val());
            $.post('/app02/regist', {'password':$('#password2').val(),'username':tel}, function(data, textStatus, xhr) {
                var result = JSON.parse(data);
                if(result.status==0){
                    $('#err_m2').html(result.msg);
                }
                else{
                    //window.location.href="/";
                    window.location.reload();
                }
            });
        }

    }


    function submit_change_fun(){
        var tel = $("#telephone_num3").val().trim(); //获取手机号
        // var telReg = !!tel.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[06789]|18[0-9]|14[57])[0-9]{8}$/);
        if(tel=='') {
            $('#err_m3').html('请输入用户名');
            $('#telephone_num3').addClass('border-error');
        }

        else if($('#password3').val()==''){
            $('#err_m3').html('请输入密码');
            $('#password3').addClass('border-error');
        }

        else if($('#repassword3').val()==''){
            $('#err_m3').html('请确认密码');
            $('#repassword3').addClass('border-error');
        }

        else if($('#repassword3').val()!=$('#password3').val()){
            $('#err_m3').html('两次密码不一致');
            $('#repassword3').addClass('border-error');
        }

        else{
            $('[name="submit_register"]')[0].innerHTML = '正在提交 ... '
            //var md5_password=$.md5($('#password3').val());
            $.post('/app02/reset_password', {'password':$('#password3').val(),'username':tel}, function(data, textStatus, xhr) {
                var result = JSON.parse(data);
                if(result.status==0){
                    $('#err_m3').html(result.msg)
                    //setTimeout("$('.submit_change').html('确认修改');",4000);
                    cleanChangeInput()

                }
                else{
                    $('[name="submit_register"]')[0].innerHTML = '再次提交'
                    $('#err_m3').html(result.msg);
                }
            });

        }

    }

    $('#telephone_num').on('focus',function(){
		$('#err_m').html('');
        $('.num_error').html('');
        $('#telephone_num').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('#password').on('focus',function(){
		$('#err_m').html('');
        $('.password_error').html('');
        $('#password').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('#telephone_num2').on('focus',function(){
		$('#err_m2').html('');
        $('.num_error2').html('');
        $('#telephone_num2').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('#captcha2').on('focus',function(){
        $('.captcha_error2').html('');
        $('#captcha2').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('#captcha3').on('focus',function(){
        $('.captcha_error3').html('');
        $('#captcha3').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('#password2').on('focus',function(){
		$('#err_m2').html('');
        $('.password_error2').html('');
        $('#password2').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('#telephone_num3').on('focus',function(){
		$('#err_m3').html('');
        $('.num_error3').html('');
        $('#telephone_num3').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('#password3').on('focus',function(){
		$('#err_m3').html('');
        $('.password_error3').html('');
        $('#password3').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('#message').on('focus',function(){
        $('.message_error').html('');
        $('#message').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('#message3').on('focus',function(){
        $('.message_error3').html('');
        $('#message3').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('#repassword2').on('click',function(){
		$('#err_m2').html('');
        $('.repassword_error2').html('');
        $('#repassword2').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('#repassword3').on('click',function(){
		$('#err_m3').html('');
        $('.repassword_error3').html('');
        $('#repassword3').removeClass('border-error');
        $('.submit_error').html('');
    });

    $('.to_login').on('click',function(){
        $('.register').css({'display':'none'});
        $('.change').css({'display':'none'});
        $('.login').css({'display':'block'});
        $('.submit_error').html('');
    });

    $('.to_register').on('click',function(){
        $('.login').css({'display':'none'});
        $('.change').css({'display':'none'});
        $('.register').css({'display':'block'});
        $('.submit_error').html('');
    });

    $('.forget').on('click',function(){
        $('.change').css({'display':'block'});
        $('.login').css({'display':'none'});
        $('.register').css({'display':'none'});
        $('.submit_error').html('');
    });

    $('#send_message2').on('click',click_sendMessage2);

    $('#send_message3').on('click',click_sendMessage3);




    function click_sendMessage2(){
        cleanErrorMsg();
        // console.log('111111111111111111');
        var tel = $("#telephone_num2").val().trim(); //获取手机号
        var captcha = $("#captcha2").val().trim(); //获取验证码
        // var telReg = !!tel.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[06789]|18[0-9]|14[57])[0-9]{8}$/);
        if(tel[0]==1  && tel.length==11){
            var base64 = new Base64();
            var secret_param = base64.encode(JSON.stringify({'telephone_num':tel,'source':'web','aim':'1','type':'0'}));
            $.post('/answer/get_verification_code3/', {'secret_param': secret_param, 'captcha': captcha}, function(data, textStatus, xhr) {
                var result = data[0];
                if(result.status!=0){
                    if(result.status==5){
                        $('.message_error').html(result.msg+',请直接登录');
                    }
                    if(result.status==11){
                        $('.captcha_error2').html(result.msg);
                    }
                    else{
                        $('.message_error').html(result.msg);
                    }

                }
                else{
                    $('#send_message2').unbind('click');
                    $('#send_message2').addClass('disabled-bg');
                    var i=60;
                    var go =    function (){
                        $('#send_message2').html(i+'s');
                        if(i==0){
                            $('#send_message2').html('重新获取验证码');
                            $('#send_message2').removeClass('disabled-bg');
                            $('#send_message2').on('click',click_sendMessage2);
                            clearInterval(timer);
                        }
                        i--;
                    }
                    var timer = setInterval(go,1000);

                }

            });
        }
        else{
            $('.num_error2').html('请输入正确的手机号');
            $('#telephone_num2').addClass('border-error');
        }
    };


    function click_sendMessage3(){
        cleanErrorMsg();
        var tel = $("#telephone_num3").val().trim(); //获取手机号
        var captcha = $("#captcha3").val().trim(); //获取验证码
        // var telReg = !!tel.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[06789]|18[0-9]|14[57])[0-9]{8}$/);
        if(tel[0]==1 && tel.length==11){
            var base64 = new Base64();
            var secret_param = base64.encode(JSON.stringify({'telephone_num':tel,'source':'web','aim':'2','type':'0'}));
            $.post('/answer/get_verification_code3/', {"secret_param": secret_param, "captcha": captcha}, function(data, textStatus, xhr) {
                var result = data[0];
                if(result.status!=0){
                    if (result.status==11) {
                        $('.captcha_error3').html(result.msg);
                    }
                    else {
                        $('.message_error3').html(result.msg);
                    }
                }
                else{
                    $('#send_message3').unbind('click');
                    $('#send_message3').addClass('disabled-bg');
                    var i=60;
                    var go = function (){
                        $('#send_message3').html(i+'s');
                        if(i==0){
                            $('#send_message3').html('重新获取验证码');
                            $('#send_message3').removeClass('disabled-bg');
                            $('#send_message3').on('click',click_sendMessage3);
                            clearInterval(timer);
                        }
                        i--;
                    };
                    var timer = setInterval(go,1000);

                }

            });
        }
        else {
            $('.num_error3').html('请输入正确的手机号');
            $('#telephone_num3').addClass('border-error');
        }
    }




    (function(){
            document.onkeydown = function(e){
                var ev = document.all ? window.event : e;
                if(ev.keyCode==13) {
                    if($('.login').css('display')=='block'){
                        submit_login_fun();
                    }
                    if($('.register').css('display')=='block'){
                        submit_register_fun();
                    }
                    if($('.change').css('display')=='block'){
                        submit_change_fun();
                    }

                }

            }
    })();







});
