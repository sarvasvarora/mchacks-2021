sbdocument.getElementById("other").style.display = "none";
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

const getInfo = (url) => {
  const response = {};
  // "https://www.youtube.com/api/timedtext?v=vM-2O-uKBNQ&asr_langs=de%2Cen%2Ces%2Cfr%2Cit%2Cja%2Cko%2Cnl%2Cpt%2Cru&caps=asr&exp=xftt&xorp=true&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1612109209&sparams=ip%2Cipbits%2Cexpire%2Cv%2Casr_langs%2Ccaps%2Cexp%2Cxorp%2Cxoaf&signature=52E02FA0668DF9B92BBD4ED4E27D5AD646C30006.E770E85FD7A4347771A85A3EF80AC0D03EBD51EB&key=yt8&lang=en&name=CC%20(English)&fmt=json3&xorb=2&xobt=3&xovt=3 "

  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({"url": url});

  var requestOptions = {
    method: 'POST',
    mode: 'no-cors',
    headers: myHeaders,
    body: raw,
    redirect: 'follow',
  };
  fetch("https://northamerica-northeast1-mchacks-303315.cloudfunctions.net/summary", requestOptions)
    .then(response => response.json())
    .then(result => {
      response = result;
      console.log(result)
    })
    .catch(error => console.log('error', error));

  return response;
};

document.getElementById("btn").onclick = function myFunction() {
  document.getElementById("prompt").style.display = "none";
  document.getElementById("summary").style.display = "block";
  let url = bgpage.url;
  console.log(url);
  if (url) {
    const res = getInfo(url);
    document.getElementById("sumtext").innerText =
      res.summary +
      '\n <span class="bold>Keywords</span>' +
      res.keywords.toString;
    console.log(res);
  } else {
    document.getElementById("sumtext").innerText = "No transcription found";
  }
};
