let bot_name = "2Nimbus Chatbot";
// Show the welcome message from AI
let html_welcome_msg = `
<a href="#" class="list-group-item list-group-item-action d-flex gap-3 py-3">
<img src="/static/images/boticon.png" alt="twbs" width="32" height="32" class="rounded-circle flex-shrink-0">
<div class="d-flex gap-2 w-100 justify-content-between">
    <div>
    <p class="mb-0 opacity-75">Hello! I am ${bot_name}. How may I help you?</p>
    </div>
</div>
</a>
`;
$("#list-group").append(html_welcome_msg);
// Get the input field
var input = document.getElementById("chat-input");

// Execute a function when the user presses a key on the keyboard
input.addEventListener("keypress", function (event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("gpt-button").click();
    }
});

$("#gpt-button").click(function () {
    var question = $("#chat-input").val();
    let html_mymsg = '';
    html_mymsg += `
  <a href="#" class="list-group-item list-group-item-action d-flex gap-3 py-3">
    <img src="/static/images/logo_sq.png" alt="twbs" width="32" height="32" class="rounded-circle flex-shrink-0">
    <div class="d-flex gap-2 w-100 justify-content-between">
      <div>
        <p class="mb-0 opacity-75">${question}</p>
      </div>
    </div>
  </a>
  `;
    $("#chat-input").val('');
    $("#list-group").append(html_mymsg);

    //AJAX CALL TO SERVER
    $.ajax({
        type: "POST",
        url: "", // Set this url to the url which contains the UI for testing!
        // NOTE: for POST requests, you cannot set a url chain where earlier parts does not exist e.g. <url>/nimbus/ui/ is invalid if <url>/nimbus has no view!!
        data: { 'questi0n': question },
        success: function (data) {
            let gpt_data = '';
            gpt_data += `
              <a href="#" class="list-group-item list-group-item-action d-flex gap-3 py-3">
                <img src="/static/images/boticon.png" alt="twbs" width="32" height="32" class="rounded-circle flex-shrink-0">
                <div class="d-flex gap-2 w-100 justify-content-between">
                  <div>
                    <p class="mb-0 opacity-75">${data.answer}</p>
                  </div>
                </div>
              </a>
        `;
            $("#list-group").append(gpt_data);
        }
    });
});