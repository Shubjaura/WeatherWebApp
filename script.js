$(document).ready(function(){
    $(window).scroll(function(){
        // sticky navbar on scroll script
        if(this.scrollY > 20){
            $('.navbar').addClass("sticky");
        }else{
            $('.navbar').removeClass("sticky");
        }
        
        // scroll-up button show/hide script
        if(this.scrollY > 500){
            $('.scroll-up-btn').addClass("show");
        }else{
            $('.scroll-up-btn').removeClass("show");
        }
    });

    // slide-up script
    $('.scroll-up-btn').click(function(){
        $('html').animate({scrollTop: 0});
        // removing smooth scroll on slide-up button click
        $('html').css("scrollBehavior", "auto");
    });

    // toggle menu/navbar script
    $('.menu-btn').click(function(){
        $('.navbar .menu').toggleClass("active");
        $('.menu-btn i').toggleClass("active");
    });

    // typing text animation script
    var typed = new Typed(".typing", {
        strings: ["Upload the excel file & see the insights!!!", "Get Ready for Data Analysis!!!"],
        typeSpeed: 100,
        backSpeed: 60,
        loop: true
    });
});


function uploadFile() {

    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        console.log(data); // Log the response data to the console
        try {
            data = JSON.parse(data)
            console.log(data); // Log the parsed data to the console

            const val1 = document.getElementById('MaxTemp');
            val1.textContent = 'Max Temp (C) : ' +"  "+  data.Max_temp + " on " + data.Max_temp_date;

            const val2 = document.getElementById('MinTemp');
            val2.textContent = 'Min Temp (C) : ' +"  "+  data.Min_temp + " on "+ data.Min_temp_date;

            const ctx = document.getElementById('myChart');

            new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.chart_data.x,
                datasets: [{
                label: 'Max Temperature (C)',
                data: data.chart_data.y,
                borderWidth: 1
                }]
            },
            options: {
                scales: {
                y: {
                    beginAtZero: true
                }
                }
            }
            });

            const ctx2 = document.getElementById('myChart2');

            new Chart(ctx2, {
            type: 'line',
            data: {
                labels: data.chart_data2.x,
                datasets: [{
                label: 'Min Temperature (C)',
                data: data.chart_data2.y,
                borderWidth: 1
                }]
            },
            options: {
                scales: {
                y: {
                    beginAtZero: true
                }
                }
            }
            });

            const sumContainer = document.querySelector('.sum-container');
            sumContainer.style.display = 'block';

        } catch (error) {
            alert('Error processing data. Please try again.');
        }
    })
    .catch(error => alert('Error uploading file.'));
}