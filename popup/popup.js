document.getElementById("other").style.display = "none";
document.getElementById("summary").style.display = "none";
const bgpage = chrome.extension.getBackgroundPage();

chrome.tabs.getSelected(null, function (tab) {
  myFunction(tab.url);
});

function myFunction(tablink) {
  console.log(tablink);
  if (!tablink.includes("youtube")) {
    document.getElementById("prompt").style.display = "none";
    document.getElementById("other").style.display = "block";
  }
}

// prettier-ignore
// let url = false;
// const response = {};

const showInfo = (url) => {
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json; charset=UTF-8");

  var raw = JSON.stringify({url : url});
  console.log(raw);

  var requestOptions = {
    method: 'POST',
    // mode: 'no-cors',
    headers: myHeaders,
    body: raw,
    redirect: 'follow',
  };
  fetch("https://northamerica-northeast1-mchacks-303315.cloudfunctions.net/summary", requestOptions)
    .then((response) => {
      console.log(response);
      return response.json()
    })
    .then(res => {
      console.log(res);
      document.getElementById("sumtext").innerText = res.summary;
      document.getElementById("kw").innerText = "keyword";
      document.getElementById("key").innerText = res.keywords.toString();
    })
    .catch(error => console.log('error', error));
};

document.getElementById("btn").addEventListener("click", () => {
  document.getElementById("prompt").style.display = "none";
  document.getElementById("summary").style.display = "block";
  let url = bgpage.url;
  console.log(url);
  if (url) {
    showInfo(url);
  } else {
    document.getElementById("sumtext").innerText = "No transcription found";
  }
});
