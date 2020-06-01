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
    $('#internshipFormModal').on('shown.bs.modal', function () {
      $('#internshipInput').trigger('focus')
    });
  
    $('#internshipThreadModal').on('shown.bs.modal', function () {
      $('#replyInput').trigger('focus')
    });
  
    // Counts textarea characters to provide data to user.
    $("#internshipInput").keyup(function () {
      var charCount = $(this).val().length;
      $("#internshipCounter").text(1000 - charCount);
    });
  
    $("#replyInput").keyup(function () {
      var charCount = $(this).val().length;
      $("#replyCounter").text(280 - charCount);
    });
  
    $("input, textarea").attr("autocomplete", "off");
  
    $("#postInternship").click(function () {
      // Ajax call after pushing button, to register a Internship object.
      $.ajax({
        url: '/internship/post-internship/',
        data: $("#postInternshipForm").serialize(),
        type: 'POST',
        cache: false,
        success: function (data) {
          $("ul.stream").prepend(data);
          $("#internshipInput").val("");
          // $("#internshipInputDescription").val("");
          // $("#internshipInputLink").val("");
          $("#internshipFormModal").modal("hide");
          $('#postInternshipForm').get(0).reset();
          hide_stream_update();
        },
        error: function (data) {
          alert(data.responseText);
        },
      });
    });
  
    $("#replyInternship").click(function () {
      // Ajax call to register a reply to any given Internship object.
      $.ajax({
        url: '/internship/post-comment/',
        data: $("#replyInternshipForm").serialize(),
        type: 'POST',
        cache: false,
        success: function (data) {
          $(".comment .comment-count").text(data.comments)
          $("#replyInput").val("");
          $("#internshipThreadModal").modal("hide");
        },
        error: function (data) {
          alert(data.responseText);
        },
      });
    });
  
    $("ul.stream").on("click", ".like", function () {
      // Ajax call on action on like button.
      var li = $(this).closest("li");
      var internship = $(li).attr("internship-id");
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
      return false;
    });
  
    $("ul.stream").on("click", ".attended", function () {
      // Ajax call on action on attended button.
      var li = $(this).closest("li");
      var internship = $(li).attr("internship-id");
      payload = {
        'internship': internship,
        
      }
      $.ajax({
        url: '/internship/attended/',
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
      // Ajax call to request a given Internship object detail and thread, and to
      // show it in a modal.
      var post = $(this).closest(".card");
      var internship = $(post).closest("li").attr("internship-id");
      $("#internshipThreadModal").modal("show");
      $.ajax({
        url: '/internship/get-thread/',
        data: { 'internship': internship },
        cache: false,
        beforeSend: function () {
          $("#threadContent").html("<li class='loadcomment'><img src='/static/img/loading.gif'></li>");
        },
        success: function (data) {
          $("input[name=parent]").val(data.uuid)
          $("#internshipContent").html(data.internship);
          $("#threadContent").html(data.thread);
        },
        error: function(xhr, status, error) {
          var err = eval("(" + xhr.responseText + ")");
          console.log(err.Message);
        }
      });
      return false;
    });
  });
  
  
  /* Example query for the GraphQL endpoint.
  
    query{
      internship(uuidId: "--insert here the required uuid_id value for the lookup"){
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
      paginatedInternship(page: 1){
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
    