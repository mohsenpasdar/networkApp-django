document.addEventListener('DOMContentLoaded', function () {
    const followForm = document.getElementById("follow-form");
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
})
