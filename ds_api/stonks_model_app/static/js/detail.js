$(document).ready(function () {
    $('.clickable').click(function (el) {
        console.log(el.target.id)
        if (el.target.id == "show") {
            $('#dots').hide()
            $('#show').hide()
            $('#description_part2').show()
            $('#hide').show()
        } else {
            $('#hide').hide()
            $('#description_part2').hide()
            $('#dots').show()
            $('#show').show()
        }
    })
})