$(document).ready(function(){
//添加项目域名
  $(".add_project_domain").click(function(){
  var data_url = $(this).attr("data-url");
  var data_pid = $(this).attr("data-pid");
   $.ajax({
            cache: true,
            type: "GET",
            url:data_url,
            async: true,
            error: function(request) {
                alert("服务端错误：500");
            },
            success: function(data) {
                $("#FormModal").html(data);
                $("#input-pid").val(data_pid);
                $("#ajax_add_submit").click(function(){
                $.ajax({
                    cache: true,
                    type: "POST",
                    url:data_url,
                    data:$('#ajax_form').serialize(),// 你的formid
                    async: true,
                    error: function(request) {
                        alert("服务端错误:500");
                    },
                    success: function(data) {
                        alert(data);
                        history.go(0);
                    }
              });
            });
            }
      });
});

  //删除项目域名
  $('.del_project_domain').click(function(){
  var data_url = $(this).attr('data-url');
  var data_pid = $(this).attr('data-pid');
  var data_id = $(this).attr('data-id');
  $.ajax({
            cache: false,
            type: "GET",
            url:data_url,
            async: true,
            error: function(request) {
                alert("服务端错误:500");
            },
            success: function(data) {
                $("#FormModal").html(data);
                $("#input-id").val(data_id);
                $("#input-pid").val(data_pid);
                $("#ajax_del_submit").click(function(){
                  $.ajax({
                            cache: false,
                            type: "POST",
                            url:data_url,
                            data:$('#ajax_form').serialize(),// 你的formid
                            async: true,
                            error: function(request) {
                                alert("服务端错误:500");
                            },
                            success: function(data) {
                                alert(data);
                                history.go(0);
                            }
                      });
                  });
            }
      });
  });

//添加项目网站
  $(".add_project_site").click(function(){
  var data_url = $(this).attr("data-url");
  var data_pid = $(this).attr("data-pid");
   $.ajax({
            cache: true,
            type: "GET",
            url:data_url,
            async: true,
            error: function(request) {
                alert("服务端错误：500");
            },
            success: function(data) {
                $("#FormModal").html(data);
                $("#input-pid").val(data_pid);
                $("#ajax_add_submit").click(function(){
                $.ajax({
                    cache: true,
                    type: "POST",
                    url:data_url,
                    data:$('#ajax_form').serialize(),// 你的formid
                    async: true,
                    error: function(request) {
                        alert("服务端错误:500");
                    },
                    success: function(data) {
                        alert(data);
                        history.go(0);
                    }
              });
            });
            }
      });
});

 //删除项目网站
  $('.del_project_site').click(function(){
  var data_url = $(this).attr('data-url');
  var data_pid = $(this).attr('data-pid');
  var data_id = $(this).attr('data-id');
  $.ajax({
            cache: false,
            type: "GET",
            url:data_url,
            async: true,
            error: function(request) {
                alert("服务端错误:500");
            },
            success: function(data) {
                $("#FormModal").html(data);
                $("#input-id").val(data_id);
                $("#input-pid").val(data_pid);
                $("#ajax_del_submit").click(function(){
                  $.ajax({
                            cache: false,
                            type: "POST",
                            url:data_url,
                            data:$('#ajax_form').serialize(),// 你的formid
                            async: true,
                            error: function(request) {
                                alert("服务端错误:500");
                            },
                            success: function(data) {
                                alert(data);
                                history.go(0);
                            }
                      });
                  });
            }
      });
  });

//添加项目IP
  $(".add_poj_ip").click(function(){
  var data_url = $(this).attr("data-url");
  var data_pid = $(this).attr("data-pid");
   $.ajax({
            cache: true,
            type: "GET",
            url:data_url,
            async: true,
            error: function(request) {
                alert("服务端错误：500");
            },
            success: function(data) {
                $("#FormModal").html(data);
                $("#input-pid").val(data_pid);
                $("#ajax_add_submit").click(function(){
                $.ajax({
                    cache: true,
                    type: "POST",
                    url:data_url,
                    data:$('#ajax_form').serialize(),// 你的formid
                    async: true,
                    error: function(request) {
                        alert("服务端错误:500");
                    },
                    success: function(data) {
                        alert(data);
                        history.go(0);
                    }
              });
            });
            }
      });
});

//删除项目IP
  $('.del_project_ip').click(function(){
  var data_url = $(this).attr('data-url');
  var data_pid = $(this).attr('data-pid');
  var data_id = $(this).attr('data-id');
  $.ajax({
            cache: false,
            type: "GET",
            url:data_url,
            async: true,
            error: function(request) {
                alert("服务端错误:500");
            },
            success: function(data) {
                $("#FormModal").html(data);
                $("#input-id").val(data_id);
                $("#input-pid").val(data_pid);
                $("#ajax_del_submit").click(function(){
                  $.ajax({
                            cache: false,
                            type: "POST",
                            url:data_url,
                            data:$('#ajax_form').serialize(),// 你的formid
                            async: true,
                            error: function(request) {
                                alert("服务端错误:500");
                            },
                            success: function(data) {
                                alert(data);
                                history.go(0);
                            }
                      });
                  });
            }
      });
  });

 });
