const template = document.createElement('template')

template.innerHTML = `
	<style> @import "https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css";
		.card {
			margin: 20px;
		}
		.post-author, .post-time {
		    display: block;
		}
		.card-header {
		    padding: .75rem 1rem;
		    display: block;
		}
	</style>
		<div class="card">
			<header class="card-header">
                <h6 class="post-author title is-size-4"></h6>
                <time class="post-time subtitle is-size-7"></time>
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
    	let tags = ['author', 'text', 'time'];
    	for(var i=0; i<tags.length; i++)
    		this.shadowRoot.querySelectorAll('.post-'+tags[i]).forEach(e => e.innerHTML = data[tags[i]]);
    	if(data.hasOwnProperty('image'))
    	    this.shadowRoot.querySelector("#postImage").setAttribute('src', 'static/'+data['image']);
    	else
    	    this.shadowRoot.querySelector(".image").setAttribute('style', 'display: none');
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