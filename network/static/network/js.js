document.addEventListener('DOMContentLoaded', function () {
    // Select all SVG elements with an ID that starts with "heart-icon-"
    const svgs = document.querySelectorAll("[id^='heart-icon-']");
    // Loop through each SVG element
    svgs.forEach(svg => {
        // Add a click event listener to the parent element of the SVG
        svg.addEventListener('click', () => {
            const post_id = svg.dataset.postId;
            const fill = svg.querySelector('path').getAttribute('fill')
            console.log(fill);
            const url = fill === 'gray' ? '/like_post/' : '/unlike_post/'
            console.log(url);
            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ post_id: post_id }),
            })
                .then((response) => {
                    if (response.status === 201) {
                        return response.json();
                    }
                    else {
                        throw new Error('Cannot like/unlike yourself.');
                    }
                })
                .then((data) => {
                    // update UI, e.g. change button text, show success message
                    if (fill === 'gray') {
                        svg.querySelector('path').setAttribute('fill', 'red')
                    } else {
                        svg.querySelector('path').setAttribute('fill', 'gray')
                    }
                    document.querySelector(`#num-likes-${post_id}`).innerText = data.num_likes
                })
                .catch((error) => {
                    console.log(error);
                });

            // Change the fill color of the SVG to red when it is clicked
            // svg.parentElement.classList.toggle('liked');
        });
    });

    const followForm = document.getElementById("follow-form");
    if (followForm) {
        const viewedUserUsername = followForm.getAttribute('data-viewed-user-username');
        const followBtn = document.getElementById("follow-btn");
        followForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const url = followBtn.innerText === 'Follow' ? `/follow/${viewedUserUsername}/` : `/unfollow/${viewedUserUsername}/`;
            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            })
                .then((response) => {
                    if (response.status === 201) {
                        return response.json();
                    }
                    else {
                        throw new Error('Cannot unfollow yourself.');
                    }
                })
                .then((data) => {
                    // update UI, e.g. change button text, show success message
                    if (followBtn.innerText === "Follow") {
                        followBtn.innerText = "Unfollow";
                    } else {
                        followBtn.innerText = "Follow";
                    }
                    const numFollowers = document.querySelector(".profile-info > p:first-of-type");
                    numFollowers.innerText = `Followers: ${data.num_followers}`;
                })
                .catch((error) => {
                    console.log(error);
                });
        });
    }


    // Get all the edit buttons on the page
    const editButtons = document.querySelectorAll('.edit');
    

    // Loop through each button and attach a click event listener
    editButtons.forEach(button => {
        console.log('form selector:', button.closest('.post-container').querySelector('form'));
        
        button.addEventListener('click', event => {
            // Get the form element for this post
            const form = button.closest('.post-container').querySelector('form');

            // Get the paragraph element for this post content
            const postContent = button.closest('.post-container').querySelector('.show-post-content');

            // Show the form element
            form.style.display = 'block';

            // Hide the paragraph element
            postContent.style.display = 'none';

            // Get the cancel button element for this post form
            const cancelButton = form.querySelector('.cancel-button');

            // Add a click event listener to the cancel button
            cancelButton.addEventListener('click', event => {
                // Prevent the form from submitting
                event.preventDefault();

                // Hide the form element
                form.style.display = 'none';

                // Show the paragraph element
                postContent.style.display = 'block';
            });
        });
    });
})
