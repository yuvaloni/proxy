window.onload = register
function register()
{
document.getElementById("btn").addEventListener("click", changeState);
}
function listen_callback(items)
{
	document.write(items['yuval_proxy_listen']);
	if(!items['yuval_proxy_listen'] || items['yuval_proxy_listen']=='False' )
	{
		chrome.storage.local.set({'yuval_proxy_listen':'True'});
	}
	else if(items['yuval_proxy_listen']=='True')
	{
		chrome.storage.local.set({'yuval_proxy_listen':'False'});
	}
}
function changeState()
{
	var state = chrome.storage.local.get('yuval_proxy_listen',listen_callback);
}