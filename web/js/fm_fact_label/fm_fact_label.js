const POINT_TO_PIXEL = 1.3281472327365;
//const TITLE_FONT_FAMILY = "Franklin Gothic Heavy";
const TITLE_FONT_FAMILY = "'Libre Franklin', sans-serif";
const TITLE_FONT_SIZE = "24pt";
const DESCRIPTION_FONT_FAMILY = "Helvetica";
const DESCRIPTION_FONT_SIZE = "8pt";
const PROPERTY_FONT_FAMILY = "Helvetica";
const PROPERTY_FONT_SIZE = "12pt";
const VALUES_FONT_FAMILY = "Helvetica";
const VALUES_FONT_SIZE = "10pt";
const COLLAPSEICON_FONT_SIZE = "8pt";
const PROPERTY_INDENTATION = 2;
const TOP_MARGING = 20;
const LEFT_MARGING = 5;
const MAIN_RULE_HEIGHT = 7 * POINT_TO_PIXEL;
const MARGING_BETWEEN_PROPERTIES = 3;
const PROPERTIES_VALUES_SPACE = 10;
const PROPERTIES_RATIO_SPACE = 3;

const EXPANDED_ICON = '\uf150';
const COLLAPSED_ICON = '\uf152';

// GLOBAL VARIABLES
var maxWidth;
var currentHeight;
var maxIndentationWidth;
var maxNameWidth
var maxValueWidth;
var maxRatioWidth;
var propertyHeight;
var x;
var yRule1;
var yMetrics;

var VISIBLE_PROPERTIES = {};
var ALL_DATA;

var IMPORTS = ['https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@900',
   'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css'];
