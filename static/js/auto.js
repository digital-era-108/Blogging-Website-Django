console.log('Autocompltete')
new Autocomplete('#autocomplete', {
    search : input => {
        console.log(input)
        const url = `/post-search/?search=${input}`
        return new Promise(resolve => {
            fetch(url)
            .then(response => response.json())
            .then(data => {
                // console.log(data.payload)
                resolve(data.payload)
            })
        })
    },
    renderResult : (result, propes) => {
        console.log(propes)
        let group = ''
        if(result.index % 3 == 0){
            group = `<li class="group">Group</li>`
        }
        return `
            <a href="/content/${result.slug}" class="a-title">
                <li ${propes}>
                    <div class="wiki-title">${result.title}</div>
                </li>
            </a>
        `
    }
})