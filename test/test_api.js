const apiPrefix = 'http://127.0.0.1:5000/';
fetch(apiPrefix + 'inform_brief?type=1&number=2&pageIndex=ab').then(res => {
    if (res.ok) {
        return res.json();
    }
}).then(json => {
    document.write(JSON.stringify(json))
});