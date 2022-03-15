function createProductionStepTags(canvasId,productionStepName,stepSequence){
	var canvas = document.getElementById(canvasId);
	var context = canvas.getContext('2d');
	var centerX = canvas.width /8;
	var centerY = canvas.height / 2;
	var radius = canvas.height / 4;
  
	context.beginPath();
	context.rect(centerX-radius*2, centerY-radius, canvas.width - radius*5, radius*2);
	context.fillStyle = 'green';
	context.fill();
	context.lineWidth = 0;
	context.strokeStyle = '#003300';
	context.stroke();

	context.beginPath();
	context.arc(centerX-radius*2, centerY, radius, 0, 2 * Math.PI, false);
	context.fillStyle = 'green';
	context.fill();
	context.lineWidth = 0;
	context.strokeStyle = '#003300';
	context.stroke();


	context.beginPath();
	context.fillStyle = "black";
	context.font = "15px Georgia";	  
	context.fillText(stepSequence, centerX-radius*2.2, centerY+radius*0.25);
	context.fill();	
	context.stroke();
	context.beginPath();
	context.fillStyle = "black";
	context.font = "15px Georgia";	  
	context.fillText(productionStepName, centerX+2*radius, centerY+radius*0.25);
	context.fill();	
	context.stroke();
}
function getLog_MainService(){
	var output = document.getElementById('logParagraph_MainService');
	var httpGetRequest = new XMLHttpRequest();
	httpGetRequest.open('POST','/log');
	httpGetRequest.onload = () => {
		const logData = (httpGetRequest.responseText)
		document.getElementById("logParagraph_MainService").innerHTML = logData.replace(/\\n/g, "<br>");
	}
	httpGetRequest.send()
}

function getLog_BoringRequester(){
	var output = document.getElementById('logParagraph_BoringRequester');
	var httpGetRequest = new XMLHttpRequest();
	httpGetRequest.open('GET','/log/BoringRequester');
	httpGetRequest.onload = () => {
	const logData = (httpGetRequest.responseText)
	document.getElementById("logParagraph_BoringRequester").innerHTML = logData.replace(/\\n/g, "<br>");
	}
	httpGetRequest.send()
	}
function getLog_TransportRequester(){
	var output = document.getElementById('logParagraph_TransportRequester');
	var httpGetRequest = new XMLHttpRequest();
	httpGetRequest.open('GET','/log/TransportRequester');
	httpGetRequest.onload = () => {
	const logData = (httpGetRequest.responseText)
	document.getElementById("logParagraph_TransportRequester").innerHTML = logData.replace(/\\n/g, "<br>");
	}
	httpGetRequest.send()
	}
function getLog_HoningRequester(){
	var output = document.getElementById('logParagraph_HoningRequester');
	var httpGetRequest = new XMLHttpRequest();
	httpGetRequest.open('GET','/log/HoningRequester');
	httpGetRequest.onload = () => {
	const logData = (httpGetRequest.responseText)
	document.getElementById("logParagraph_HoningRequester").innerHTML = logData.replace(/\\n/g, "<br>");
	}
	httpGetRequest.send()
	}

function getLog_Register(){
	var output = document.getElementById('logParagraph_Register');
	var httpGetRequest = new XMLHttpRequest();
	httpGetRequest.open('GET','/log/Register');
	httpGetRequest.onload = () => {
	const logData = (httpGetRequest.responseText)
	document.getElementById("logParagraph_Register").innerHTML = logData.replace(/\\n/g, "<br>");
	}
	httpGetRequest.send()
}

function get_MessageData(messageID,conversationId){
	uri = encodeURI(messageID+"**"+conversationId);
	var output = document.getElementById('data_Content_modal');
	var httpGetRequest = new XMLHttpRequest();
	httpGetRequest.open('GET','/search/'+uri);
	document.getElementById("FrameTreeDiv").innerHTML = "";
	httpGetRequest.onload = () => {
		var data = (httpGetRequest.responseText)
		var data1 = data.replace(/\\n/g, "<br>");
		data = JSON.parse(data1);

		document.getElementById("data_Content_header").innerHTML = messageID;
		document.getElementById("FrameTreeDiv").appendChild( createResultFrameTree(data));
		setResultFrameTreeListner()
	}
httpGetRequest.send()
}
function setResultFrameTreeListner()
{
 	$('.FrameTreeDivClass .listElement').click(function(){
 	    $('.highlight').removeClass('highlight');
 		$(this).addClass('highlight');

 	});

 	var toggler = document.getElementsByClassName("rbox");
 	var i;
	console.log(toggler);
 	for (i = 0; i < toggler.length; i++) {
 	  toggler[i].addEventListener("click", function() {
 		  
 	    console.log(this.parentElement.querySelector(".rNested").classList.toggle("active"));
 	    this.classList.toggle("rcheck-box");
 	  });
 	}
}

