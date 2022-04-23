const POINT_TO_PIXEL = 1.3281472327365;
//const TITLE_FONT_FAMILY = "Franklin Gothic Heavy";
const TITLE_FONT_FAMILY = "'Libre Franklin', sans-serif";
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

function drawFMFactLabel(data) {
   var chart = d3.select(".chart");

   // Calculate maximum width for the label.
   //var maxWidth = Math.max(calculateTotalMaxWidth(data.metrics), calculateTotalMaxWidth(data.analysis));

   var maxIndentationWidth = Math.max(calculateMaxIndentationWidth(data.metrics), calculateMaxIndentationWidth(data.analysis));
   var maxNameWidth = Math.max(calculateMaxNameWidth(data.metrics), calculateMaxNameWidth(data.analysis));
   var maxValueWidth = Math.max(calculateMaxValueWidth(data.metrics), calculateMaxValueWidth(data.analysis));
   var maxRatioWidth = Math.max(calculateMaxRatioWidth(data.metrics), calculateMaxRatioWidth(data.analysis));
   var maxWidth = maxIndentationWidth + maxNameWidth + PROPERTIES_VALUES_SPACE + maxValueWidth + PROPERTIES_RATIO_SPACE + maxRatioWidth + LEFT_MARGING; //textSize("-".repeat(PROPERTY_INDENTATION), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width;

   chart.attr("width", maxWidth);
      //.attr("height", BAR_HEIGHT * 10 + BAR_HEIGHT * data.metadata.length + BAR_HEIGHT * data.metrics.length); // CAMBIAR EL *10 AJUSTANDOLO BIEN

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
   currentHeight += propertyHeight * data.analysis.length + MARGING_BETWEEN_PROPERTIES;
   var borderPath = chart.append("rect")
      .attr("x", 0)
      .attr("y", 0)
      .attr("height", currentHeight)
      .attr("width", maxWidth)
      .style("stroke", "black")
      .style("fill", "none")
      .style("stroke-width", "3pt");
   
   chart.attr("height", currentHeight);
}

/**
 * 
 * @param {any} d A FM property.
 * @returns The value for the property.
 */
function get_value(d) {
   return d.size === null ? d.value : d.size;
}

/**
 * 
 * @param {any} d A FM property.
 * @returns The percentage for the property.
 */
function get_ratio(d) {
   return d.ratio === null ? "" : "(" + Math.round((d.ratio + Number.EPSILON) * 100) + "%)"; 
}

/**
 * 
 * @param {Array} data Dataset.
 * @param {String} propertyName Property's name.
 * @returns The property by its name. 
 */
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
   for (let p of data.analysis) {
      if (p.name == propertyName) {
         return p;
      }
   }
}

/**
 * Wrap the text D3 Object to the given width.
 * 
 * @param {Object} text Text to be wrapped.
 * @param {String} width Width used for wrapping.
 */
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

// function getSize(d) {
//    var bbox = this.getBBox(),
//       cbbox = this.parentNode.getBBox(),
//       scale = Math.min(cbbox.width / bbox.width, cbbox.height / bbox.height);
//    d.scale = scale;
// }

// function getSize2(d) {
//    var bbox = d.node().getBBox(),
//       cbbox = d.node().parentNode.getBBox(),
//       scale = Math.min(cbbox.width / bbox.width, cbbox.height / bbox.height);
//    d.scale = scale;
// }


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

/**
 * 
 * @param {Array} data Dataset.
 * @returns Maximum width for a property's name in the dataset.
 */
function calculateMaxNameWidth(data) {
   return Math.max.apply(Math, data.map(function (d) {
      return textSize(d.name, PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width;
   }))
}

/**
 * 
 * @param {Array} data Dataset.
 * @returns Maximum width for a property's value in the dataset.
 */
function calculateMaxValueWidth(data) {
   return Math.max.apply(Math, data.map(function (d) {
      return textSize(String(get_value(d)), VALUES_FONT_FAMILY, VALUES_FONT_SIZE).width;
   }))
}

/**
 * 
 * @param {Array} data Dataset.
 * @returns Maximum width for a property's ratio in the dataset.
 */
function calculateMaxRatioWidth(data) {
   return Math.max.apply(Math, data.map(function (d) {
      return textSize(String(get_ratio(d)), VALUES_FONT_FAMILY, VALUES_FONT_SIZE).width;
   }))
}

/**
 * 
 * @param {Array} data Dataset.
 * @returns Maximum width for a property's indentation in the dataset.
 */
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
