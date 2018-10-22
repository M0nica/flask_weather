function toggleWeather(city, state, unit) {
    var url = "/weather/" + city + "/" + state;
    if(unit === "False") {
        url += '?toToggle=1';
    }
    location.replace(url);
}
