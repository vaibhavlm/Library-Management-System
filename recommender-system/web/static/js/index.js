function addRow(){
   d3.csv("csv/books1k.csv", function(error, data) {

        var select = d3.select("body")
          .select("#container-select")
          .append("select")
          .attr("class", "js-example-basic-single col-6")
          .attr("name", "book-choice");

        var rating = d3.select("body")
                  .select("#container-select")
                  .append("input")
                  .attr("class", "col-1 offset-1 mb-3")
                  .attr("type", "number")
                  .attr("value", 5)
                  .attr("min", 1)
                  .attr("max", 5)
                  .attr("name", "book-rating");

        select.selectAll("option")
            .data(data)
            .enter()
            .append("option")
            .attr("value", function (d) { return d.title; })
            .text(function (d) { return d.title; });

    });
}
$(function(){

    $("#get-started").on('click', function(){
        $("#select-form").prepend("<span class='offset-3'>Title</span><span class='offset-4 text-center'>Rating</span><p></p>")
        for(let i = 0; i < 5; i++)addRow();
        $('#submit').removeAttr('hidden');
        $(this).hide();
    });

    $("#hover-to-hide").hover(function() {
        $('.js-example-basic-single').select2();
    });

});