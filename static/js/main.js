console.log('Hello World')

const allBlog = document.getElementById('all-blog')
let msgBox = document.getElementById('msg-box')
let loadBtn = document.getElementById('load-btn')
let loadMore = document.getElementById('load-more')
let visibleBox = document.getElementById('visible')
let visble = 3


const handleGetData = () => {
    $.ajax(
        {
        type:'GET',
        url:`/posts-json/${visble}/`,
        success:function(response){
            // console.log(response.max_size)
            const maxSize = response.max_size
            const data = response.data
            visibleBox.classList.remove('not-visible')
            setTimeout( () => {
                visibleBox.classList.add('not-visible')
                data.map(post => {
                    console.log(post.id)
                    
                    allBlog.innerHTML += `
                    <div class="blog">
                        <div class="blog-flex card">
                            <div class="blog-img">
                                <img src="/media/${post.image}" alt="">
                            </div>
                            <div class="blog-text">
                                <a href="/content/${post.slug}" class="a-title"><h1 class="blog-title">${post.title}</h1></a>
                                <div id="model-content"></div>
                                <p class="created_at light">${post.created_at}</p>
                            </div>
                        </div>
                    </div>`
                })

                if (maxSize){
                    console.log('Done')
                    const msg = 'No More Load'
                    msgBox.innerHTML += `<p class="popular-title upper mt-2">${msg}</p>`
                    loadMore.classList.add('not-visible')
                }

            }, 500)
            
        },
        error:function(error){
            console.log(error)
        }
    }
    )
}

    
handleGetData()
loadBtn.addEventListener('click', () => {
    visble += 3
    handleGetData()
})



