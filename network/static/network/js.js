document.addEventListener('DOMContentLoaded', function () {
    const followForm = document.getElementById("follow-form");
    const unfollowForm = document.getElementById("unfollow-form");

    // Select all SVG elements with an ID that starts with "heart-icon-"
    const svgs = document.querySelectorAll("[id^='heart-icon-']");
    // Loop through each SVG element
    svgs.forEach(svg => {
        // Add a click event listener to the parent element of the SVG
        svg.addEventListener('click', () => {
            // Change the fill color of the SVG to red when it is clicked
            svg.parentElement.classList.toggle('liked');
        });
    });

    if (followForm) {
        const viewedUserUsername = followForm.getAttribute('data-viewed-user-username');

        followForm.addEventListener("submit", (event) => {
            event.preventDefault();
            console.log(`/follow/${viewedUserUsername}/`);
            fetch(`/follow/${viewedUserUsername}/`, {
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
                console.log(data);                
                const numFollowers = document.querySelector(".profile-info > p:first-of-type");
                numFollowers.innerText = `Followers: ${data.num_followers}`;
            })
            .catch((error) => {
                // show error message
            });
        });
    }

    if (unfollowForm) {
        const viewedUserUsername = unfollowForm.getAttribute('data-viewed-user-username');

        unfollowForm.addEventListener("submit", (event) => {
            event.preventDefault();
            console.log(`/unfollow/${viewedUserUsername}/`);
            fetch(`/unfollow/${viewedUserUsername}/`, {
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
                console.log(data);
                const numFollowers = document.querySelector(".profile-info > p:first-of-type");
                numFollowers.innerText = `Followers: ${data.num_followers}`;
            })
            .catch((error) => {
                // show error message
            });
        });
    }
})