//Submodel Tree creation

function createSubmodelTree(submodel,data)
{
 	var submodelUlNested = document.createElement('ul'); 
 	submodelUlNested.setAttribute("class","nested");
	var testURL = (processEachSubmodelElement(data[submodel]['data'],submodel,submodelUlNested));
	
	var submodelLI = document.createElement('li');
	submodelLI.appendChild(createSpanElement(submodel));
	submodelLI.appendChild(testURL);
 	
	var submodelUL = document.createElement('ul'); 
	submodelUL.setAttribute("id","submodelTree");
	submodelUL.appendChild(submodelLI);
 	
 	var t = document.getElementById(submodel+"TreeDiv");
	t.appendChild(submodelUL);
}
function processEachSubmodelElement(connectstatusDict,submodel,submodelUL)
{
	if ( typeof connectstatusDict === "object")
		{
			for (const [key, value] of Object.entries(connectstatusDict)) {
				if ( typeof value == "object")
					{
						objectUl1 = document.createElement('ul');
						objectUl1.setAttribute("class","nested");
						returnli = processEachSubmodelElement(value,submodel,objectUl1);
						objectli = document.createElement('li');
						objectli.append(createSpanElement(key));
						objectli.append(returnli);
						submodelUL.append(objectli);
					}
				else {
					text = document.createElement('li');
					text.setAttribute("class","listElement");
					text.setAttribute("onclick","showData('"+ value+"','"+key+"','"+submodel+"')");
					text.appendChild(createAPropertySPAN(key,value));
					submodelUL.append(text);
					
				}
			}
		}

	else {
		
	}
	return submodelUL;
}
function createSpanElement(spanText)
{
	span1 = document.createElement('span');
	span1.setAttribute("style","color:white;background-color:#6c8ebf;");
	span1.innerHTML = "Coll";
	
	span2 = document.createElement('span');
	span2.setAttribute("style","color:black;background-color:white;");
	span2.innerHTML = "&nbsp;&nbsp;"+spanText;
	
	
 	var textSpan = document.createElement('span');
 	textSpan.setAttribute("class","box");
 	textSpan.appendChild(span1);
	textSpan.appendChild(span2);
 	
 	return textSpan;
}
function createAPropertySPAN(key,value)
{
	span1 = document.createElement('span');
	span1.setAttribute("style","color:white;background-color:#6c8ebf;");
	span1.innerHTML = "Prop"
	span2 = document.createElement('span');
	span2.setAttribute("style","color:black;");
	if (isNaN(key))
	{
		span2.innerHTML = "&nbsp;&nbsp;"+key;
	}
	else {
		span2.innerHTML = "&nbsp;&nbsp;"+value;
	}
	
	span3 = document.createElement('span');
	span3.appendChild(span1);
	span3.appendChild(span2);
	return span3;
}
function modalSubmodelDataModifier(submodelName,submodelProperty)
{
	document.getElementById("submodelPropertyHeader").innerHTML = "Update " + submodelName + " property : " +  submodelProperty;
	document.getElementById("submodelNameInnerText").value = submodelName	
	document.getElementById("submodelPropertyInnerText").value = submodelProperty
}
function createImageInput(property,key,imageSrc)
{
	imageInput = document.createElement("input");
	imageInput.setAttribute("type","image");
	imageInput.setAttribute("style","height: 4vh");
	imageInput.setAttribute("onclick","modalSubmodelDataModifier('"+property+"','"+key+"')");
	imageInput.setAttribute("data-bs-toggle","modal");
	imageInput.setAttribute("data-bs-target","#propertyUpdate");
	imageInput.setAttribute("data-whatever","@mdo");
	imageInput.setAttribute("src","/static/images/"+imageSrc+".svg");
	imageInput.setAttribute("name","submit");
	
	return imageInput;
}
function createEditButton(property,key)
{
	inputImage = createImageInput(property,key,"edit");
	inputAImage = createImageInput(property,key,"edit1");
	
	var overlayDiv = document.createElement("div");
	overlayDiv.setAttribute("class","overlay");
	overlayDiv.appendChild(inputAImage);
	
	var imageCon = document.createElement("div");
	imageCon.setAttribute("class","imagecontainer");
	imageCon.appendChild(inputImage);
	imageCon.appendChild(overlayDiv);
	
	return imageCon;
}
function showData(value,key,submodel,elem) {
	var v = document.getElementById(submodel+"LeafValuep");
	v.innerHTML = value;
	var editButton = createEditButton(submodel,key);
	var submodelleafValueDiv = document.getElementById(submodel+"leafValueDiv");
	submodelleafValueDiv.innerHTML = '';
	submodelleafValueDiv.appendChild(editButton);	
}
//Search Result Tree creation

