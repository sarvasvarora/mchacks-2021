console.log("script is working");

window.url = "hihihihi";
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log(message);
  if (message.url) {
    window.url = message.url;
  }
});
