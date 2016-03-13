function sleep(millis)
 {
  var date = new Date();
  var curDate = null;
  do { curDate = new Date(); }
  while(curDate-date < millis);
}
chrome.tabs.query({"currentWindow":true}, function(tabs_array){
var i;
for(i=0;i<tabs_array.length;i++)
{
var url = tabs_array[i].url;
var prevurl = url;
if(url.indexOf("facebook")==-1)
{
continue;
}
if(url.indexOf("src=")>-1)
{
url = url.slice(url.indexOf("src=")+4);
url = url.slice(0,url.indexOf("&"));
url = decodeURIComponent(url);
}
else
{
url = ""
}
if(url.length>0)
{
chrome.tabs.update(tabs_array[i].id,{"url":url});
document.write("a");
chrome.tabs.onUpdated.addListener(function(i,options,tab){
if(tab.title.indexOf("Error")>-1)
{
document.write("yo");
chrome.tabs.executeScript(tab.id,{"code":"window.history.back();"});
return
}
if(tab.url.indexOf("facebook")>-1)
{
url = tab.url;
if(url.indexOf("fbid")==-1)
{
url = url.split("/")[6];
}
else
{
url = url.slice(url.indexOf("fbid=")+5);
url = url.slice(0,url.indexOf("&"));
}
chrome.tabs.executeScript(tab.id,{"code":"var xhttp = new XMLHttpRequest();xhttp.onreadystatechange=function(){if(xhttp.readyState==4&&xhttp.status==200) window.location=xhttp.responseURL.slice(0,-5);};xhttp.open('GET','https://www.facebook.com/photo/download/?fbid="+url+"',true);xhttp.send();"});

}


});
}

else
{
if(tabs_array[i].url.indexOf("facebook")>-1)
{
url = tabs_array[i].url;
if(url.indexOf("fbid")==-1)
{
url = url.split("/")[6];
document.write(url);
}
else
{
url = url.slice(url.indexOf("fbid=")+5);
url = url.slice(0,url.indexOf("&"));
}
chrome.tabs.executeScript(tabs_array[i].id,{"code":"var xhttp = new XMLHttpRequest();xhttp.onreadystatechange=function(){if(xhttp.readyState==4&&xhttp.status==200) window.location=xhttp.responseURL.slice(0,-5);};xhttp.open('GET','https://www.facebook.com/photo/download/?fbid="+url+"',true);xhttp.send();"});

}
}
}
});