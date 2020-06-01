$(function () {
    function hide_stream_update() {
      $(".stream-update").hide();
    };
  
    function getCookie(name) {
      // Function to get any cookie available in the session.
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    };
  
    function csrfSafeMethod(method) {
      // These HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
  
    var csrftoken = getCookie('csrftoken');
    var page_title = $(document).attr("title");
    // This sets up every ajax call with proper headers.
    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
  
    // Focus on the modal input by default.
    $('#newsFormModal').on('shown.bs.modal', function () {
      $('#newsInput').trigger('focus')
    });
  
    $('#newsThreadModal').on('shown.bs.modal', function () {
      $('#replyInput').trigger('focus')
    });
  
    // Counts textarea characters to provide data to user.
    $("#newsInput").keyup(function () {
      var charCount = $(this).val().length;
      $("#newsCounter").text(1000 - charCount);
    });
  
    $("#replyInput").keyup(function () {
      var charCount = $(this).val().length;
      $("#replyCounter").text(1000 - charCount);
    });
  
    $("input, textarea").attr("autocomplete", "off");
  
    
  
    $("#replyNews").click(function () {
      // Ajax call to register a reply to any given News object.
      $.ajax({
        url: '/news/post-comment/',
        data: $("#replyNewsForm").serialize(),
        type: 'POST',
        cache: false,
        success: function (data) {
          $("#replyInput").val("");
          $("#newsThreadModal").modal("hide");
        },
        error: function (data) {
          alert(data.responseText);
        },
      });
    });
  
    $("ul.stream").on("click", ".like", function () {
      // Ajax call on action on like button.
      console.log("clicked like");
      var li = $(this).closest("li");
      var internship = $(li).attr("internship-id");
      if (internship !== undefined){
        payload = {
            'internship': internship,
            'csrf_token': csrftoken
          }
          $.ajax({
            url: '/internship/like/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
              console.log('IN SUCCESS FUNCTION FOR LIKE!');
              $(".like .like-count", li).text(data.likes);
              if ($(".like .heart", li).hasClass("fa fa-heart")) {
                console.log('IN IF FOR LIKE!');
                $(".like .heart", li).removeClass("fa fa-heart");
                $(".like .heart", li).addClass("fa fa-heart-o");
              } else {
                console.log('IN ELSE FOR LIKE!');
                $(".like .heart", li).removeClass("fa fa-heart-o");
                $(".like .heart", li).addClass("fa fa-heart");
              }
            }
          });
      }
      else{
        var research = $(li).attr("research-id");
        if (research !== undefined){
          var li = $(this).closest("li");
          var research = $(li).attr("research-id");
          payload = {
            'research': research,
            'csrf_token': csrftoken
          }
          $.ajax({
            url: '/research/like/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
              console.log('IN SUCCESS FUNCTION FOR LIKE!');
              $(".like .like-count", li).text(data.likes);
              if ($(".like .heart", li).hasClass("fa fa-heart")) {
                console.log('IN IF FOR LIKE!');
                $(".like .heart", li).removeClass("fa fa-heart");
                $(".like .heart", li).addClass("fa fa-heart-o");
              } else {
                console.log('IN ELSE FOR LIKE!');
                $(".like .heart", li).removeClass("fa fa-heart-o");
                $(".like .heart", li).addClass("fa fa-heart");
              }
            }
          });
        }
      }
      return false;
    });
  
    $("ul.stream").on("click", ".attended", function () {
      // Ajax call on action on attended button.
      var li = $(this).closest("li");
      var news = $(li).attr("news-id");
      payload = {
        'news': news,
        
      }
      $.ajax({
        url: '/news/attended/',
        data: payload,
        type: 'POST',
        cache: false,
        success: function (data) {
          $(".attended .attended-count", li).text(data.attendeds);
          if ($(".attended .check", li).hasClass("fa fa-check-square")) {
            $(".attended  .check", li).removeClass("fa fa-check-square");
            $(".attended  .check", li).addClass("fa fa-check-square-o");
          } else {
            $(".attended  .check", li).removeClass("fa fa-check-square-o");
            $(".attended  .check", li).addClass("fa fa-check-square");
          }
        },
        error: function(data){
          alert('error');
        }
      });
      return false;
    });
  
    $("ul.stream").on("click", ".comment", function () {
      // Ajax call to request a given News object detail and thread, and to
      // show it in a modal.
      var post = $(this).closest(".card");
      var news = $(post).closest("li").attr("news-id");
      $("#newsThreadModal").modal("show");
      $.ajax({
        url: '/news/get-thread/',
        data: { 'news': news },
        cache: false,
        beforeSend: function () {
          $("#threadContent").html("<li class='loadcomment'><img src='/static/img/loading.gif'></li>");
        },
        success: function (data) {
          $("input[name=parent]").val(data.uuid)
          $("#newsContent").html(data.news);
          $("#threadContent").html(data.thread);
        }
      });
      return false;
    });
  });
  
  
  /* Example query for the GraphQL endpoint.
  
    query{
      news(uuidId: "--insert here the required uuid_id value for the lookup"){
        uuidId
        content
        timestamp
        countThread
        countLikers
        user {
        name
        picture
        }
        liked {
        name
        }
        thread{
        content
        }
      }
      paginatedNews(page: 1){
        page
        pages
        hasNext
        hasPrev
        objects {
        uuidId
        content
        timestamp
        countThread
        countLikers
        user {
          name
          picture
        }
        liked {
          name
        }
        thread{
          content
        }
        }
      }
      }
   */
  