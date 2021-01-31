const regexp = new RegExp(
  /playerCaptionsTracklistRenderer.*?(youtube.com\/api\/timedtext.*?)"/
);

setInterval(() => {
  let url = regexp.exec(document.body.innerHTML)[1].replace(/\\u0026/g, '&');
  url = url.replace(/,/g, '%2C');
  url = url.replace(/\&kind=asr/, '');
  url = "https://www." + url + "&name=CC%20(English)&fmt=json3&xorb=2&xobt=3&xovt=3";
  chrome.runtime.sendMessage({ url: url });
}, 1000);
