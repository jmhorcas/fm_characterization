var WIDTH = 250;
var BAR_HEIGHT = 20;

function drawFMFactTag(data) {
   var chart = d3.select(".chart");

   chart.attr("width", WIDTH)
        .attr("height", BAR_HEIGHT*10 + BAR_HEIGHT*data.metadata.length + BAR_HEIGHT*data.metrics.length); // CAMBIAR EL *10 AJUSTANDOLO BIEN
   
   var x = d3.scaleLinear()
             .domain([0, WIDTH])
             .range([0, WIDTH]);

   var currentHeight = BAR_HEIGHT;
   var title = chart.append("g").attr("transform", "translate(0," + currentHeight + ")");
   
   currentHeight += BAR_HEIGHT;
   var metadata = chart.append("g").attr("transform", "translate(0," + currentHeight + ")");

   currentHeight += BAR_HEIGHT*data.metadata.length;
   chart.append("g")
        .attr("transform", "translate(0," + currentHeight + ")")
        .append("rect")
        .classed("FMlabel_rule", true)
        .attr("width", WIDTH);

   currentHeight += BAR_HEIGHT;
   var metrics = chart.append("g").attr("transform", "translate(0," + currentHeight + ")");
   
   currentHeight += BAR_HEIGHT * data.metrics.length;
   chart.append("g")
   .attr("transform", "translate(0," + currentHeight + ")")
   .append("rect")
   .classed("FMlabel_rule", true)
   .attr("width", WIDTH);

   var analysis = chart.append("g").attr("transform", "translate(0," + currentHeight + ")");

   // Title
   title.append("text")
             .attr("x", function(d) { return x(0); })
             .attr("y", 3)
             .classed("FMlabel_title", true)
             .text(get_property(data, 'Name').value);

   var property = metadata.selectAll("g")
                          .data(data.metadata.slice(1))
                          .enter().append("g")
                          .attr("transform", function(d, i) { return "translate(0," + i * BAR_HEIGHT + ")"; });

   property.append("rect")
      .attr("width", WIDTH)
      .attr("height", BAR_HEIGHT - 1)
      .classed("FMlabel_property", true)
      .attr("fill", "steelblue");

   property.append("text")
           .attr("x", function(d) { return x(0); })
           .attr("y", BAR_HEIGHT / 2)
           .attr("font-family", "Helvetica")
           .attr("font-size", "12px")
           .text(function(d) { return d.name + ":"; });        

   property.append("text")
           .attr("x", function(d) { return d.name.length*7; })
           .attr("y", BAR_HEIGHT / 2)
           .attr("font-family", "Helvetica")
           .attr("font-size", "12px")
           .text(function(d) { return d.value; })
           .call(wrap, WIDTH);        

  

   // metadata.append("text")
   //         .attr("x", function(d) { return x(0); })
   //         .attr("y", 3)
   //         .attr("font-family", "Helvetica")
   //         .attr("font-size", "12px")
   //         .text("Metrics");          

   var property = metrics.selectAll("g")
             .data(data.metrics)
             .enter().append("g")
             .attr("transform", function(d, i) { return "translate(0," + i * BAR_HEIGHT + ")"; });

   property.append("rect")
 .attr("width", WIDTH)
 .attr("height", BAR_HEIGHT - 1)
 .classed("FMlabel_property", true)
 .attr("fill", "steelblue");

 property.append("text")
 .attr("text-anchor", "start")
 .attr("x", function(d) { return x(0) + 10*d.level + 3; })
 .attr("y", BAR_HEIGHT / 2)
 .attr("dy", ".35em")
 .attr("fill", "black")
 .text(function(d) { return d.name; });

 property.append("text")
 .attr("text-anchor", "end")
 .attr("x", WIDTH - 3)
 .attr("y", BAR_HEIGHT / 2)
 .attr("dy", ".35em")
 .text(function(d) { return get_value(d); });


   //drawMetadata(data);
   //drawMetrics(data);
   //drawAnalysis(data);
}

function drawMetadata(data) {
   var chart = d3.select(".chart");
   
   chart.append("text")
     .attr("x", 3)
     .attr("y", 3)
     .attr("font-family", "sans-serif")
     .attr("font-size", "24px")
     .text(get_property(data, 'Features').name);
}

function drawAnalysis(data) {

}

function drawMetrics(data) {  
   console.log("metrics: " + data);
   console.log("length: " + data.length);
   console.log("length: " + data[0].name);
  
   var chart = d3.select(".chart");
    
   chart.attr("width", WIDTH)
        .attr("height", BAR_HEIGHT * data.length);
  
   var x = d3.scaleLinear()
             .domain([0, WIDTH])
             .range([0, WIDTH]);
  
   console.log("x(0):" + x(0));
  
   var bar = chart.selectAll("g")
                  .data(data)
                  .enter().append("g")
                  .attr("transform", function(d, i) { return "translate(0," + i * BAR_HEIGHT + ")"; });
   
   bar.append("rect")
      .attr("width", WIDTH)
      .attr("height", BAR_HEIGHT - 1);
  
   bar.append("text")
      .attr("text-anchor", "start")
      .attr("x", function(d) { return x(0) + 10*d.level + 3; })
      .attr("y", BAR_HEIGHT / 2)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });
  
   bar.append("text")
      .attr("text-anchor", "end")
      .attr("x", WIDTH - 3)
      .attr("y", BAR_HEIGHT / 2)
      .attr("dy", ".35em")
      .text(function(d) { return get_value(d); });
}

function get_value(d) {
   if (d.size === null) {
      return d.value;
   } else {
      return d.size;
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