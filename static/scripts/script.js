window.onload = function() {
    var canvas = document.getElementById("graphCanvas1");
    var ctx = canvas.getContext("2d");
  
    // Sample data points with date-value pairs
    var data = [
      { date: "2024-02-01", value: 50 },
      { date: "2024-02-02", value: 80 },
      { date: "2024-02-03", value: 30 },
      { date: "2024-02-04", value: 70 },
      { date: "2024-02-05", value: 50 },
      { date: "2024-02-06", value: 100 },
      { date: "2024-02-07", value: 80 }
    ];
  
    // Function to draw the area graph
    function drawGraph() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
  
      // Calculate the maximum value for scaling
      var maxValue = Math.max.apply(null, data.map(function(point) { return point.value; }));
  
      // Define margin and padding for the graph
      var margin = { top: 30, right: 30, bottom: 30, left: 50 };
      var graphWidth = canvas.width - margin.left - margin.right;
      var graphHeight = canvas.height - margin.top - margin.bottom;
  
      // Draw x-axis and y-axis
      ctx.beginPath();
      ctx.moveTo(margin.left, margin.top);
      ctx.lineTo(margin.left, canvas.height - margin.bottom);
      ctx.lineTo(canvas.width - margin.right, canvas.height - margin.bottom);
      ctx.strokeStyle = "#000";
      ctx.stroke();
  
      // Draw x-axis labels
      ctx.fillStyle = "#000";
      ctx.textAlign = "center";
      ctx.fillText("Date", canvas.width / 2, canvas.height - 5);
  
      // Draw y-axis labels
      ctx.textAlign = "right";
      ctx.fillText("Value", margin.left - 5, margin.top - 10);
  
      // Calculate the scale
      var xScale = graphWidth / (data.length - 1);
      var yScale = graphHeight / maxValue;
  
      // Draw data points
      ctx.beginPath();
      ctx.moveTo(margin.left, canvas.height - margin.bottom - data[0].value * yScale);
      for (var i = 1; i < data.length; i++) {
        ctx.lineTo(margin.left + i * xScale, canvas.height - margin.bottom - data[i].value * yScale);
      }
      ctx.strokeStyle = "#0080FF";
      ctx.stroke();
  
      // Draw x-axis date labels
      ctx.textAlign = "center";
      for (var i = 0; i < data.length; i++) {
        ctx.fillText(data[i].date, margin.left + i * xScale, canvas.height - margin.bottom + 15);
      }
  
      // Draw y-axis value labels
      ctx.textAlign = "right";
      var yAxisLabelStep = maxValue / 5;
      for (var i = 0; i <= 5; i++) {
        var value = i * yAxisLabelStep;
        ctx.fillText(value, margin.left - 10, canvas.height - margin.bottom - (value * yScale));
      }
    }
  
    // Function to handle mouse movement
    function handleMouseMove(event) {
      var rect = canvas.getBoundingClientRect();
      var mouseX = event.clientX - rect.left;
      var mouseY = event.clientY - rect.top;
  
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawGraph();
  
      for (var i = 0; i < data.length; i++) {
        var x = margin.left + i * (canvas.width - margin.left - margin.right) / (data.length - 1);
        var y = canvas.height - margin.bottom - data[i].value * (canvas.height - margin.top - margin.bottom) / Math.max.apply(null, data.map(function(point) { return point.value; }));
  
        if (Math.abs(mouseX - x) < 5 && Math.abs(mouseY - y) < 5) {
          ctx.beginPath();
          ctx.arc(x, y, 5, 0, Math.PI * 2);
          ctx.fillStyle = "#FF0000";
          ctx.fill();
          ctx.fillStyle = "#000000";
          ctx.fillText(`(${data[i].date}, ${data[i].value})`, x, y - 10);
        }
      }
    }
  
    // Add event listener for mouse movement
    canvas.addEventListener("mousemove", handleMouseMove);
  
    // Redraw the graph initially
    drawGraph();
  };
  