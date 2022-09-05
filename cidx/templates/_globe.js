am5.ready(function () {

    // Create root element
    // https://www.amcharts.com/docs/v5/getting-started/#Root_element
    var root = am5.Root.new("globe3d");


    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    root.setThemes([
        am5themes_Animated.new(root)
    ]);


    // Create the map chart
    // https://www.amcharts.com/docs/v5/charts/map-chart/
    var chart = root.container.children.push(am5map.MapChart.new(root, {
        panX: "rotateX",
        panY: "rotateY",
        projection: am5map.geoOrthographic()
    }));


    // Create series for background fill
    // https://www.amcharts.com/docs/v5/charts/map-chart/map-polygon-series/#Background_polygon
    var backgroundSeries = chart.series.push(
        am5map.MapPolygonSeries.new(root, {})
    );
    backgroundSeries.mapPolygons.template.setAll({
        fill: root.interfaceColors.get("alternativeBackground"),
        fillOpacity: 0.1,
        strokeOpacity: 0
    });
    backgroundSeries.data.push({
        geometry:
            am5map.getGeoRectangle(90, 180, -90, -180)
    });


    // Create main polygon series for countries
    // https://www.amcharts.com/docs/v5/charts/map-chart/map-polygon-series/
    var polygonSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {
        geoJSON: am5geodata_worldLow
    }));
    polygonSeries.mapPolygons.template.setAll({
        fill: root.interfaceColors.get("alternativeBackground"),
        fillOpacity: 0.15,
        strokeWidth: 0.5,
        stroke: root.interfaceColors.get("background")
    });


    // Create polygon series for projected circles
    var circleSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {}));
    circleSeries.mapPolygons.template.setAll({
        templateField: "polygonTemplate",
        tooltipText: "{name}:{value}"
    });

    // Define data
    var colors = am5.ColorSet.new(root, {});

var data = {{ world_map | safe }};

var valueLow = Infinity;
var valueHigh = -Infinity;

for (var i = 0; i < data.length; i++) {
    var value = data[i].value;
    if (value < valueLow) {
        valueLow = value;
    }
    if (value > valueHigh) {
        valueHigh = value;
    }
}

// radius in degrees
var minRadius = 0.5;
var maxRadius = 5;

// Create circles when data for countries is fully loaded.
polygonSeries.events.on("datavalidated", function () {
    circleSeries.data.clear();

    for (var i = 0; i < data.length; i++) {
        var dataContext = data[i];
        var countryDataItem = polygonSeries.getDataItemById(dataContext.id);
        var countryPolygon = countryDataItem.get("mapPolygon");

        var value = dataContext.value;

        var radius = minRadius + maxRadius * (value - valueLow) / (valueHigh - valueLow);

        if (countryPolygon) {
            var geometry = am5map.getGeoCircle(countryPolygon.visualCentroid(), radius);
            circleSeries.data.push({
                name: dataContext.name,
                value: dataContext.value,
                polygonTemplate: dataContext.polygonTemplate,
                geometry: geometry
            });
        }
    }
})


// Make stuff animate on load
chart.appear(1000, 100);

}); // end am5.ready()
