const template = document.createElement('template')

template.innerHTML = `
	<style> @import "https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css";
		.card {
			margin: 20px;
		}
	</style>
		<div class="card">
			<header class="card-header">
				<p class="post-author card-header-title">
				</p>
				<a href="#" class="card-header-icon" aria-label="more options">
					<span class="icon">
						<i class="fas fa-angle-down" aria-hidden="true"></i>
					</span>
				</a>
			</header>
			<div class="card-content">
				<div class="content">
					<p class="post-text">
					</p>
				</div>
			</div>
			<div class="card-image">
				<figure class="image is-4by3">
					<img class="image" id="postImage" alt="Placeholder image">
				</figure>
			</div>
		</div>
		`

class PostElement extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: 'open'})
		this.template = template.content.cloneNode(true);
        this.shadowRoot.append(this.template);

        this.getPostData = this.getPostData.bind(this);
        this.addPostData = this.addPostData.bind(this);
    }

    connectedCallback() {

        let postId = this.getAttribute("id");
       	let postData = this.getPostData(postId);
       	this.addPostData(postData);
    }

    addPostData(data) {
    	let tags = ['author', 'text'];
    	for(var i=0; i<tags.length; i++)
    		this.shadowRoot.querySelectorAll('.post-'+tags[i]).forEach(e => e.innerHTML = data[tags[i]]);
    	this.shadowRoot.querySelector("#postImage").setAttribute('src', 'static/postimages/'+data['image']);
    }

    getPostData(postId) {
        let postData;
        $.ajax({
            async: false,
            type: 'GET',
            url: '/post/'+postId,
            success: function(data) {
                postData = data;
            }
        });
        console.log(postData);
        return postData;
    }
}

(function() {
    $.get(
        "total/",
        function(data) {
            data = data['count']
            for (var i=0; i<data.length; i++) {
                var e = document.createElement('post-element');
                e.setAttribute("id", data[i]);
                document.getElementById("posts").appendChild(e);
            }
        }
    )
})();

window.customElements.define("post-element", PostElement);