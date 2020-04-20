function getCurrentTabUrl(callback) {
    var queryInfo = {
      active: true,
      currentWindow: true
    };

    chrome.tabs.query(queryInfo, function(tabs) {
      var tab = tabs[0];
      var url = tab.url;
      // callback("http://34.212.202.13:8000/?u="+url); // EC2
      callback("http://127.0.0.1:8000/?u="+url); // Localhost
    });
  }

  function renderURL(statusText) {
    document.getElementById('urlName').textContent = statusText;
    document.getElementById('foo').innerHTML = '<iframe src="' + statusText + '" width="100%" height="100%" frameborder="0"></iframe>';
  }

  document.addEventListener('DOMContentLoaded', function() {
    getCurrentTabUrl(function(url) {
      renderURL(url);
    });
  });