function initCheckAll() {
  $("#checkAll").on("change", function () {
    $(".table-check .form-check-input").prop(
      "checked",
      $(this).prop("checked")
    );
  }),
    $(".table-check .form-check-input").change(function () {
      $(".table-check .form-check-input:checked").length ==
      $(".table-check .form-check-input").length
        ? $("#checkAll").prop("checked", !0)
        : $("#checkAll").prop("checked", !1);
    });
}
function checkAll(e) {
  var t = document.getElementsByTagName("input");
  if (e.checked)
    for (var c = 0; c < t.length; c++)
      "checkbox" == t[c].type && (t[c].checked = !0);
  else
    for (c = 0; c < t.length; c++)
      "checkbox" == t[c].type && (t[c].checked = !1);
}
!(function (c) {
  "use strict";
  var e,
    t = localStorage.getItem("language"),
    n = "en";
  function a(e) {
    document.getElementById("header-lang-img") &&
      ("en" == e
        ? (document.getElementById("header-lang-img").src =
            "../../static/images/flags/us.jpg")
        : "sp" == e
        ? (document.getElementById("header-lang-img").src =
            "../../static/images/flags/spain.jpg")
        : "gr" == e
        ? (document.getElementById("header-lang-img").src =
            "../../static/images/flags/germany.jpg")
        : "it" == e
        ? (document.getElementById("header-lang-img").src =
            "../../static/images/flags/italy.jpg")
        : "ru" == e &&
          (document.getElementById("header-lang-img").src =
            "../../static/images/flags/russia.jpg"),
      localStorage.setItem("language", e),
      "null" == (t = localStorage.getItem("language")) && a(n),
      c.getJSON("../../static/lang/" + t + ".json", function (e) {
        c("html").attr("lang", t),
          c.each(e, function (e, t) {
            "head" === e && c(document).attr("title", t.title),
              c("[key='" + e + "']").text(t);
          });
      }));
  }
  function s() {
    for (
      var e = document
          .getElementById("topnav-menu-content")
          .getElementsByTagName("a"),
        t = 0,
        c = e.length;
      t < c;
      t++
    )
      "nav-item dropdown active" === e[t].parentElement.getAttribute("class") &&
        (e[t].parentElement.classList.remove("active"),
        null !== e[t].nextElementSibling &&
          e[t].nextElementSibling.classList.remove("show"));
  }
  function l(e) {
    1 == c("#light-mode-switch").prop("checked") && "light-mode-switch" === e
      ? (c("html").removeAttr("dir"),
        c("#dark-mode-switch").prop("checked", !1),
        c("#rtl-mode-switch").prop("checked", !1),
        c("#dark-rtl-mode-switch").prop("checked", !1),
        c("#bootstrap-style").attr(
          "href",
          "../../static/css/bootstrap.min.css"
        ),
        c("#app-style").attr("href", "../../static/css/app.min.css"),
        sessionStorage.setItem("is_visited", "light-mode-switch"))
      : 1 == c("#dark-mode-switch").prop("checked") && "dark-mode-switch" === e
      ? (c("html").removeAttr("dir"),
        c("#light-mode-switch").prop("checked", !1),
        c("#rtl-mode-switch").prop("checked", !1),
        c("#dark-rtl-mode-switch").prop("checked", !1),
        c("#bootstrap-style").attr(
          "href",
          "../../static/css/bootstrap-dark.min.css"
        ),
        c("#app-style").attr("href", "../../static/css/app-dark.min.css"),
        sessionStorage.setItem("is_visited", "dark-mode-switch"))
      : 1 == c("#rtl-mode-switch").prop("checked") && "rtl-mode-switch" === e
      ? (c("#light-mode-switch").prop("checked", !1),
        c("#dark-mode-switch").prop("checked", !1),
        c("#dark-rtl-mode-switch").prop("checked", !1),
        c("#bootstrap-style").attr(
          "href",
          "../../static/css/bootstrap-rtl.min.css"
        ),
        c("#app-style").attr("href", "../../static/css/app-rtl.min.css"),
        c("html").attr("dir", "rtl"),
        sessionStorage.setItem("is_visited", "rtl-mode-switch"))
      : 1 == c("#dark-rtl-mode-switch").prop("checked") &&
        "dark-rtl-mode-switch" === e &&
        (c("#light-mode-switch").prop("checked", !1),
        c("#rtl-mode-switch").prop("checked", !1),
        c("#dark-mode-switch").prop("checked", !1),
        c("#bootstrap-style").attr(
          "href",
          "../../static/css/bootstrap-dark-rtl.min.css"
        ),
        c("#app-style").attr("href", "../../static/css/app-dark-rtl.min.css"),
        c("html").attr("dir", "rtl"),
        sessionStorage.setItem("is_visited", "dark-rtl-mode-switch"));
  }
  function r() {
    document.webkitIsFullScreen ||
      document.mozFullScreen ||
      document.msFullscreenElement ||
      (console.log("pressed"), c("body").removeClass("fullscreen-enable"));
  }
  c("#side-menu").metisMenu(),
    c("#vertical-menu-btn").on("click", function (e) {
      e.preventDefault(),
        c("body").toggleClass("sidebar-enable"),
        992 <= c(window).width()
          ? c("body").toggleClass("vertical-collpsed")
          : c("body").removeClass("vertical-collpsed");
    }),
    c("#sidebar-menu a").each(function () {
      var e = window.location.href.split(/[?#]/)[0];
      this.href == e &&
        (c(this).addClass("active"),
        c(this).parent().addClass("mm-active"),
        c(this).parent().parent().addClass("mm-show"),
        c(this).parent().parent().prev().addClass("mm-active"),
        c(this).parent().parent().parent().addClass("mm-active"),
        c(this).parent().parent().parent().parent().addClass("mm-show"),
        c(this)
          .parent()
          .parent()
          .parent()
          .parent()
          .parent()
          .addClass("mm-active"));
    }),
    c(document).ready(function () {
      var e;
      0 < c("#sidebar-menu").length &&
        0 < c("#sidebar-menu .mm-active .active").length &&
        300 < (e = c("#sidebar-menu .mm-active .active").offset().top) &&
        ((e -= 300),
        c(".vertical-menu .simplebar-content-wrapper").animate(
          { scrollTop: e },
          "slow"
        ));
    }),
    c(".navbar-nav a").each(function () {
      var e = window.location.href.split(/[?#]/)[0];
      this.href == e &&
        (c(this).addClass("active"),
        c(this).parent().addClass("active"),
        c(this).parent().parent().addClass("active"),
        c(this).parent().parent().parent().addClass("active"),
        c(this).parent().parent().parent().parent().addClass("active"),
        c(this).parent().parent().parent().parent().parent().addClass("active"),
        c(this)
          .parent()
          .parent()
          .parent()
          .parent()
          .parent()
          .parent()
          .addClass("active"));
    }),
    c('[data-bs-toggle="fullscreen"]').on("click", function (e) {
      e.preventDefault(),
        c("body").toggleClass("fullscreen-enable"),
        document.fullscreenElement ||
        document.mozFullScreenElement ||
        document.webkitFullscreenElement
          ? document.cancelFullScreen
            ? document.cancelFullScreen()
            : document.mozCancelFullScreen
            ? document.mozCancelFullScreen()
            : document.webkitCancelFullScreen &&
              document.webkitCancelFullScreen()
          : document.documentElement.requestFullscreen
          ? document.documentElement.requestFullscreen()
          : document.documentElement.mozRequestFullScreen
          ? document.documentElement.mozRequestFullScreen()
          : document.documentElement.webkitRequestFullscreen &&
            document.documentElement.webkitRequestFullscreen(
              Element.ALLOW_KEYBOARD_INPUT
            );
    }),
    document.addEventListener("fullscreenchange", r),
    document.addEventListener("webkitfullscreenchange", r),
    document.addEventListener("mozfullscreenchange", r),
    c(".right-bar-toggle").on("click", function (e) {
      c("body").toggleClass("right-bar-enabled");
    }),
    c(document).on("click", "body", function (e) {
      0 < c(e.target).closest(".right-bar-toggle, .right-bar").length ||
        c("body").removeClass("right-bar-enabled");
    }),
    (function () {
      if (document.getElementById("topnav-menu-content")) {
        for (
          var e = document
              .getElementById("topnav-menu-content")
              .getElementsByTagName("a"),
            t = 0,
            c = e.length;
          t < c;
          t++
        )
          e[t].onclick = function (e) {
            "#" === e.target.getAttribute("href") &&
              (e.target.parentElement.classList.toggle("active"),
              e.target.nextElementSibling.classList.toggle("show"));
          };
        window.addEventListener("resize", s);
      }
    })(),
    [].slice
      .call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
      .map(function (e) {
        return new bootstrap.Tooltip(e);
      }),
    [].slice
      .call(document.querySelectorAll('[data-bs-toggle="popover"]'))
      .map(function (e) {
        return new bootstrap.Popover(e);
      }),
    [].slice.call(document.querySelectorAll(".offcanvas")).map(function (e) {
      return new bootstrap.Offcanvas(e);
    }),
    window.sessionStorage &&
      ((e = sessionStorage.getItem("is_visited")) ||
        ((e = "light-mode-switch"), sessionStorage.setItem("is_visited", e)),
      c(".right-bar input:checkbox").prop("checked", !1),
      c("#" + e).prop("checked", !0),
      l(e)),
    c(
      "#light-mode-switch, #dark-mode-switch, #rtl-mode-switch, #dark-rtl-mode-switch"
    ).on("change", function (e) {
      l(e.target.id);
    }),
    c("#password-addon").on("click", function () {
      0 < c(this).siblings("input").length &&
        ("password" == c(this).siblings("input").attr("type")
          ? c(this).siblings("input").attr("type", "input")
          : c(this).siblings("input").attr("type", "password"));
    }),
    null != t && t !== n && a(t),
    c(".language").on("click", function (e) {
      a(c(this).attr("data-lang"));
    }),
    c(window).on("load", function () {
      c("#status").fadeOut(), c("#preloader").delay(350).fadeOut("slow");
    }),
    Waves.init(),
    c("#checkAll").on("change", function () {
      c(".table-check .form-check-input").prop(
        "checked",
        c(this).prop("checked")
      );
    }),
    c(".table-check .form-check-input").change(function () {
      c(".table-check .form-check-input:checked").length ==
      c(".table-check .form-check-input").length
        ? c("#checkAll").prop("checked", !0)
        : c("#checkAll").prop("checked", !1);
    });
})(jQuery);

function deleteTV(tvName) {
    if (confirm("Are you sure you want to delete " + tvName + "?")) {
        $.ajax({
            url: `/delete-tv/${tvName}/`,
            type: 'DELETE',
            success: function(result) {
                alert(tvName + ' deleted successfully.');
                location.reload();  // Optionally reload the page to refresh the list
            },
            error: function(xhr, status, error) {
                alert('Failed to delete ' + tvName + '.');
            }
        });
    }
}



function deleteVideo(videoId) {
    if (confirm("Are you sure you want to delete this video?")) {
        $.ajax({
            url: `/delete-video/${videoId}/`,
            type: 'DELETE',
            success: function(response) {
                alert('Video deleted successfully.');
                location.reload();  // Refresh the page to update the list
            },
            error: function(error) {
                alert('Error deleting the video.');
            }
        });
    }
}

window.onload = function() {
    // Call the filter function with 'year' as the default filter
    filterVideos('year');
};

function viewVideo(videoId) {
    // Construct the video URL using the video ID
    const videoUrl = `/videos/${videoId}`;
    
    // Redirect to the video URL to stream the video
    window.location.href = videoUrl;
}

function filterVideos(filter) {
    // Send an AJAX request to fetch filtered videos based on the selected filter
    $.ajax({
        url: `/filter-videos/${filter}/`,  // Backend URL to filter videos
        type: 'GET',
        success: function(response) {
            // Clear the current table body
            const videoTableBody = document.getElementById('videoTableBody');
            videoTableBody.innerHTML = '';

            // Iterate through the response and populate the table with filtered videos
            response.videos.forEach(function(video) {
                const row = `
                    <tr>
                        <td>${video.title}</td>
                        <td>${new Date(video.uploaded_at).toLocaleString()}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" onclick="viewVideo('${video.id}')">View</button>
                            <button class="btn btn-danger btn-sm" onclick="deleteVideo('${video.id}')">Delete</button>
                        </td>
                    </tr>
                `;
                videoTableBody.innerHTML += row;
            });
        },
        error: function(error) {
            alert('Error fetching filtered videos.');
        }
    });
}
// Get CSRF token from cookies (if using CSRF)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

Dropzone.options.videoUploadDropzone = {
    paramName: "file", // The file being uploaded
    maxFilesize: 2000, // Maximum file size in MB
    acceptedFiles: "video/*", // Accept only video files
    autoProcessQueue: false, // Manually trigger the upload
    init: function() {
        var myDropzone = this;

        // Send video title and CSRF token along with the file
        this.on("sending", function(file, xhr, formData) {
            var videoTitle = document.getElementById("video-title").value;  // Get the title from input field
            formData.append("title", videoTitle);  // Add the title to the form data
            formData.append("csrfmiddlewaretoken", csrftoken);  // Add the CSRF token
        });

        // Trigger upload when "Send Videos" button is clicked
        document.querySelector(".btn-primary").addEventListener("click", function() {
            myDropzone.processQueue(); // Manually trigger the queue
        });
    }
};


function submitVideoUpload() {
    var myDropzone = Dropzone.forElement("#video-upload-dropzone");
    myDropzone.processQueue(); // Manually process the queue
}