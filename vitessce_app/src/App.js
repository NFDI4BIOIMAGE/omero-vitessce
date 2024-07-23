import React from 'react';
import { Vitessce } from 'vitessce';

export default function App() {
	// Use the useParams hook to get the "Config" parameter from the URL
	var params = new URLSearchParams(window.location.search)
	const viewConfig = params.get("config")

	function fetchData(url) {
	   const request = new XMLHttpRequest();	
	   request.open('GET', url, false);
	   request.send()	  
	   return JSON.parse(request.responseText) 
	}
	const fetchedConfig = fetchData(viewConfig);
	console.log(fetchedConfig)
	
	return (
		<Vitessce
			config={fetchedConfig} // Use the parsed viewConfig from the URL
			theme="dark"
		/>
	);
}
	
