//Put metals type in metals data into array
//Put metals type in metals data into array
// - Delete non type columns from metals data set
// - Remove duplicate metals names
var metals_type = JSON.parse(JSON.stringify(metals_table));
metals_type.forEach(function(currentItem) {
    delete currentItem["Year"];
    delete currentItem["Price"];
});
var metals_array = Array();
for(var i = 0; i < (metals_type.length - 1); i++) {
    if ((metals_type[i]['Type'] != metals_type[i+1]['Type']) || (i==0)) {
        metals_array.push(metals_type[i+1]['Type']);
    }
}
console.log(metals_array);
        
var metal_1_dropdown = document.getElementById("metal-1-select");
for(index in metals_array) {
    metal_1_dropdown.options[metal_1_dropdown.options.length] = new Option(metals_array[index], index);
}    

metal_2_dropdown = document.getElementById("metal-2-select");
for(index in metals_array) {
    metal_2_dropdown.options[metal_2_dropdown.options.length] = new Option(metals_array[index], index);
}    

// Set metal selection to default
var metal_1_selection = metal_1_dropdown.options[metal_1_dropdown.selectedIndex].text;       
var metal_2_selection = metal_2_dropdown.options[metal_2_dropdown.selectedIndex].text;       
document.getElementById("CalculatePriceCorrelation").onclick = function () { 
    metal_1_selection = metal_1_dropdown.options[metal_1_dropdown.selectedIndex].text;       
    metal_2_selection = metal_2_dropdown.options[metal_2_dropdown.selectedIndex].text;       

    //Ensure metals table dataset unchanged by creating metals data variable through stringify 
    var metals_data = JSON.parse(JSON.stringify(metals_table));    
    
    //For metal 1 selected
    // - Filter overall data set so it only contains type of metal selected
    // - Remove elements with blank price
    // - Rename price to price 1
    var metal_1 = metals_data.filter(function (el) {
      return el.Type == metal_1_selection;
    });
    metal_1.forEach(function(currentItem) {
        delete currentItem["Type"];
    });
    function RemoveNode_1(col, val) {
        return metal_1.filter(function(emp) {
            if (emp[col] == val) {
                return false;
            }
            return true;
        });
    }
    var metal_1 = RemoveNode_1("Price", "");
    metal_1 = JSON.parse(JSON.stringify(metal_1).split('"Price":').join('"Price_1":'));
    console.log(metal_1);

    //For metal 2 selected
    // - Filter overall data set so it only contains type of metal selected
    // - Remove elements with blank price
    // - Rename price to price 2
    var metal_2 = metals_data.filter(function (el) {
      return el.Type == metal_2_selection;
    });
    metal_2.forEach(function(currentItem) {
        delete currentItem["Type"];
    });
    function RemoveNode_2(col, val) {
        return metal_2.filter(function(emp) {
            if (emp[col] == val) {
                return false;
            }
            return true;
        });
    }
    var metal_2 = RemoveNode_2("Price", "");    
    metal_2 = JSON.parse(JSON.stringify(metal_2).split('"Price":').join('"Price_2":'));
    console.log(metal_2);

    //Create overall metal data set
    // - Combine metal 1 and metal 2 data sets
    var metal = [...[metal_1, metal_2].reduce((m, a) => (a.forEach(o => m.has(o.Year) && Object.assign(m.get(o.Year), o) || m.set(o.Year, o)), m), new Map).values()];
    
    //Prepare metals data for graphing
    // - Sort data set by year
    // - Create arrays for year, metal 1 and metal 2
    var metals_graph = JSON.parse(JSON.stringify(metal));
    function compare(a, b) {
          // Use toUpperCase() to ignore character casing
          const bandA = a.Year.toUpperCase();
          const bandB = b.Year.toUpperCase();
          let comparison = 0;
          if (bandA > bandB) {
            comparison = 1;
          } else if (bandA < bandB) {
            comparison = -1;
          }
          return comparison;
    }
    metals_graph.sort(compare);
    var year_graph = Array();
    for(var i = 0; i < metals_graph.length; i++) {
        year_graph.push(parseFloat(metals_graph[i]['Year']));
    }
    var metal_1_graph = Array();
    for(var i = 0; i < metals_graph.length; i++) {
        try {
            metal_1_graph.push(parseFloat(metals_graph[i]['Price_1']));
        }
        catch(err) {
            metal_1_graph.push(parseFloat(""));
        }
    }
    var metal_2_graph = Array();
    for(var i = 0; i < metals_graph.length; i++) {
        try {
            metal_2_graph.push(parseFloat(metals_graph[i]['Price_2']));
        }
        catch(err) {
            metal_2_graph.push(parseFloat(""));
        }
    }

    //Graph metals data
    // - Create line chart with prices of two metals graphed    
    years = year_graph
    new Chart(document.getElementById("line-chart"), {
          type: 'line',
          data: {
            labels: years,
            datasets: [{ 
                data: metal_1_graph,
                label: metal_1_selection,
                borderColor: "#3e95cd",
                fill: false
              }, { 
                data: metal_2_graph,
                label: metal_2_selection,
                borderColor: "#8e5ea2",
                fill: false
              }        ]
          },
          options: {
            title: {
              display: true,
              text: 'Price history of selected metals in dollars'
            }
          }
    });

    //Clean up overall metal data set    
    // - Remove elements for years that don't have both price 1 and price 2 data
    for(var prop in metal) {
        if(metal.hasOwnProperty(prop)) {
            if(Object.keys(metal[prop]).length < 3) {
                delete metal[prop];
            }
        }
    }
    var metal = metal.filter(value => JSON.stringify(value) !== '{}');
    console.log(metal);
    
    //Create metal 1 price data set for correlation calculation
    // - Remove non price 1 variables
    // - Convert to array of numbers
    var price_1 = JSON.parse(JSON.stringify(metal));
    price_1.forEach(function(currentItem) {
        delete currentItem["Year"];
        delete currentItem["Price_2"];
    });
    var data_1 = Array();
    for(var i = 0; i < price_1.length; i++) {
        data_1.push(parseFloat(price_1[i]['Price_1']));
    }
    console.log(data_1);

    //Create metal 2 price data set for correlation calculation
    // - Remove non price 2 variables
    // - Convert to array of numbers
    var price_2 = JSON.parse(JSON.stringify(metal));
    price_2.forEach(function(currentItem) {
        delete currentItem["Year"];
        delete currentItem["Price_1"];
    });
    var data_2 = Array();
    for(var i = 0; i < price_2.length; i++) {
        data_2.push(parseFloat(price_2[i]['Price_2']));
    }
    console.log(data_2);

    //Calculate price correlation between metal 1 and metal 2
    var data = new Array(
                data_1, data_2
            );
    var corr_coeff = pearsonCorrelation(data,0,1)
    console.log(corr_coeff);

    if (metal_1_selection != metal_2_selection) {
        document.getElementById("demo").innerHTML = "Price correlation is: " + corr_coeff.toFixed(2);         
    } else {
        document.getElementById("demo").innerHTML = "Please select two different metals";         
    }

    
    
    
    
    
    
};
