function loadSelect2() {
    $('.js-example-basic-single').select2();
}

function addRow() {
    d3.csv("csv/books1k.csv", function (error, data) {

        // selecting the table row
        var selectRow = d3.select("body")
            .select("#container-select")
            .select("table")
            .append("tr")

        // generation of the <select> tag
        var select = selectRow.append("td")
            .append("div")
            .attr("class", "select-div")
            .append("select")
            .attr("class", "js-example-basic-single")
            .attr("name", "book-choice");

        // adding the number input for ratings
        selectRow.append("td")
            .append('div')
            .attr("class", "rating-div")
            .append("input")
            .attr("type", "number")
            .attr("value", 3)
            .attr("min", 1)
            .attr("max", 5)
            .attr("name", "book-rating")
            .style("text-align", "center")
            .style("height", "2.875rem")
            .style("width", "2.875rem")
            .style("border", "1px solid #CED4DA")
            .style("border-radius", "4px");

        // adding the options to each <select> tag
        select.selectAll("option")
            .data(data)
            .enter()
            .append("option")
            .attr("value", function (d) { return d.title; })
            .text(function (d) { return d.title; });

        // set-up the select2 utility
        select.forEach(function (elem) {
            $(elem).on('change', loadSelect2());
        });
    });

}

// Delete row functionality
function deleteRow() {
    var len = $("div.select-div").length;
    if (len <= 5) {
        Swal.fire({
            title: 'Error!',
            text: 'Minimum 5 recommendations are required. Cannot delete any more rows',
            icon: 'error',
            confirmButtonText: 'Understood'
        });
        return
    }
    $("tr:last").remove();
}


// function to make sure the user chooses different books and gives at least 1 different rating in their selction
function validateInput() {

    let selectedChoices = [];
    $("#container-select option:checked").each(function () {
        selectedChoices.push($(this).val())
    });
    let setOfSelectedChoices = new Set(selectedChoices);
    if (selectedChoices.length === setOfSelectedChoices.size) {
        Swal.fire({
            title: 'Success!',
            text: 'Recommendations successfully submitted!',
            icon: 'success',
            confirmButtonText: 'Great!',
            timer: 3000
        });
        $("form")[0].submit();
    }
    else {
        Swal.fire({
            title: 'Error!',
            text: 'Multiple books with similar titles, please choose a different selection',
            icon: 'error',
            confirmButtonText: 'Understood'
        });
    }
}

$(function () {

    for (let i = 0; i < 5; i++) {
        addRow();
    }

});