function drawFMFactLabel(data) {
   var chart = d3.select(".chart");  // The svg 

   // chart.append('defs')
   //    .append('style')
   //    .attr('type', 'text/css')
   //    .text("@import url('https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@900');");
   chart.selectAll('defs')
      .data(IMPORTS, d => d)
      .join("style")
      .attr('type', 'text/css')
      .text(function (d) { return "@import url('" + d + "');"; });

   ALL_DATA = data
   // Initialize visible properties   
   for (let p of data.metadata) {VISIBLE_PROPERTIES[p.name] = true;}
   for (let p of data.metrics) {VISIBLE_PROPERTIES[p.name] = true;}
   for (let p of data.analysis) {VISIBLE_PROPERTIES[p.name] = true;}
    
   // Calculate maximum width for the label.
   //var maxWidth = Math.max(calculateTotalMaxWidth(data.metrics), calculateTotalMaxWidth(data.analysis));
   propertyHeight = textSize("Any text", PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE, "bold").height;// + MARGING_BETWEEN_PROPERTIES;
   maxIndentationWidth = Math.max(calculateMaxIndentationWidth(data.metrics), calculateMaxIndentationWidth(data.analysis));
   maxNameWidth = Math.max(calculateMaxNameWidth(data.metrics), calculateMaxNameWidth(data.analysis));
   maxValueWidth = Math.max(calculateMaxValueWidth(data.metrics), calculateMaxValueWidth(data.analysis));
   maxRatioWidth = Math.max(calculateMaxRatioWidth(data.metrics), calculateMaxRatioWidth(data.analysis));
   maxWidth = maxIndentationWidth + maxNameWidth + PROPERTIES_VALUES_SPACE + maxValueWidth + PROPERTIES_RATIO_SPACE + maxRatioWidth + LEFT_MARGING; //textSize("-".repeat(PROPERTY_INDENTATION), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width;
   chart.attr("width", maxWidth);
   //.attr("height", BAR_HEIGHT * 10 + BAR_HEIGHT * data.metadata.length + BAR_HEIGHT * data.metrics.length); // CAMBIAR EL *10 AJUSTANDOLO BIEN

   x = d3.scaleLinear().domain([0, maxWidth]).range([0, maxWidth]);

   // Title
   var titleSize = textSize(get_property(data, "Name").value, TITLE_FONT_FAMILY, TITLE_FONT_SIZE);
   var yTitle = TOP_MARGING;
   var title = chart.append("g").attr("transform", "translate(0," + yTitle + ")");
   title.append("text")
      .text(get_property(data, 'Name').value)
      .attr("x", function (d) { return x(maxWidth / 2); })
      //.attr("y", 3)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "central")
      .attr("font-family", TITLE_FONT_FAMILY)
      .attr("font-size", TITLE_FONT_SIZE)
      .attr("font-weight", "bold");

   // Description
   var yDescription = yTitle + titleSize.height + 1;
   var indentationDescription = textSize("-".repeat(PROPERTY_INDENTATION), DESCRIPTION_FONT_FAMILY, DESCRIPTION_FONT_SIZE).width;
   var description = chart.append("g").attr("transform", "translate(0," + yDescription + ")");
   description.append("text")
      .text(get_property(data, 'Description').value)
      .attr("x", function (d) { return x(indentationDescription) })
      //.attr("y", BAR_HEIGHT / 2)
      .attr("font-family", DESCRIPTION_FONT_FAMILY)
      .attr("font-size", DESCRIPTION_FONT_SIZE)
      .call(wrap, maxWidth - indentationDescription);
   var descriptionSize = description.node().getBBox();

   /*
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

   // Middle rule 1
   yRule1 = yDescription + descriptionSize.height + 1; //*data.metadata.slice(2).length;
   chart.append("g").attr("id", "rule1");
   drawRule("rule1", yRule1);

   // Metrics
   yMetrics = yRule1 + MAIN_RULE_HEIGHT;
   chart.append("g").attr("id", "metrics").attr("transform", "translate(0," + yMetrics + ")");
   var metricsHeight = updateProperties(data.metrics, "metrics");

   // Middle rule 2
   var yRule2 = yMetrics + metricsHeight;
   chart.append("g").attr("id", "rule2");
   drawRule("rule2", yRule2);

   // Analysis
   var yAnalysis = yRule2 + MAIN_RULE_HEIGHT;
   chart.append("g").attr("id", "analysis").attr("transform", "translate(0," + yAnalysis + ")");
   var analysisHeight = updateProperties(data.analysis, "analysis");

   // Border of the label
   var maxHeight = yAnalysis + analysisHeight + MARGING_BETWEEN_PROPERTIES;
   chart.append("rect").attr("id", "border");
   drawBorders(maxWidth, maxHeight);

   chart.attr("height", maxHeight);

   // Set the configuration options
   d3.select("#collapseZeroValues").on("change", function () { collapseZeroValues(data); });
   d3.select("#collapseSubProperties").on("change", function () { collapseSubProperties(data); });
   //d3.selectAll("#collapse").on("click", function (d) { collapseProperty(data, d); });
}

function updateProperties(data, id) {
   var property = d3.select("#" + id)
      .selectAll("g")
      .data(data, d => d)
      .join("g")
      .attr("transform", function (d, i) { return "translate(0," + i * propertyHeight + ")"; });
   // Indentation
   property.append("id", function (d) { return d.name; })
      .append("rect")
      .attr("x", function (d) { return x(0); })
      .attr("y", propertyHeight)
      .attr("dy", ".35em")
      .attr("width", function (d) { return get_indentation(d); })
      .attr("height", propertyHeight)
      .attr("fill", "white");
   //.append("text")
   // .attr("text-anchor", "start")
   // .attr("x", function (d) { return x(0); })
   // .attr("y", propertyHeight / 2)
   // .attr("dy", ".35em")
   // .attr("font-family", PROPERTY_FONT_FAMILY)
   // .attr("font-size", PROPERTY_FONT_SIZE)
   // .attr("font-weight", function (d) { return parseInt(d.level, 10) == 0 ? "bold" : "normal"; })

   //.text(function (d) { return "-".repeat(1 + PROPERTY_INDENTATION * parseInt(d.level, 10)); });
   // Collapse icon
   var maxLevel = calculateMaxLevel(data)
   var collapseIcon = property.append('text')
      .attr("x", function (d) { return get_indentation(d); })
      .attr("dy", ".35em")
      .attr("y", propertyHeight / 2)
      .attr('font-family', 'FontAwesome')
      .attr('font-size', COLLAPSEICON_FONT_SIZE)
      .text(function (d) { return hasChildrenProperties(d) && getChildrenProperties(data, d).length == 0 ? COLLAPSED_ICON : EXPANDED_ICON; })
      .attr("visibility", function (d) { return hasChildrenProperties(d) ? "visible" : "hidden"; })
      .attr("cursor", "pointer")
      .on("click", function (p, d) { hasChildrenProperties(d) && getChildrenProperties(data, d).length == 0 ? expandProperty(ALL_DATA, d) : collapseProperty(ALL_DATA, d); });

   var collapseIconWidth = collapseIcon.node() === null ? 0 : collapseIcon.node().getBBox().width;

   // property.append('svg:foreignObject')
   //    .attr("x", function (d) { return textSize("-".repeat(1 + PROPERTY_INDENTATION * parseInt(d.level, 10)), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width; })
   //    .attr("y", propertyHeight)
   //    .attr("dy", ".35em")
   //    .html('<i class="fa-regular fa-square-caret-down"></i>');
   // property.append("i")
   //    .attr("x", function (d) { return textSize("-".repeat(1 + PROPERTY_INDENTATION * parseInt(d.level, 10)), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width; })
   //    .attr("y", propertyHeight)
   //    .attr("dy", ".35em")
   //    .attr("class", "fa-regular fa-square-caret-down")
   property.append("text")
      .attr("text-anchor", "start")
      .attr("x", function (d) { return get_indentation(d) + collapseIconWidth + PROPERTY_INDENTATION; })
      .attr("y", propertyHeight / 2)
      .attr("dy", ".35em")
      .attr("font-family", PROPERTY_FONT_FAMILY)
      .attr("font-size", PROPERTY_FONT_SIZE)
      .attr("font-weight", function (d) { return parseInt(d.level, 10) == 0 ? "bold" : "normal"; })
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
   return propertyHeight * data.length;
}

function drawRule(id, yPosition) {
   d3.select("#" + id)
      .attr("transform", "translate(0," + yPosition + ")")
      .append("rect")
      .attr("height", MAIN_RULE_HEIGHT)
      .attr("width", maxWidth);
}

function drawBorders(width, height) {
   d3.select("#border")
      .attr("x", 0)
      .attr("y", 0)
      .attr("width", width)
      .attr("height", height)
      .style("stroke", "black")
      .style("fill", "none")
      .style("stroke-width", "3pt");
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
 * @param {any} d A FM property. 
 * @returns The indentation width.
 */
function get_indentation(d) {
   return textSize("-".repeat(1 + PROPERTY_INDENTATION * parseInt(d.level, 10)), PROPERTY_FONT_FAMILY, PROPERTY_FONT_SIZE).width;
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
 * @param {Array} data    Array of properties.
 * @param {any} property  Property.
 * @returns List of children of the property.
 */
function getChildrenProperties(data, property) {
   var children = [];
   for (let p of data) {
      if (p.parent == property.name) {
         children.push(p);
      }
   }
   for (let c of children) {
      subChildren = getChildrenProperties(data, c);
      for (let sb of subChildren) {
         children.push(sb);
      }
   }
   return children;
}

function hasChildrenProperties(property) {
   for (let p of ALL_DATA.metrics) {
      if (p.parent == property.name) {
         return true;
      }
   }
   for (let p of ALL_DATA.analysis) {
      if (p.parent == property.name) {
         return true;
      }
   }
   return false;
}

function calculateMaxLevel(data) {
   return Math.max.apply(Math, data.map(function (d) {
      return parseInt(d.level, 10);
   }))
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

function filterData(data) {
   if (d3.select("#collapseSubProperties").property("checked")) {
      metrics = data.metrics.filter(function (d, i) { return parseInt(d.level, 10) == 0; });
      analysis = data.analysis.filter(function (d, i) { return parseInt(d.level, 10) == 0; });
   } else {
      metrics = data.metrics;
      analysis = data.analysis;
   }
   if (d3.select("#collapseZeroValues").property("checked")) {
      metrics = metrics.filter(function (d, i) { return get_value(d) != '0'; });
      analysis = analysis.filter(function (d, i) { return get_value(d) != '0'; });
   }
   metrics = metrics.filter(function (d, i) { return VISIBLE_PROPERTIES[d.name]; });
   analysis = analysis.filter(function (d, i) { return VISIBLE_PROPERTIES[d.name]; });
   return { "metadata": data.metadata, "metrics": metrics, "analysis": analysis };
}

function redrawLabel(data) {
   var height = 0;
   var metricsHeight = updateProperties(data.metrics, "metrics");
   height = yMetrics + metricsHeight;
   drawRule("rule2", height);
   height += MAIN_RULE_HEIGHT;
   d3.select("#analysis").attr("transform", "translate(0," + height + ")")
   var analysisHeight = updateProperties(data.analysis, "analysis");
   height += analysisHeight + MARGING_BETWEEN_PROPERTIES;
   drawBorders(maxWidth, height);
   d3.select("chart").attr("height", height);
}
/**
 * Set-up the collapse zero values option.
 */
function collapseZeroValues(data) {
   var newData = filterData(data);
   redrawLabel(newData);
}

function collapseSubProperties(data) {
   var newData = filterData(data);
   redrawLabel(newData);
}

function collapseProperty(data, property) {
   var children = getChildrenProperties(data.metrics, property);
   for (let c of children) {VISIBLE_PROPERTIES[c.name] = false;}
   var children = getChildrenProperties(data.analysis, property);
   for (let c of children) {VISIBLE_PROPERTIES[c.name] = false;}
   newData = filterData(data);
   redrawLabel(newData);
}

function expandProperty(data, property) {
   var children = getChildrenProperties(data.metrics, property);
   for (let c of children) {VISIBLE_PROPERTIES[c.name] = true;}
   var children = getChildrenProperties(data.analysis, property);
   for (let c of children) {VISIBLE_PROPERTIES[c.name] = true;}
   newData = filterData(data);
   redrawLabel(newData);
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
