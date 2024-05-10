function on_btn_voice_click(btn_ind) {
    $.ajax({
        type: "POST",
        url : "/btn",
        data: {'btn_ind': btn_ind},
        dataType: 'json',
        success: function(response) {
            $('#voices1').html(response.voices1)
            $('#voices2').html(response.voices2)
            $('#voices3').html(response.voices3)
            $('#voices4').html(response.voices4)
        },
        error: function(error) {
            console.log(error);
        }
    });
};

function on_btn_msg_click() {
    $.ajax({
        type: "POST",
        url : "/msg",
        data: {'msg': document.getElementById('message').value},
        dataType: 'json',
        success: function(response) {
            $('#chat').html(response.chat)
            document.getElementById('message').value = ""
        },
        error: function(error) {
            console.log(error);
        }
    });
};

setInterval(function() {
    $.ajax({
        type: "POST",
        url : "/process",
        success: function(response) {
            $('#voices1').html(response.voices1)
            $('#voices2').html(response.voices2)
            $('#voices3').html(response.voices3)
            $('#voices4').html(response.voices4)
            $('#chat').html(response.chat)
        },
        error: function(error) {
            console.log(error);
        }
    });
}, 100);