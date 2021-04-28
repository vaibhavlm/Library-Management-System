function loadDropbox(){
    $('.js-example-basic-single').select2();

}
function addRow(){
   d3.csv("csv/books.csv", function(error, data) {
        var select = d3.select("body")
          .select("#container-select")
          .append("select")
          .attr("class", "js-example-basic-single")
          .attr("hidden", true)
          .attr("name", "book-choice");

        var rating = d3.select("body")
                  .select("#container-select")
                  .append("input")
                  .attr("type", "number")
                  .attr("value", 5)
                  .attr("min", 1)
                  .attr("max", 5)
                  .attr("name", "book-rating");

        select
          .on("change", function(d) {
            var value = d3.select(this).property("value");
          });

        select.selectAll("option")
            .data(data)
            .enter()
            .append("option")
            .attr("value", function (d) { return d.title; })
            .text(function (d) { return d.title; });

    });
}
$(function(){
    for(let i = 0; i < 5; i++){
        addRow();
    }
});