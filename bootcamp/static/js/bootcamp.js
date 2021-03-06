/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');

/* Notifications JS basic client */
$(function () {
    let emptyMessage = 'data-empty="true"';

    function checkNotifications() {
        $.ajax({
            url: '/notifications/latest-notifications/',
            cache: false,
            success: function (data) {
                if (!data.includes(emptyMessage)) {
                    $("#notifications").addClass("btn-danger");
                }
            },
        });
    };

    function update_social_activity (id_value) {
        let newsToUpdate = $("[news-id=" + id_value + "]");
        payload = {
            'id_value': id_value,
        };
        $.ajax({
            url: '/news/update-interactions/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".like-count", newsToUpdate).text(data.likes);
                $(".attended-count", newsToUpdate).text(data.attendeds);
                $(".comment-count", newsToUpdate).text(data.comments);
            },
        });
    };

    function update_social_activity_research (id_value) {
        let newsToUpdate = $("[research-id=" + id_value + "]");
        payload = {
            'id_value': id_value,
        };
        $.ajax({
            url: '/research/update-interactions/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".like-count", newsToUpdate).text(data.likes);
                $(".attended-count", newsToUpdate).text(data.attendeds);
                $(".comment-count", newsToUpdate).text(data.comments);
            },
        });
    };

    function update_social_activity_internship (id_value) {
        let newsToUpdate = $("[internship-id=" + id_value + "]");
        payload = {
            'id_value': id_value,
        };
        $.ajax({
            url: '/internship/update-interactions/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".like-count", newsToUpdate).text(data.likes);
                $(".attended-count", newsToUpdate).text(data.attendeds);
                $(".comment-count", newsToUpdate).text(data.comments);
            },
        });
    };

    function update_social_activity_community (id_value) {
        let newsToUpdate = $("[community-id=" + id_value + "]");
        payload = {
            'id_value': id_value,
        };
        $.ajax({
            url: '/community/update-interactions/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".like-count", newsToUpdate).text(data.likes);
                $(".attended-count", newsToUpdate).text(data.attendeds);
                $(".comment-count", newsToUpdate).text(data.comments);
            },
        });
    };

    checkNotifications();

    $('#notifications').popover({
        html: true,
        trigger: 'manual',
        container: "body" ,
        placement: "bottom",
    });

    $("#notifications").click(function () {
        if ($(".popover").is(":visible")) {
            $("#notifications").popover('hide');
            checkNotifications();
        }
        else {
            $("#notifications").popover('dispose');
            $.ajax({
                url: '/notifications/latest-notifications/',
                cache: false,
                success: function (data) {
                    console.log(data);
                    $("#notifications").popover({
                        html: true,
                        trigger: 'focus',
                        container: "body" ,
                        placement: "bottom",
                        content: data,
                    });
                    $("#notifications").popover('show');
                    $("#notifications").removeClass("btn-danger")
                },
            });
        }
        return false;
    });

    // Code block to manage WebSocket connections
    // Try to correctly decide between ws:// and wss://
    let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    let ws_path = ws_scheme + '://' + window.location.host + "/notifications/";
    let webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    // Helpful debugging
    webSocket.socket.onopen = function () {
        console.log("Connected to " + ws_path);
    };

    webSocket.socket.onclose = function () {
        console.error("Disconnected from " + ws_path);
    };

    // Listen the WebSocket bridge created throug django-channels library.
    webSocket.listen(function(event) {
        switch (event.key) {
            case "notification":
                $("#notifications").addClass("btn-danger");
                break;

            case "social_update":
                //$("#notifications").addClass("btn-danger");
                console.log("actor_name" + event.actor_name + "currentUser" + currentUser);
                if (event.actor_name !== currentUser){
                    update_social_activity(event.id_value);
                }
                console.log("Skipped the if statement");
                break;
            
            case "social_update_research":
                //$("#notifications").addClass("btn-danger");
                console.log("actor_name" + event.actor_name + "currentUser" + currentUser);
                if (event.actor_name !== currentUser){
                    console.log("In the if statement");
                    update_social_activity_research(event.id_value);
                }
                console.log("Past the if statement");
                break;

            case "social_update_internship":
                //$("#notifications").addClass("btn-danger");
                console.log("actor_name" + event.actor_name + "currentUser" + currentUser);
                if (event.actor_name !== currentUser){
                    console.log("In the if statement");
                    update_social_activity_internship(event.id_value);
                }
                console.log("Past the if statement");
                break;
            
            case "social_update_community":
                //$("#notifications").addClass("btn-danger");
                console.log("actor_name" + event.actor_name + "currentUser" + currentUser);
                if (event.actor_name !== currentUser){
                    console.log("In the if statement");
                    update_social_activity_community(event.id_value);
                }
                console.log("Past the if statement");
                break;

            case "additional_news":
                if (event.actor_name !== currentUser) {
                    $(".stream-update").show();
                }
                break;
            
            case "additional_research":
                if (event.actor_name !== currentUser) {
                    $(".stream-update").show();
                }
                break;
            
            case "additional_internship":
                if (event.actor_name !== currentUser) {
                    $(".stream-update").show();
                }
                break;
            
            case "additional_community":
                if (event.actor_name !== currentUser) {
                    $(".stream-update").show();
                }
                break;

            default:
                console.log('error: ', event);
                break;
        };
    });
});
