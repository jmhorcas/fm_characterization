const POINT_TO_PIXEL = 1.3281472327365;
const TITLE_FONT_FAMILY = "Franklin Gothic Heavy";
const TITLE_FONT_SIZE = "24pt";
const PROPERTY_FONT_FAMILY = "Helvetica";
const PROPERTY_FONT_SIZE = "12pt";
const VALUES_FONT_FAMILY = "Helvetica";
const VALUES_FONT_SIZE = "10pt";
const PROPERTY_INDENTATION = 2;
const TOP_MARGING = 20;
const LEFT_MARGING = 5;
const MAIN_RULE_HEIGHT = 7 * POINT_TO_PIXEL;
const MARGING_BETWEEN_PROPERTIES = 3;
const PROPERTIES_VALUES_SPACE = 10;
const PROPERTIES_RATIO_SPACE = 3;

var WIDTH = 200;
var BAR_HEIGHT = 20;
var TITLE_HEIGHT = 20;
var DESCRIPTION_HEIGHT = 40;
var RULE_HEIGHT = 7;

function drawFMFactTag(data) {
   var chart = d3.select(".chart");

   // Calculate maximum width for the label.
   //var maxWidth = Math.max(calculateTotalMaxWidth(data.metrics), calculateTotalMaxWidth(data.analysis));

   var maxIndentationWidth = Math.max(calculateMaxIndentationWidth(data.metrics), calculateMaxIndentationWidth(data.analysis));
   var maxNameWidth = Math.max(calculateMaxNameWidth(data.metrics), calculateMaxNameWidth(data.analysis));
   var maxValueWidth = Math.max(calculateMaxValueWidth(data.metrics), calculateMaxValueWidth(data.analysis));
   var maxRatioWidth = Math.max(calculateMaxRatioWidth(data.metrics), calculateMaxRatioWidth(data.analysis));
   var maxWidth = maxIndentationWidth + maxNameWidth + PROPERTIES_VALUES_SPACE + maxValueWidth + PROPERTIES_RATIO_SPACE + maxRatioWidth + LEFT_MARGING; //textSize("-".repeat(PROPERTY_INDENTATION), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width;

   chart.attr("width", maxWidth)
      .attr("height", BAR_HEIGHT * 10 + BAR_HEIGHT * data.metadata.length + BAR_HEIGHT * data.metrics.length); // CAMBIAR EL *10 AJUSTANDOLO BIEN

   var x = d3.scaleLinear().domain([0, maxWidth]).range([0, maxWidth]);

   // Title
   var titleSize = textSize(get_property(data, "Name").value, TITLE_FONT_FAMILY, TITLE_FONT_SIZE);
   var currentHeight = TOP_MARGING;
   var title = chart.append("g").attr("transform", "translate(0," + currentHeight + ")");
   title.append("text")
      .text(get_property(data, 'Name').value)
      .attr("x", function (d) { return x(maxWidth / 2); })
      //.attr("y", 3)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "central")
      .attr("font-family", TITLE_FONT_FAMILY)
      .attr("font-size", TITLE_FONT_SIZE);

   /*
   // Description
   currentHeight += TITLE_HEIGHT;
   var description = chart.append("g").attr("transform", "translate(0," + currentHeight + ")");
   description.append("text")
              .text(get_property(data, 'Description').value) 
              .attr("x", function(d) { return x(0); })
              .attr("y", BAR_HEIGHT / 2)
              .attr("font-family", "Helvetica")
              .attr("font-size", "8pt")
              .call(wrap, WIDTH);      

   // Other metadata
   currentHeight += DESCRIPTION_HEIGHT;
   var metadata = chart.append("g").attr("transform", "translate(0," + currentHeight + ")");
   var property = metadata.selectAll("g")
                          .data(data.metadata.slice(2))
                          .enter().append("g")
                          .attr("transform", function(d, i) { return "translate(0," + i * BAR_HEIGHT + ")"; });
   property.append("text")
           .attr("x", function(d) { return x(0); })
           .attr("y", BAR_HEIGHT / 2)
           .attr("font-family", "Helvetica")
           .attr("font-size", "8pt")
           .text(function(d) { return d.name + ":"; });        
   property.append("text")
           .attr("x", function(d) { return d.name.length*7; })
           .attr("y", BAR_HEIGHT / 2)
           .attr("font-family", "Helvetica")
           .attr("font-size", "8pt")
           .text(function(d) { return d.value; })
           .call(wrap, WIDTH);
   */

   // Middle rule
   currentHeight += titleSize.height; //*data.metadata.slice(2).length;
   chart.append("g")
      .attr("transform", "translate(0," + currentHeight + ")")
      .append("rect")
      .attr("height", MAIN_RULE_HEIGHT)
      .attr("width", maxWidth);

   // Metrics
   currentHeight += MAIN_RULE_HEIGHT;
   var metrics = chart.append("g").attr("transform", "translate(0," + currentHeight + ")");

   var propertyHeight = textSize("Any text", PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE, "bold").height + MARGING_BETWEEN_PROPERTIES;
   var property = metrics.selectAll("g")
      .data(data.metrics)
      .enter().append("g")
      .attr("transform", function (d, i) { return "translate(0," + i * propertyHeight + ")"; });
   property.append("text")
      .attr("text-anchor", "start")
      .attr("x", function (d) { return x(textSize("-".repeat(1 + PROPERTY_INDENTATION * parseInt(d.level, 10)), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width); })
      .attr("y", propertyHeight / 2)
      .attr("dy", ".35em")
      .attr("font-family", PROPERTY_FONT_FAMILY)
      .attr("font-size", PROPERTY_FONT_SIZE)
      .attr("font-weight", function (d) { return d.level == 0 ? "bold" : "normal"; })
      .text(function (d) { return d.name; });
   property.append("text")
      .attr("text-anchor", "end")
      .attr("x", function (d) { return x(maxIndentationWidth + maxNameWidth + PROPERTIES_VALUES_SPACE + maxValueWidth); })
      .attr("y", propertyHeight / 2)
      .attr("dy", ".35em")
      .attr("font-family", PROPERTY_FONT_FAMILY)
      .attr("font-size", VALUES_FONT_SIZE)
      .attr("font-weight", "bold")
      .text(function (d) { return get_value(d); });
   property.append("text")
      .attr("text-anchor", "end")
      .attr("x", function (d) { return x(maxWidth - LEFT_MARGING); })
      .attr("y", propertyHeight / 2)
      .attr("dy", ".35em")
      .attr("font-family", PROPERTY_FONT_FAMILY)
      .attr("font-size", VALUES_FONT_SIZE)
      .attr("font-weight", "bold")
      .text(function (d) { return get_ratio(d); });

   // Middle rule
   currentHeight += propertyHeight * data.metrics.length;
   chart.append("g")
      .attr("transform", "translate(0," + currentHeight + ")")
      .append("rect")
      .attr("height", MAIN_RULE_HEIGHT)
      .attr("width", maxWidth);

   // Analysis
   currentHeight += MAIN_RULE_HEIGHT;
   var analysis = chart.append("g").attr("transform", "translate(0," + currentHeight + ")");
   var property = analysis.selectAll("g")
      .data(data.analysis)
      .enter().append("g")
      .attr("transform", function (d, i) { return "translate(0," + i * propertyHeight + ")"; });
   property.append("text")
      .attr("text-anchor", "start")
      .attr("x", function (d) { return x(textSize("-".repeat(1 + PROPERTY_INDENTATION * parseInt(d.level, 10)), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width); })
      .attr("y", propertyHeight / 2)
      .attr("dy", ".35em")
      .attr("font-family", PROPERTY_FONT_FAMILY)
      .attr("font-size", PROPERTY_FONT_SIZE)
      .attr("font-weight", function (d) { return d.level == 0 ? "bold" : "normal"; })
      .text(function (d) { return d.name; });
   property.append("text")
      .attr("text-anchor", "end")
      .attr("x", function (d) { return x(maxIndentationWidth + maxNameWidth + PROPERTIES_VALUES_SPACE + maxValueWidth); })
      .attr("y", propertyHeight / 2)
      .attr("dy", ".35em")
      .attr("font-family", PROPERTY_FONT_FAMILY)
      .attr("font-size", VALUES_FONT_SIZE)
      .attr("font-weight", "bold")
      .text(function (d) { return get_value(d); });
   property.append("text")
      .attr("text-anchor", "end")
      .attr("x", function (d) { return x(maxWidth - LEFT_MARGING); })
      .attr("y", propertyHeight / 2)
      .attr("dy", ".35em")
      .attr("font-family", PROPERTY_FONT_FAMILY)
      .attr("font-size", VALUES_FONT_SIZE)
      .attr("font-weight", "bold")
      .text(function (d) { return get_ratio(d); });


   // Border of the label
   currentHeight += propertyHeight * data.analysis.length;
   var borderPath = chart.append("rect")
      .attr("x", 0)
      .attr("y", 0)
      .attr("height", currentHeight)
      .attr("width", maxWidth)
      .style("stroke", "black")
      .style("fill", "none")
      .style("stroke-width", "3pt");


   // Set-up the export button
   // d3.select('#savePNG').on('click', function () {
   //    var svgString = getSVGString(chart.node());
   //    svgString2Image(svgString, 2 * maxWidth, 2 * currentHeight, 'pdf', save); // passes Blob and filesize String to the callback

   //    function save(dataBlob, filesize) {
   //       saveAs(dataBlob, 'D3 vis exported to PNG.png'); // FileSaver.js function
   //    }
   // });

   // Set-up the export button
   d3.select('#savePNG').on('click', function () {
      //download(() => rasterize(chart.node()), undefined, "Save as PNG");
      var blob = rasterize(chart.node());
      saveAs(blob, get_property(data, 'Name').value + ".png")
   });

   // Set-up the export button
   d3.select('#saveSVG').on('click', function () {
      //download(() => serialize(chart.node()), undefined, "Save as SVG");
      var blob = serialize(chart.node());
      saveAs(blob, get_property(data, 'Name').value + ".svg")
   });

   // Set-up the export button
   d3.select('#saveTXT').on('click', function () {
      var blob = new Blob([fmCharacterizationString], { type: "text/plain" });
      saveAs(blob, get_property(data, 'Name').value + ".txt")
   });
}

function get_value(d) {
   if (d.size === null) {
      return d.value;
   } else {
      return d.size;
   }
}

function get_ratio(d) {
   if (d.ratio === null) {
      return "";
   } else {
      return "(" + Math.round((d.ratio + Number.EPSILON) * 100) + "%)";
   }
}


function get_property(data, propertyName) {
   for (let p of data.metadata) {
      if (p.name == propertyName) {
         return p;
      }
   }
   for (let p of data.metrics) {
      if (p.name == propertyName) {
         return p;
      }
   }
}

function wrap(text, width) {
   text.each(function () {
      var text = d3.select(this),
         words = text.text().split(/\s+/).reverse(),
         word,
         line = [],
         lineNumber = 0, //<-- 0!
         lineHeight = 1.2, // ems
         x = text.attr("x"), //<-- include the x!
         y = text.attr("y"),
         dy = text.attr("dy") ? text.attr("dy") : 0; //<-- null check
      tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em");
      while (word = words.pop()) {
         line.push(word);
         tspan.text(line.join(" "));
         if (tspan.node().getComputedTextLength() > width) {
            line.pop();
            tspan.text(line.join(" "));
            line = [word];
            tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
         }
      }
   });
}

function type(d) {
   d.value = +d.value;
   return d;
}

function _5(DOM, serialize, chart) {
   return (DOM.download(() => serialize(chart), undefined, "Save as SVG"))
}

function _serialize(NodeFilter) {
   const xmlns = "http://www.w3.org/2000/xmlns/";
   const xlinkns = "http://www.w3.org/1999/xlink";
   const svgns = "http://www.w3.org/2000/svg";
   return function serialize(svg) {
      svg = svg.cloneNode(true);
      const fragment = window.location.href + "#";
      const walker = document.createTreeWalker(svg, NodeFilter.SHOW_ELEMENT);
      while (walker.nextNode()) {
         for (const attr of walker.currentNode.attributes) {
            if (attr.value.includes(fragment)) {
               attr.value = attr.value.replace(fragment, "#");
            }
         }
      }
      svg.setAttributeNS(xmlns, "xmlns", svgns);
      svg.setAttributeNS(xmlns, "xmlns:xlink", xlinkns);
      const serializer = new window.XMLSerializer;
      const string = serializer.serializeToString(svg);
      return new Blob([string], { type: "image/svg+xml" });
   };
}

function _8(DOM, rasterize, chart) {
   return (
      DOM.download(() => rasterize(chart), undefined, "Save as PNG")
   )
}

function _rasterize(DOM, serialize) {
   return (
      function rasterize(svg) {
         let resolve, reject;
         const promise = new Promise((y, n) => (resolve = y, reject = n));
         const image = new Image;
         image.onerror = reject;
         image.onload = () => {
            const rect = svg.getBoundingClientRect();
            const context = DOM.context2d(rect.width, rect.height);
            context.drawImage(image, 0, 0, rect.width, rect.height);
            context.canvas.toBlob(resolve);
         };
         image.src = URL.createObjectURL(serialize(svg));
         return promise;
      }
   )
}

function getSize(d) {
   var bbox = this.getBBox(),
      cbbox = this.parentNode.getBBox(),
      scale = Math.min(cbbox.width / bbox.width, cbbox.height / bbox.height);
   d.scale = scale;
}

function getSize2(d) {
   var bbox = d.node().getBBox(),
      cbbox = d.node().parentNode.getBBox(),
      scale = Math.min(cbbox.width / bbox.width, cbbox.height / bbox.height);
   d.scale = scale;
}


/**
 * Measure text size in pixels with D3.js
 * 
 * Usage: textSize("This is a very long text"); 
 * => Return: Object {width: 140, height: 15.453125}
 * 
 * @param {String} text 
 * @param {String} fontFamily 
 * @param {String} fontSize 
 * @param {String} fontWeight
 * @returns Object including width and height.
 */
function textSize(text, fontFamily, fontSize, fontWeight = "normal") {
   var container = d3.select('body').append('svg');
   container.append('text').text(text).attr("font-family", fontFamily).attr("font-size", fontSize).attr("font-weight", fontWeight);
   var size = container.node().getBBox();
   container.remove();
   return { width: size.width, height: size.height };
}

// Calculate the maximum width for a property's name.
function calculateMaxNameWidth(data) {
   return Math.max.apply(Math, data.map(function (d) {
      return textSize(d.name, PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width;
   }))
}

// Calculate the maximum width for a property's value.
function calculateMaxValueWidth(data) {
   return Math.max.apply(Math, data.map(function (d) {
      return textSize(String(get_value(d)), VALUES_FONT_FAMILY, VALUES_FONT_SIZE).width;
   }))
}

// Calculate the maximum width for a property's ratio.
function calculateMaxRatioWidth(data) {
   return Math.max.apply(Math, data.map(function (d) {
      return textSize(String(get_ratio(d)), VALUES_FONT_FAMILY, VALUES_FONT_SIZE).width;
   }))
}

// Calculate the maximum width for a property's indentation.
function calculateMaxIndentationWidth(data) {
   return Math.max.apply(Math, data.map(function (d) {
      return textSize("-".repeat(1 + PROPERTY_INDENTATION * parseInt(d.level, 10)), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width;
   }))
}

// function calculateTotalMaxWidth(data) {
//    return Math.max.apply(Math, data.map(function(d) { 
//       indentationWidth = textSize("-".repeat(1 + PROPERTY_INDENTATION * parseInt(d.level, 10)), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width;
//       nameWidth = textSize(d.name, PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width;
//       valueWidth = textSize(String(get_value(d)), VALUES_FONT_FAMILY, VALUES_FONT_SIZE).width;
//       ratioWidth = textSize(String(get_ratio(d)), VALUES_FONT_FAMILY, VALUES_FONT_SIZE).width;
//       return indentationWidth + nameWidth + valueWidth + ratioWidth;
//    })) + PROPERTIES_VALUES_SPACE + PROPERTIES_RATIO_SPACE + LEFT_MARGING;
// };

// function saveSVG3() {
//    //var svgElement = document.getElementById('FMFactLabelChart');
//    var chart = d3.select(".chart");
//    var blob = serialize(chart);
//    let URL = window.URL || window.webkitURL || window;
//    let blobURL = URL.createObjectURL(blob);

//    let image = new Image();
//    image.onload = () => {
//       let canvas = document.createElement('canvas');
//       canvas.widht = width;
//       canvas.height = height;
//       let context = canvas.getContext('2d');
//       // draw image in canvas starting left-0 , top - 0  
//       context.drawImage(image, 0, 0, width, height );
//       //  downloadImage(canvas); need to implement
//       let png = canvas.toDataURL(); // default png
//       download(png, "image.png");
//    };
//    image.src = blobURL;
// }

// function download(href, name){
//    var link = document.createElement('a');
//    link.download = name;
//    link.style.opacity = "0";
//    document.append(link);
//    link.href = href;
//    link.click();
//    link.remove();
//  }

// function saveSVG2() {
//    console.log("saveSVG");
//    var chart = d3.select(".chart");
//    var canvas = document.getElementById("mycanvas");
//    blob = _serialize(chart);
//    console.log('blob: ' + blob);
//    saveBlob(blob, 'test.svg');
//    //saveAs(blob, "example.svg");
// }

// function _serialize(NodeFilter) {
//    const xmlns = "http://www.w3.org/2000/xmlns/";
//    const xlinkns = "http://www.w3.org/1999/xlink";
//    const svgns = "http://www.w3.org/2000/svg";
//    return function serialize(svg) {
//       svg = svg.cloneNode(true);
//       const fragment = window.location.href + "#";
//       const walker = document.createTreeWalker(svg, NodeFilter.SHOW_ELEMENT);
//       while (walker.nextNode()) {
//          for (const attr of walker.currentNode.attributes) {
//             if (attr.value.includes(fragment)) {
//                attr.value = attr.value.replace(fragment, "#");
//             }
//          }
//       }
//       svg.setAttributeNS(xmlns, "xmlns", svgns);
//       svg.setAttributeNS(xmlns, "xmlns:xlink", xlinkns);
//       const serializer = new window.XMLSerializer;
//       const string = serializer.serializeToString(svg);
//       var url = "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(source);
//       document.getElementById("saveSVG").href = url;
//       return new Blob([string], { type: "image/svg+xml" });
//    };
// }

// function serialize(svg) {
//    const xmlns = "http://www.w3.org/2000/xmlns/";
//    const xlinkns = "http://www.w3.org/1999/xlink";
//    const svgns = "http://www.w3.org/2000/svg";

//    svg = svg.cloneNode(true);
//    const fragment = window.location.href + "#";
//    const walker = document.createTreeWalker(svg, NodeFilter.SHOW_ELEMENT);
//    while (walker.nextNode()) {
//       for (const attr of walker.currentNode.attributes) {
//          if (attr.value.includes(fragment)) {
//             attr.value = attr.value.replace(fragment, "#");
//          }
//       }
//    }
//    svg.setAttributeNS(xmlns, "xmlns", svgns);
//    svg.setAttributeNS(xmlns, "xmlns:xlink", xlinkns);
//    const serializer = new window.XMLSerializer;
//    const string = serializer.serializeToString(svg);
//    var url = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(source);
//    document.getElementById("saveSVG").href = url;
//    return new Blob([string], { type: "image/svg+xml" });
// }

// function saveBlob() {
//    var a = document.createElement("a");
//    document.body.appendChild(a);
//    a.style = "display: none";
//    return function (blob, fileName) {
//        var url = window.URL.createObjectURL(blob);
//        a.href = url;
//        a.download = fileName;
//        a.click();
//        window.URL.revokeObjectURL(url);
//    };
// }

// function importSVG(sourceSVG, targetCanvas) {
//    // https://developer.mozilla.org/en/XMLSerializer
//    svg_xml = (new XMLSerializer()).serializeToString(sourceSVG);
//    var ctx = targetCanvas.getContext('2d');

//    // this is just a JavaScript (HTML) image
//    var img = new Image();
//    // http://en.wikipedia.org/wiki/SVG#Native_support
//    // https://developer.mozilla.org/en/DOM/window.btoa
//    img.src = "data:image/svg+xml;base64," + btoa(svg_xml);

//    img.onload = function() {
//        // after this, Canvas’ origin-clean is DIRTY
//        ctx.drawImage(img, 0, 0);
//    }
// }

// function saveSVG() {
//    let svg = new XMLSerializer().serializeToString(document.getElementById("#FMFactLabelChart"));
//    let canvas = document.createElement("canvas");
//    let svgSize = $(svg)[0];
//    // let svgSize = $(svg)[0].getBoundingClientRect();
//    canvas.width = svgSize.width.baseVal.value;
//    canvas.height = svgSize.height.baseVal.value;

//    let ctx = canvas.getContext("2d");
//    let doc = new jsPDF({
//      orientation: 'l',
//      unit: 'px'
//    });
//    let img = document.createElement("img");
//    img.onload = () => {
//      ctx.drawImage(img, 0, 0);
//      // console.log(canvas.toDataURL("image/png"));
//      doc.setFontSize(11);
//      doc.text(5, 10, 'D3 Chart');
//      doc.addImage(canvas.toDataURL("image/png"), 'PNG', 10, 10);
//      doc.save('download.pdf');
//    };
//    img.setAttribute("src", "data:image/svg+xml;base64," + btoa(svg));
//  }


//  // Set-up the export button
// d3.select('#saveSVG').on('click', function(){
// 	var svgString = getSVGString(svg.node());
// 	svgString2Image( svgString, 2*width, 2*height, 'png', save ); // passes Blob and filesize String to the callback

// 	function save( dataBlob, filesize ){
// 		saveAs( dataBlob, 'D3 vis exported to PNG.png' ); // FileSaver.js function
// 	}
// });

// // Below are the functions that handle actual exporting:
// // getSVGString ( svgNode ) and svgString2Image( svgString, width, height, format, callback )
// function getSVGString( svgNode ) {
// 	svgNode.setAttribute('xlink', 'http://www.w3.org/1999/xlink');
// 	var cssStyleText = getCSSStyles( svgNode );
// 	appendCSS( cssStyleText, svgNode );

// 	var serializer = new XMLSerializer();
// 	var svgString = serializer.serializeToString(svgNode);
// 	svgString = svgString.replace(/(\w+)?:?xlink=/g, 'xmlns:xlink='); // Fix root xlink without namespace
// 	svgString = svgString.replace(/NS\d+:href/g, 'xlink:href'); // Safari NS namespace fix

// 	return svgString;

// 	function getCSSStyles( parentElement ) {
// 		var selectorTextArr = [];

// 		// Add Parent element Id and Classes to the list
// 		selectorTextArr.push( '#'+parentElement.id );
// 		for (var c = 0; c < parentElement.classList.length; c++)
// 				if ( !contains('.'+parentElement.classList[c], selectorTextArr) )
// 					selectorTextArr.push( '.'+parentElement.classList[c] );

// 		// Add Children element Ids and Classes to the list
// 		var nodes = parentElement.getElementsByTagName("*");
// 		for (var i = 0; i < nodes.length; i++) {
// 			var id = nodes[i].id;
// 			if ( !contains('#'+id, selectorTextArr) )
// 				selectorTextArr.push( '#'+id );

// 			var classes = nodes[i].classList;
// 			for (var c = 0; c < classes.length; c++)
// 				if ( !contains('.'+classes[c], selectorTextArr) )
// 					selectorTextArr.push( '.'+classes[c] );
// 		}

// 		// Extract CSS Rules
// 		var extractedCSSText = "";
// 		for (var i = 0; i < document.styleSheets.length; i++) {
// 			var s = document.styleSheets[i];

// 			try {
// 			    if(!s.cssRules) continue;
// 			} catch( e ) {
// 		    		if(e.name !== 'SecurityError') throw e; // for Firefox
// 		    		continue;
// 		    	}

// 			var cssRules = s.cssRules;
// 			for (var r = 0; r < cssRules.length; r++) {
// 				if ( contains( cssRules[r].selectorText, selectorTextArr ) )
// 					extractedCSSText += cssRules[r].cssText;
// 			}
// 		}


// 		return extractedCSSText;

// 		function contains(str,arr) {
// 			return arr.indexOf( str ) === -1 ? false : true;
// 		}

// 	}

// 	function appendCSS( cssText, element ) {
// 		var styleElement = document.createElement("style");
// 		styleElement.setAttribute("type","text/css"); 
// 		styleElement.innerHTML = cssText;
// 		var refNode = element.hasChildNodes() ? element.children[0] : null;
// 		element.insertBefore( styleElement, refNode );
// 	}
// }


// function svgString2Image( svgString, width, height, format, callback ) {
// 	var format = format ? format : 'png';

// 	var imgsrc = 'data:image/svg+xml;base64,'+ btoa( unescape( encodeURIComponent( svgString ) ) ); // Convert SVG string to data URL

// 	var canvas = document.createElement("canvas");
// 	var context = canvas.getContext("2d");

// 	canvas.width = width;
// 	canvas.height = height;

// 	var image = new Image();
// 	image.onload = function() {
// 		context.clearRect ( 0, 0, width, height );
// 		context.drawImage(image, 0, 0, width, height);

// 		canvas.toBlob( function(blob) {
// 			var filesize = Math.round( blob.length/1024 ) + ' KB';
// 			if ( callback ) callback( blob, filesize );
// 		});


// 	};

// 	image.src = imgsrc;
// }




// Below are the functions that handle actual exporting:
// getSVGString ( svgNode ) and svgString2Image( svgString, width, height, format, callback )
function getSVGString(svgNode) {
   svgNode.setAttribute('xlink', 'http://www.w3.org/1999/xlink');
   var cssStyleText = getCSSStyles(svgNode);
   appendCSS(cssStyleText, svgNode);

   var serializer = new XMLSerializer();
   var svgString = serializer.serializeToString(svgNode);
   svgString = svgString.replace(/(\w+)?:?xlink=/g, 'xmlns:xlink='); // Fix root xlink without namespace
   svgString = svgString.replace(/NS\d+:href/g, 'xlink:href'); // Safari NS namespace fix

   return svgString;

   function getCSSStyles(parentElement) {
      var selectorTextArr = [];

      // Add Parent element Id and Classes to the list
      selectorTextArr.push('#' + parentElement.id);
      for (var c = 0; c < parentElement.classList.length; c++)
         if (!contains('.' + parentElement.classList[c], selectorTextArr))
            selectorTextArr.push('.' + parentElement.classList[c]);

      // Add Children element Ids and Classes to the list
      var nodes = parentElement.getElementsByTagName("*");
      for (var i = 0; i < nodes.length; i++) {
         var id = nodes[i].id;
         if (!contains('#' + id, selectorTextArr))
            selectorTextArr.push('#' + id);

         var classes = nodes[i].classList;
         for (var c = 0; c < classes.length; c++)
            if (!contains('.' + classes[c], selectorTextArr))
               selectorTextArr.push('.' + classes[c]);
      }

      // Extract CSS Rules
      var extractedCSSText = "";
      for (var i = 0; i < document.styleSheets.length; i++) {
         var s = document.styleSheets[i];

         try {
            if (!s.cssRules) continue;
         } catch (e) {
            if (e.name !== 'SecurityError') throw e; // for Firefox
            continue;
         }

         var cssRules = s.cssRules;
         for (var r = 0; r < cssRules.length; r++) {
            if (contains(cssRules[r].selectorText, selectorTextArr))
               extractedCSSText += cssRules[r].cssText;
         }
      }


      return extractedCSSText;

      function contains(str, arr) {
         return arr.indexOf(str) === -1 ? false : true;
      }

   }

   function appendCSS(cssText, element) {
      var styleElement = document.createElement("style");
      styleElement.setAttribute("type", "text/css");
      styleElement.innerHTML = cssText;
      var refNode = element.hasChildNodes() ? element.children[0] : null;
      element.insertBefore(styleElement, refNode);
   }
}


function svgString2Image(svgString, width, height, format, callback) {
   var format = format ? format : 'png';

   var imgsrc = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgString))); // Convert SVG string to data URL

   var canvas = document.createElement("canvas");
   var context = canvas.getContext("2d");

   canvas.width = width;
   canvas.height = height;

   var image = new Image();
   image.onload = function () {
      context.clearRect(0, 0, width, height);
      context.drawImage(image, 0, 0, width, height);

      canvas.toBlob(function (blob) {
         var filesize = Math.round(blob.length / 1024) + ' KB';
         if (callback) callback(blob, filesize);
      });


   };

   image.src = imgsrc;
}

const xmlns = "http://www.w3.org/2000/xmlns/";
const xlinkns = "http://www.w3.org/1999/xlink";
const svgns = "http://www.w3.org/2000/svg";
function serialize(svg) {
   svg = svg.cloneNode(true);
   const fragment = window.location.href + "#";
   const walker = document.createTreeWalker(svg, NodeFilter.SHOW_ELEMENT);
   while (walker.nextNode()) {
      for (const attr of walker.currentNode.attributes) {
         if (attr.value.includes(fragment)) {
            attr.value = attr.value.replace(fragment, "#");
         }
      }
   }
   svg.setAttributeNS(xmlns, "xmlns", svgns);
   svg.setAttributeNS(xmlns, "xmlns:xlink", xlinkns);
   const serializer = new window.XMLSerializer;
   const string = serializer.serializeToString(svg);
   return new Blob([string], { type: "image/svg+xml" });
}

function rasterize(svg) {
   let resolve, reject;
   const promise = new Promise((y, n) => (resolve = y, reject = n));
   const image = new Image;
   image.onerror = reject;
   image.onload = () => {
      const rect = svg.getBoundingClientRect();
      const context = context2d(rect.width, rect.height);
      context.drawImage(image, 0, 0, rect.width, rect.height);
      context.canvas.toBlob(resolve);
   };
   image.src = URL.createObjectURL(serialize(svg));
   return promise;
}

function context2d(width, height, dpi) {
   if (dpi == null) dpi = devicePixelRatio;
   var canvas = document.createElement("canvas");
   canvas.width = width * dpi;
   canvas.height = height * dpi;
   canvas.style.width = width + "px";
   var context = canvas.getContext("2d");
   context.scale(dpi, dpi);
   return context;
 }

 function download(value, name = "untitled", label = "Save") {
   const a = html`<a><button></button></a>`;
   const b = a.firstChild;
   b.textContent = label;
   a.download = name;
 
   async function reset() {
     await new Promise(requestAnimationFrame);
     URL.revokeObjectURL(a.href);
     a.removeAttribute("href");
     b.textContent = label;
     b.disabled = false;
   }
 
   a.onclick = async event => {
     b.disabled = true;
     if (a.href) return reset(); // Already saved.
     b.textContent = "Saving…";
     try {
       const object = await (typeof value === "function" ? value() : value);
       b.textContent = "Download";
       a.href = URL.createObjectURL(object);
     } catch (ignore) {
       b.textContent = label;
     }
     if (event.eventPhase) return reset(); // Already downloaded.
     b.disabled = false;
   };
 
   return a;
 }