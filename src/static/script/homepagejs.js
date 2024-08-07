const backgroundImagestore = [
    "/static/images/plantgrowing.jpg",
    "/static/images/farm.jpg",
    "/static/images/farmwheat.jpg",
];
var count = 0;
document.getElementById("prev").addEventListener("click" , ()=>{
    document.getElementById("mycarousel").style.backgroundImage = `url(${backgroundImagestore[count]})`;
    count = (count+1) % 3;
});

document.getElementById("next").addEventListener("click" , ()=>{
    document.getElementById("mycarousel").style.backgroundImage = `url(${backgroundImagestore[count]})`;
    count = (count+1) % 3;
});