$(document).on('click','#add',function(){
        $('#AddOption').append('<div class="row"><div class="col-lg-4"><div class="form-group"><input type="text" class="form-control opt"></div></div>');
    });
    $(document).on('click','#remove',function(){
        $('#AddOption').children().last().remove();
    });

    $(document).on('click','#create',function(){
        var options=[];
        var url;
        var question=$('#question').val();
        $('.opt').each(function() {
            var val=$( this ).val();
            options.push(val);
        });
        var pid=$('#title').html();
        var edit = /^\d+$/.test(pid);
        if(edit){
            url=('/edit/').concat(pid);
            url=url.concat('/')
        }
        else{
            url='/create/'
        }
         $.ajax({
            url:url,
            type:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
                //csrftoken code updated in base_layout.html
            },
            data: JSON.stringify({'question':question,'options':options}),
            success:function(data){
                $('body').html(data);
            },
            error:function(){
                alert("error");
            }
        });
    });