function processDirectionMessage(messages,conVId)
{
	messagesList = []
	for ( var i = 0; i < messages.length; i ++)
	{
		var aLink = document.createElement("a");	
		aLink.setAttribute("class","searchLink");
		aLink.setAttribute("href","#");
		aLink.setAttribute("style","text-decoration:none;color:black; cursor: pointer;");
		aLink.setAttribute("onclick","get_MessageData('"+ messages[i]+"','"+conVId+"')");
		aLink.setAttribute("data-bs-toggle","modal");
		aLink.setAttribute("data-bs-target","#framedataBox");
		aLink.setAttribute("data-whatever","@mdo");
		aLink.innerHTML = messages[i];
		var col = document.createElement("td");	
		col.appendChild(aLink);
		var row = document.createElement("tr");	
		row.appendChild(col);
		console.log(row);
		messagesList.push(row)
	}
	return messagesList;
}
function createTable(messages,conVId)
{
	var messagesList = processDirectionMessage(messages,conVId);
	var tbody= document.createElement("tbody");
	for ( var i = 0; i < messagesList.length; i ++)
	{
		tbody.appendChild(messagesList[i]);
	}
	var htmlTable = document.createElement("table");
	htmlTable.setAttribute("class","table");
	htmlTable.setAttribute("style","text-align: center;");
	htmlTable.appendChild(tbody);
	return htmlTable;
}
function createSearResultTree(data)
{	
	var resultList = data[Object.keys(data)[0]][0]
	var searchResultInbound = document.getElementById("searchResultInbound");
	searchResultInbound.append(createTable(resultList["inbound"],String(Object.keys(data)[0])));
	
	var searchResultInbound = document.getElementById("searchResultOutbound");
	searchResultInbound.append(createTable(resultList["outbound"],String(Object.keys(data)[0])));
}
// Result Frame Tree
function createResultFrameTree(data)
{
	console.log(data);
	var messageId = data["frame"]["messageId"];
	var conversationId = data["frame"]["conversationId"]
	var frameUlNested = document.createElement('ul'); 
 	frameUlNested.setAttribute("class","rNested");
	var testURL = processEachResultFrameElement(data,messageId,frameUlNested);

	var frameLI = document.createElement('li');
	frameLI.appendChild(createResultFrameSpanElement(conversationId));
	frameLI.appendChild(testURL);
 	
	var frameUL = document.createElement('ul'); 
	frameUL.setAttribute("id","resultTree");
	frameUL.appendChild(frameLI);

 	return frameUL;
}
function processEachResultFrameElement(data,coversationId,frameUL)
{
	console.log(data,coversationId,frameUL);
	if ( typeof data === "object")
	{
		for (const [key, value] of Object.entries(data)) {
			if ( typeof value == "object")
				{
					objectUl1 = document.createElement('ul');
					objectUl1.setAttribute("class","rNested");
					returnli = processEachResultFrameElement(value,coversationId,objectUl1);
					objectli = document.createElement('li');
					objectli.append(createResultFrameSpanElement(key));
					objectli.append(returnli);
					frameUL.append(objectli);
				}
			else {
				text = document.createElement('li');			
				text.appendChild(createResultFramePropertySPAN(key,value))
				frameUL.append(text);
			}
		}
	}
	else {
		
	}
	return frameUL;
}
function createResultFrameSpanElement(spanText)
{
	span1 = document.createElement('span');
	span1.setAttribute("style","color:white;background-color:#6c8ebf;");
	span1.innerHTML = "Coll";
	
	span2 = document.createElement('span');
	span2.setAttribute("style","color:black;background-color:white;");
	span2.innerHTML = "&nbsp;&nbsp;"+spanText;
	
	
 	var textSpan = document.createElement('span');
 	textSpan.setAttribute("class","rbox");
 	textSpan.appendChild(span1);
	textSpan.appendChild(span2);
 	
 	return textSpan;
}

function createResultFramePropertySPAN(key,value)
{
	span1 = document.createElement('span');
	span1.setAttribute("style","color:white;background-color:#6c8ebf;");
	span1.innerHTML = "Prop"
	span2 = document.createElement('span');
	span2.setAttribute("style","color:black;");
	if (isNaN(key))
	{
		span2.innerHTML = "&nbsp;&nbsp;"+key+"&nbsp;&nbsp; :"+"&nbsp;&nbsp;"+value;
	}
	else {
		span2.innerHTML = "&nbsp;&nbsp;"+value;
	}
	
	span3 = document.createElement('span');
	span3.setAttribute("class","listElement");
	span3.appendChild(span1);
	span3.appendChild(span2);
	return span3;
}
