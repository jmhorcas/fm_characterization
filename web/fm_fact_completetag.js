const POINT_TO_PIXEL = 1.3281472327365;
const TITLE_FONT_FAMILY = "Franklin Gothic Heavy";
const TITLE_FONT_SIZE = "24pt";
const PROPERTY_FONT_FAMILY = "Helvetica";
const PROPERTY_FONT_SIZE = "12pt";
const VALUES_FONT_FAMILY = "Helvetica";
const VALUES_FONT_SIZE = "10pt";
const PROPERTY_INDENTATION = 2;
const TOP_MARGING = 20;
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
   //var maxWidth = calculateTotalMaxWidth(data.metrics);
   var maxIndentationWidth = calculateMaxIndentationWidth(data.metrics);
   var maxNameWidth = calculateMaxNameWidth(data.metrics);
   var maxValueWidth = calculateMaxValueWidth(data.metrics);
   var maxRatioWidth = calculateMaxRatioWidth(data.metrics);
   var maxWidth = maxIndentationWidth + maxNameWidth + PROPERTIES_VALUES_SPACE + maxValueWidth + PROPERTIES_RATIO_SPACE + maxRatioWidth;
                
   chart.attr("width", maxWidth)
        .attr("height", BAR_HEIGHT*10 + BAR_HEIGHT*data.metadata.length + BAR_HEIGHT*data.metrics.length); // CAMBIAR EL *10 AJUSTANDOLO BIEN
   
   var x = d3.scaleLinear().domain([0, maxWidth]).range([0, maxWidth]);

   // Title
   var titleSize = textSize(get_property(data, "Name").value, TITLE_FONT_FAMILY, TITLE_FONT_SIZE);
   var currentHeight = TOP_MARGING;
   var title = chart.append("g").attr("transform", "translate(0," + currentHeight + ")");
   title.append("text")
        .text(get_property(data, 'Name').value) 
        .attr("x", function(d) { return x(maxWidth/2); })
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
                         .attr("transform", function(d, i) { return "translate(0," + i * propertyHeight + ")"; });
   // property.append("rect")
   //         .attr("width", WIDTH)
   //         .attr("height", BAR_HEIGHT - 1)
   //         .classed("FMlabel_property", true)
   //         .attr("fill", "steelblue");
   property.append("text")
           .attr("text-anchor", "start")
           .attr("x", function(d) { return x(textSize("-".repeat(1 + PROPERTY_INDENTATION * parseInt(d.level, 10)), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width); })
           .attr("y", propertyHeight / 2)
           .attr("dy", ".35em")
           .attr("font-family", PROPERTY_FONT_FAMILY)
           .attr("font-size", PROPERTY_FONT_SIZE)
           .attr("font-weight", function(d) { return d.level == 0 ? "bold" : "normal"; })
           .text(function(d) { return d.name; });
   property.append("text")
           .attr("text-anchor", "end")
           .attr("x", function(d) { return x(maxIndentationWidth + maxNameWidth + PROPERTIES_VALUES_SPACE + maxValueWidth); })
           .attr("y", propertyHeight / 2)
           .attr("dy", ".35em")
           .attr("font-family", PROPERTY_FONT_FAMILY)
           .attr("font-size", VALUES_FONT_SIZE)
           .attr("font-weight", "bold")
           .text(function(d) { return get_value(d); });
   property.append("text")
           .attr("text-anchor", "end")
           .attr("x", function(d) { return x(maxWidth); })
           .attr("y", propertyHeight / 2)
           .attr("dy", ".35em")
           .attr("font-family", PROPERTY_FONT_FAMILY)
           .attr("font-size", VALUES_FONT_SIZE)
           .attr("font-weight", "bold")
           .text(function(d) { return get_ratio(d); });

   // Middle rule
   currentHeight += propertyHeight * data.metrics.length;
   chart.append("g")
        .attr("transform", "translate(0," + currentHeight + ")")
        .append("rect")
        .attr("height", MAIN_RULE_HEIGHT)
        .attr("width", maxWidth);

   // Analysis
   var analysis = chart.append("g").attr("transform", "translate(0," + currentHeight + ")");

//    var borderPath = chart.append("rect")
//   .attr("x", 0)
//   .attr("y", 0)
//   .attr("height", currentHeight)
//   .attr("width", maxWidth)
//   .style("stroke", "black")
//   .style("fill", "none")
//   .style("stroke-width", "3pt");

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
   text.each(function() {
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

function _5(DOM,serialize,chart) {
   return(DOM.download(() => serialize(chart), undefined, "Save as SVG"))
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
    return new Blob([string], {type: "image/svg+xml"});
  };
}

function _8(DOM,rasterize,chart){return(
   DOM.download(() => rasterize(chart), undefined, "Save as PNG")
   )}
   
   function _rasterize(DOM,serialize){return(
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
   )}

   function getSize(d) {
      var bbox = this.getBBox(),
          cbbox = this.parentNode.getBBox(),
          scale = Math.min(cbbox.width/bbox.width, cbbox.height/bbox.height);
      d.scale = scale;
    }

    function getSize2(d) {
      var bbox = d.node().getBBox(),
          cbbox = d.node().parentNode.getBBox(),
          scale = Math.min(cbbox.width/bbox.width, cbbox.height/bbox.height);
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
function textSize(text, fontFamily, fontSize, fontWeight="normal") {
   var container = d3.select('body').append('svg');
   container.append('text').text(text).attr("font-family", fontFamily).attr("font-size", fontSize).attr("font-weight", fontWeight);
   var size = container.node().getBBox();
   container.remove();
   return { width: size.width, height: size.height };
}

// Calculate the maximum width for a property's name.
function calculateMaxNameWidth(data) { 
   return Math.max.apply(Math, data.map(function(d) { 
      return textSize(d.name, PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width;
   }))
}

// Calculate the maximum width for a property's value.
function calculateMaxValueWidth(data) { 
   return Math.max.apply(Math, data.map(function(d) { 
      return textSize(String(get_value(d)), VALUES_FONT_FAMILY, VALUES_FONT_SIZE).width;
   }))
}

// Calculate the maximum width for a property's ratio.
function calculateMaxRatioWidth(data) { 
   return Math.max.apply(Math, data.map(function(d) { 
      return textSize(String(get_ratio(d)), VALUES_FONT_FAMILY, VALUES_FONT_SIZE).width;
   }))
}

// Calculate the maximum width for a property's indentation.
function calculateMaxIndentationWidth(data) { 
   return Math.max.apply(Math, data.map(function(d) { 
      return textSize("-".repeat(1 + PROPERTY_INDENTATION * parseInt(d.level, 10)), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width;
   }))
}