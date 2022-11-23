$(function(){
    //ここから、LINE通知（非同期通信）のコード
    //result.htmlのタスクを取得してくる
    $("#btn1").click(function(e){
        e.preventDefault();
        var task = $("#task1").val();
        //↑で値（task）の取得はできた
        
        data = {"task": task};
        json = JSON.stringify(data);  // object型からJSON文字列(string型)に変換
        $.ajax({
            type: "POST",
            url: "/line",
            data: json,
            contentType: "application/json",
         
            success: function(msg) {
                let line = "<p>LINE通知は成功しました<br>あとは行動するだけですね！！</p>"
                $("div.line").html(line)
                console.log("成功");
            },
            error: function(msg) {
                console.log("error");
            }
        });
        
    })
    //ここまで、LINE通知（非同期通信）のコード



    
})



