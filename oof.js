const regexp = new RegExp(
  /playerCaptionsTracklistRenderer.*?(youtube.com\/api\/timedtext.*?)"/
);

setInterval(() => {
  const url = regexp.exec(document.body.innerHTML)[1];
  chrome.runtime.sendMessage({ url: url });
}, 1000);
