function buildMetadata(Id) {

  // @TODO: Complete the following function that builds the metadata panel
  // Use `d3.json` to fetch the metadata for a sample
  var url = "/data/" + Id;
  d3.json(url).then(function(Id){

    // Use d3 to select the panel with id of `#sample-metadata`
    var sample_metadata = d3.select("#sample-metadata");

    // Use `.html("") to clear any existing metadata
    sample_metadata.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    Object.entries(Id).forEach(([key, value]) => {
      var row = sample_metadata.append("p");
      row.text(`${key}: ${value}`);

    })
  })
};

function buildCharts(Id) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  var url = `/data/${Id}`;
  d3.json(url).then(function(data) {

    // @TODO: Build a Bubble Chart using the sample data
    var xValues = ['Base Pay', 'Overtime Pay', 'Other Pay', 'Benefits', 'Total Pay Benefits'];
    var yValues = [data.BasePay, data.OvertimePay, data.OtherPay, data.Benefits, data.TotalPayBenefits];

    var trace1 = {
      x: xValues,
      y: yValues,
      type: 'bar'
    };

    var data = [trace1];

    var layout = {
      title: "Compensation Breakdown"
    };

    Plotly.newPlot('bar', data, layout);


    // @TODO: Build a Pie Chart
    d3.json(url).then(function(data) {
      var pieValue = [data.BasePay, data.OvertimePay, data.OtherPay, data.Benefits, data.TotalPayBenefits];
      var pielabel = ['Base Pay', 'Overtime Pay', 'Other Pay', 'Benefits', 'Total Pay Benefits'];
      
      
      var trace2 = {
        values: pieValue,
        labels: pielabel,
        type: 'pie'
      };

      var data2 = [trace2];

      var layout = {
        title: "Percentage of Compensation of " + data.EmployeeName,
      };

      Plotly.newPlot('pie', data2, layout);
    });
  });
};

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleId) => {
    sampleId.forEach((Id) => {
      selector
        .append("option")
        .text(Id)
        .property("value", Id);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleId[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
};

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
};

// Initialize the dashboard
init();